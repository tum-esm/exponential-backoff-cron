# Exponential Backoff CRON

## What is it?

This repository contains a program that can be used as a deamon (https://en.wikipedia.org/wiki/Daemon_(computing)) to execute commands periodically - similar to `crontab`. However, when the next execution will start is determined from the output stream of the current execution of the command. Under the hood, it uses the `at` command (https://en.wikipedia.org/wiki/At_(command)), so it only works on Unix-like systems.
Author: Moritz Makowski, moritz.makowski@tum.de

<br/>
<br/>

## What does it do?

Here is an example of the `config.json` file:

```json
{
    "backoff_times": [
        "1 minutes",
        "4 minutes",
        "12 minutes",
        "2 hours",
        "24 hours"
    ],
    "job_command": "bash <do-something>",
    "keyword_for_short_delay": "started",
    "keyword_for_long_delay": "failed"
}
```

`job_command` is the shell command to be executed.

`backoff_times` are the times, the deamon waits until the next execution. Whenever the stoud-stream of the command execution contains the word "started", the next execution will be in 1 minute, for the word "failed" it will be in 24 hours. In any other case, the backoff time will increase from execution to exection until it stays at 24 hours.

Example usecase:

-   "started" = A new job with unknown execution time has been started -> restart delay-progress
-   "failed" = A job has failed (e.g. no data available) -> no point in retrying soon
-   in any other case = no job has ended or been started -> wait a little longer for the next retry

<br/>
<br/>

## How to set it up and run it?

1. Have Python `3.9^` installed in your system, only the standard library is being used

2. Use the file `config.example.json` to create a `config.json` file in your project directory for your setup

3. Run `python3 <project-dir>/run.py` to start the deamon
