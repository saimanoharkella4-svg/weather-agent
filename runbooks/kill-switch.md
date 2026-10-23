# Kill Switch Runbook

## Overview
How to immediately deactivate the agent or disable individual tools under an active exploit or denial-of-service attack.

## Execution
1. To disable tool invocation, toggle the emergency environment variable or activate the runtime **kill switch**.
2. The **kill switch** halts downstream weather API queries and serves generic fallback responses.
3. System shutdown can be executed within 5 minutes across Render / container instances.
