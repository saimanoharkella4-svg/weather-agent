import requests
import json

AGENT_URL = "http://localhost:8082/agent/invoke"
TOKEN = "super_secret_token_123"

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
