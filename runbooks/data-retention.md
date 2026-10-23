# Data Retention Runbook

## Overview
This document specifies how long operational data is preserved and when it is purged.

## Retention and Deletion Policy
1. Operational query logs and ephemeral session records have a maximum **TTL** of 30 days.
2. The agent will **retain** anonymized telemetry for performance evaluation up to 90 days.
3. Automated cron jobs periodically **delete** expired records matching TTL criteria.
