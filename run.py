#!/usr/bin/python3
import os
import json
import subprocess
from datetime import datetime

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
with open(f"{PROJECT_DIR}/config.json", "r") as f:
    config = json.load(f)

BACKOFF_TIMES = config["backoff_times"]
JOB_COMMAND = config["job_command"]
SHORT_DELAY_KEYWORD = config["keyword_for_short_delay"]
LONG_DELAY_KEYWORD = config["keyword_for_long_delay"]
STATE_FILE = f"{PROJECT_DIR}/state.json"
REPORT_FILE = f"{PROJECT_DIR}/report.txt"

# create STATE_FILE if it does not exist yet
if not os.path.isfile(STATE_FILE):
    with open(STATE_FILE, "w") as f:
        json.dump({"last_backoff_index": 0}, f)

# read last backoff index from STATE_FILE
with open(STATE_FILE) as f:
    config = json.load(f)
    backoff_index = config["last_backoff_index"]
    assert backoff_index in range(len(BACKOFF_TIMES))

# run the command and read the stdout
result = subprocess.run(JOB_COMMAND.split(), stdout=subprocess.PIPE)
stdout = result.stdout.decode()

# determine the next backoff time based on stdout
if backoff_index < len(BACKOFF_TIMES) - 1:
    backoff_index += 1
if SHORT_DELAY_KEYWORD in stdout:
    backoff_index = 0
elif LONG_DELAY_KEYWORD in stdout:
    backoff_index = len(BACKOFF_TIMES) - 1

# append timestamp + stdout to REPORT_FILE
with open(REPORT_FILE, "a") as f:
    f.write(str(datetime.now()) + "\n")
    f.write(stdout + "\n")

# save the state for the next execution
with open(STATE_FILE, "w") as f:
    json.dump({"last_backoff_index": backoff_index}, f)

# start next execution at "now + backoff time"
os.system(
    f'echo "python3 {PROJECT_DIR}/run.py" '
    + f"| at now + {BACKOFF_TIMES[backoff_index]}"
)
