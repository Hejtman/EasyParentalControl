from dataclasses import dataclass
from datetime import date


@dataclass
class ClientConfiguration:
    ip: str
    user: str = ''                      # custom user identification
    process: str = 'chromium-browse'    # process to detect and block when time limit is reached
    daily_limit: int = 2*3600           # granted seconds of daily use of process (2h)
    time_spend_today: int = 0           # already used seconds
    warning_time: int = 20*60           # warn about kill seconds ahead (20min)
    loop_time: int = 60                 # seconds between each loop (time spend count, config retrieval, process killing)
    date_recorded: date = date.today()  # date of this record (not today > reset to default for today)

    @property
    def time_left_sec(self) -> int:
        return self.daily_limit - self.time_spend_today

    @property
    def time_left_min(self) -> int:
        return int(self.time_left_sec/60)

    def validate(self) -> None:
        today = date.today()
        if self.date_recorded != today:
            self.date_recorded = today
            self.time_spend_today = 0
