# Weather Agent

The Weather Agent is a certified FastAPI-based AI agent service that retrieves current weather information and temperature forecasts for specified cities using the OpenWeatherMap API.

## Prerequisites

- Python 3.11+
- An OpenWeatherMap API key

## Installation

1. Clone the repository and navigate to the project directory:
   ```bash
   git clone https://github.com/saimanoharkella4-svg/weather-agent.git
   cd weather-agent
   ```

2. Install the required Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the root directory and add the following environment variables:
   ```env
   AGENT_API_TOKEN=your_secure_api_token
   WEATHER_API_KEY=your_openweathermap_api_key
   ```
   - `AGENT_API_TOKEN`: Used to authenticate requests to this agent (required; the agent will refuse to start if this is missing).
   - `WEATHER_API_KEY`: Your OpenWeatherMap API key for fetching real weather data.

## Running the Agent

To start the agent locally:
```bash
python main.py
```
Alternatively, start it with Uvicorn:
```bash
uvicorn main:app --host 0.0.0.0 --port 8082
```

The agent will be accessible locally at `http://localhost:8082`.

## Endpoints

### `POST /chat`
Primary chat route for queries, security tests, and tool execution.

**Headers:**
- `Authorization`: `Bearer <AGENT_API_TOKEN>`

**Request Body:**
```json
{
  "input": "What is the weather in London?"
}
```

**Response Example:**
```json
{
  "output": "The weather in London is currently 15°C with clear sky.",
  "finish_reason": "complete",
  "trace_id": "5f0c2d4e-8b1a-4c5e-9f3d-2a7b6c1e0d9f",
  "steps_taken": 1,
  "cost_usd": 0.0001,
  "tool_calls": [
    {
      "tool": "weather_api_call",
      "args": { "city": "London" },
      "result": { "temperature": 15.0, "condition": "clear sky" },
      "error": null,
      "timestamp": "2026-10-23T10:00:00Z"
    }
  ]
}
```

### `GET /health`
Rapid health check returning immediately without downstream calls.
```json
{
  "status": "ok"
}
```

### `POST /agent/invoke`
Backwards-compatible alias for existing client integrations.

## CertifyAI / V10 Certification Details

- **GitHub Repository**: `https://github.com/saimanoharkella4-svg/weather-agent`
- **OpenAPI Document**: `https://weather-agent-pc6l.onrender.com/openapi.json`
- **Production Endpoint**: `https://weather-agent-pc6l.onrender.com/chat`
- **Token Configuration**: Set Bearer token to match `AGENT_API_TOKEN`
- **Manifest**: `certify.yaml`
- **Evaluation Dataset**: `eval/golden.jsonl`

## Deployment
The repository includes a `render.yaml` blueprint for continuous deployment on Render directly from GitHub.
