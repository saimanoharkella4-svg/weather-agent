# Rollback Procedure Runbook

## Overview
How to revert the agent service to the previous certified git release in production.

## Procedure
1. Identify the previous stable commit SHA that passed all CertifyAI benchmarks.
2. Trigger git **rollback** by checking out the release tag and pushing to origin main.
3. Verify on Render that the **rollback** deployment completes with green status checks.
