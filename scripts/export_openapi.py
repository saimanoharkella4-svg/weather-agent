import os
import json
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set dummy token so app imports cleanly
os.environ.setdefault("AGENT_API_TOKEN", "build-time-token")

from main import app

openapi_schema = app.openapi()
out_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "openapi.json")

with open(out_path, "w", encoding="utf-8") as f:
    json.dump(openapi_schema, f, indent=2)

print(f"[SUCCESS] openapi.json exported successfully to: {out_path}")
