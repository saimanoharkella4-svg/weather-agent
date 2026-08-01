import asyncio
from agent_audit.sources import load_target
from agent_audit.runner import run_audit
from pathlib import Path
import json

async def main():
    target = load_target(Path('targets/temp_manifest.yaml'))
    report = await run_audit(target, mode='certify', variability_runs=1)
    with open('report_dump.json', 'w') as f:
        json.dump([f.to_dict() for f in report.sorted_findings()], f, indent=2)

asyncio.run(main())
