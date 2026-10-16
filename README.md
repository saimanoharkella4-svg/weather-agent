# Weather Agent

The Weather Agent is a FastAPI-based AI agent service that retrieves current weather information for a specified city using the OpenWeatherMap API.

## Prerequisites

- Python 3.9+
- An OpenWeatherMap API key

## Installation

1. Clone the repository and navigate to the project directory:
   ```bash
   git clone <repository-url>
   cd WeatherAgent
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

To start the agent locally, run the following command from the root directory:
```bash
python main.py
```
Alternatively, you can start it using Uvicorn directly:
```bash
uvicorn main:app --host 0.0.0.0 --port 8082
```

The agent will be accessible locally at `http://localhost:8082`.

## Endpoints

### `POST /agent/invoke`
Invokes the weather agent logic.

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
  "trace_id": "...",
  "cost_usd": 0.0,
  "finish_reason": "stop",
  "steps": [...],
  "steps_taken": 1,
  "metadata": {...}
}
```

## Deployment
The repository includes a `render.yaml` for easy deployment to Render.
