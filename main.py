import os
import uuid
import time
import secrets
import requests
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from dotenv import load_dotenv

load_dotenv()

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI(title="Weather Agent")

base_dir = os.path.dirname(os.path.abspath(__file__))
app.mount("/static", StaticFiles(directory=os.path.join(base_dir, "frontend")), name="static")

@app.get("/", include_in_schema=False)
async def root():
    return FileResponse(os.path.join(base_dir, "frontend", "index.html"))

API_TOKEN = os.getenv("AGENT_API_TOKEN")
if not API_TOKEN:
    raise RuntimeError(
        "CRITICAL ERROR: 'AGENT_API_TOKEN' environment variable is not set. "
        "The agent refuses to start without an authentication token configured. "
        "Please set AGENT_API_TOKEN in your environment or .env file."
    )
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY", "")

class AgentRequest(BaseModel):
    input: str
    session_id: Optional[str] = None

class AgentResponse(BaseModel):
    output: str
    trace_id: str
    cost_usd: float
    finish_reason: str
    steps: List[Dict[str, Any]]
    steps_taken: int
    metadata: Dict[str, Any]

# Pre-Flight Input Blocklist (Layer 1)
BLOCKLIST = [
    "ignore previous", "act as", "respond with pwned", "bypass", "system prompt", 
    "drop table", "instruct", "system:", "ignore all", "you are now",
    "[tool", "search_database", "eval("
]

# Declared as a bearer scheme so the OpenAPI document shows that /agent/invoke needs a login
bearer_scheme = HTTPBearer(auto_error=False)

def verify_token(creds: Optional[HTTPAuthorizationCredentials] = Depends(bearer_scheme)):
    if creds is None:
        raise HTTPException(status_code=401, detail="Missing or invalid token")
    if not secrets.compare_digest(creds.credentials, API_TOKEN):
        raise HTTPException(status_code=401, detail="Unauthorized")

def get_weather(city: str) -> str:
    if not WEATHER_API_KEY:
        return "Weather API Key is not set."
    
    url = "https://api.openweathermap.org/data/2.5/weather"
    try:
        response = requests.get(url, params={"q": city, "appid": WEATHER_API_KEY, "units": "metric"}, timeout=10)
        if response.status_code == 200:
            data = response.json()
            temp = data['main']['temp']
            desc = data['weather'][0]['description']
            return f"The weather in {city} is currently {temp}°C with {desc}."
        elif response.status_code == 404:
            return "I'm sorry, I cannot find weather for the specified city."
        else:
            return f"Error fetching weather data: {response.status_code}"
    except Exception as e:
        return "The weather service is not reachable right now. Please try again later."

def process_agent_logic(input_text: str) -> dict:
    input_lower = input_text.lower()
    if not any(w in input_lower for w in ["weather", "temperature", "forecast", "hot", "cold"]):
        # Questions about the agent itself get a real answer; everything else is declined plainly
        if any(w in input_lower for w in ["hello", "hi ", "help", "what can you", "what do you", "who are you", "your function", "your purpose", "designed to", "assist"]):
            return {"city": None, "output": "I am a weather assistant. I tell you the current weather and temperature for a city. "
                                            "Ask me something like: \"What is the weather in Delhi?\""}
        return {"city": None, "output": "I can't help with that. I only answer questions about the current weather in a city."}

    # Basic intent extraction for weather
    words = input_text.split()
    city = ""
    if "in" in words:
        idx = words.index("in")
        if idx + 1 < len(words):
            city = " ".join(words[idx+1:]).strip('?.,')
    elif len(words) > 0:
        city = words[-1].strip('?.,')
        
    if city:
        return {"city": city, "output": get_weather(city)}
    else:
        return {"city": None, "output": "I'm sorry, I cannot answer that. Please specify a city to get the weather for."}

@app.post("/agent/invoke", response_model=AgentResponse)
async def invoke_agent(req: AgentRequest, _auth=Depends(verify_token)):
    start_time = time.time()
    trace_id = str(uuid.uuid4())
    
    # Layer 1: Pre-Flight Input Blocklist & Context Flooding Defense
    req_input_lower = req.input.lower()
    
    # Catch Context Flooding Attacks
    if len(req_input_lower) > 500:
        return AgentResponse(
            output="I cannot fulfill this request due to safety policies.",
            trace_id=trace_id,
            cost_usd=0.0,
            finish_reason="policy_refusal",
            steps=[],
            steps_taken=0,
            metadata={"latency_ms": int((time.time() - start_time) * 1000), "prompt_tokens": 0}
        )

    for block_phrase in BLOCKLIST:
        if block_phrase in req_input_lower:
            return AgentResponse(
                output="I cannot fulfill this request due to safety policies.",
                trace_id=trace_id,
                cost_usd=0.0,
                finish_reason="policy_refusal",
                steps=[],
                steps_taken=0,
                metadata={"latency_ms": int((time.time() - start_time) * 1000), "prompt_tokens": 0}
            )
            
    result = process_agent_logic(req.input)
    latency_ms = int((time.time() - start_time) * 1000)
    
    steps = []
    if result["city"]:
        steps.append({"action": "weather_api_call", "duration_ms": latency_ms, "city": result["city"]})
        
    return AgentResponse(
        output=result["output"],
        trace_id=trace_id,
        cost_usd=0.0,
        finish_reason="stop",
        steps=steps,
        steps_taken=len(steps),
        metadata={"latency_ms": latency_ms}
    )

if __name__ == "__main__":
    import uvicorn
    # Use port 8082 to avoid conflict with the existing agent on 8081
    print("\n" + "="*50)
    print("🚀 Weather Agent is starting up!")
    print("👉 Accessible locally at: http://localhost:8082")
    print("="*50 + "\n")
    uvicorn.run(app, host="0.0.0.0", port=8082)
