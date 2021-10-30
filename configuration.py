from dataclasses import dataclass


@dataclass
class ClientConfiguration:
    user: str
    process: str = 'chromium-browse'    # process to detect and block when time limit is reached
    daily_limit: int = 2*3600           # granted seconds of daily use of process (2h)
    time_spend_today: int = 0           # already used seconds
    warning_time: int = 20*60           # warn about kill seconds ahead (20min)
    loop_time: int = 60                 # seconds between each loop (time spend count, config retrieval, process killing)
