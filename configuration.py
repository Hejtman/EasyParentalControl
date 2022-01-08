import logging

from dataclasses import dataclass
from datetime import date


@dataclass
class ClientConfiguration:
    client_ip: str
    server_ip: str
    user: str = ''                      # custom user identification
    server_connected: bool = False      # client will show whether has connection with server or not
    process: str = 'chromium-browse'    # process to detect and block when time limit is reached
    daily_limit: int = 2*3600           # granted seconds of daily use of process (2h)
    time_spend_today: int = 0           # already used seconds
    time_left_today: int = daily_limit  # time left to spend
    warning_time: int = 20*60           # warn about kill seconds ahead (20min)
    loop_time: int = 60                 # seconds between each loop (time spend count, config retrieval, process killing)
    date_recorded: date = date.today()  # date of this record (not today > reset to default for today)

    @property
    def time_left_min(self) -> int:
        return int(self.time_left_today/60)

    @property
    def daily_limit_min(self) -> int:
        return int(self.daily_limit/60)

    def validate(self) -> None:
        today = date.today()
        if self.date_recorded == today:
            logging.debug(f'config valid: ({self.date_recorded} == {today})')
        else:
            self.date_recorded = today
            self.time_spend_today = 0
            self.time_left_today = self.daily_limit
            logging.debug(f'config old: ({self.date_recorded} != {today}) - re-setting limits')
