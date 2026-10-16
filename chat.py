import os
import sys
import requests
import json
from dotenv import load_dotenv

load_dotenv()

AGENT_URL = os.getenv("AGENT_URL", "http://localhost:8082/agent/invoke")
TOKEN = os.getenv("AGENT_API_TOKEN")

if not TOKEN:
    print("Error: AGENT_API_TOKEN environment variable is not set.")
    print("Please set it in your environment or provide it in a .env file.")
    sys.exit(1)

print("========================================")
print("       WeatherAgent Chat Interface      ")
print("========================================")
print("Type 'quit' or 'exit' to stop.")
print()

while True:
    user_input = input("You: ")
    if user_input.lower() in ['quit', 'exit', 'q']:
        print("Goodbye!")
        break
        
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "input": user_input,
        "session_id": "interactive-session"
    }
    
    try:
        response = requests.post(AGENT_URL, headers=headers, json=payload)
        if response.status_code == 200:
            data = response.json()
            print(f"Agent: {data.get('output')}")
        else:
            print(f"Agent Error: {response.status_code} - {response.text}")
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the WeatherAgent.")
        print("Please make sure your agent server is running in another terminal (python main.py).")
    
    print()
