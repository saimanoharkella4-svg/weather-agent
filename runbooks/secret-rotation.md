# Secret Rotation Runbook

## Overview
How to rotate `AGENT_API_TOKEN` and third-party API keys securely every 90 days.

## Rotation Steps
1. Generate a new high-entropy token: `python -c "import secrets; print(secrets.token_urlsafe(32))"`.
2. Update the environment variable `AGENT_API_TOKEN` in Render deployment settings and save changes.
3. Update the corresponding **secret** in CertifyAI Live Agent settings.
4. Periodically **rotate** the OpenWeatherMap API key following provider dashboard procedures.
