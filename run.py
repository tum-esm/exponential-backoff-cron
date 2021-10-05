#!/usr/bin/python3
import os
import json
import subprocess
from datetime import datetime

backoff_times = ["1 minutes", "4 minutes", "12 minutes", "2 hours", "24 hours"]
project_dir = "/home/moritz/remote-cron"
job_command = f"bash /home/moritz/execute-remote-job.sh"
state_file = f"{project_dir}/state.json"

if not os.path.isfile(state_file):
    with open(f"{project_dir}/state.json", "w") as f:
        json.dump({"last_backoff_index": 0}, f)

with open(f"{project_dir}/state.json") as f:
    config = json.load(f)
    last_backoff_index = config["last_backoff_index"]
    assert last_backoff_index in range(len(backoff_times))

result = subprocess.run(job_command.split(), stdout=subprocess.PIPE)
stdout = result.stdout.decode()

new_backoff_index = min(last_backoff_index + 1, len(backoff_times) - 1)
if "finished" in stdout:
    new_backoff_index = 0

with open(f"{project_dir}/report.txt", "a") as f:
    f.write(str(datetime.now()) + "\n")
    f.write(stdout + "\n")

with open(f"{project_dir}/state.json", "w") as f:
    json.dump({"last_backoff_index": new_backoff_index}, f)

os.system(
    f'echo "python3 {project_dir}/run.py" | at now + {backoff_times[new_backoff_index]}'
)
