#!/usr/bin/env python3

import time
from pathlib import Path
from logger import TerminalLogger

from utils import OS
from server_api import ServerAPI
from configuration import ClientConfiguration


def warn_if_needed(configuration: ClientConfiguration) -> None:
    warn_if_needed.was_warned = False

    time_left = configuration.daily_limit - configuration.time_spend_today
    if time_left < configuration.warning_time and not warn_if_needed.was_warned:
        logger.info(f'⏰{time_left}')
        OS.pop_up(message=f'⏰ {time_left}')
        warn_if_needed.was_warned = True
    else:
        warn_if_needed.was_warned = False


def kill_if_needed(configuration: ClientConfiguration) -> None:
    if configuration.time_spend_today > configuration.daily_limit:
        logger.info(f'☠️{configuration.process}')
        OS.pop_up(message='☠️')
        OS.kill(process=configuration.process)


def main() -> None:
    server = ServerAPI(ip='192.168.1.1')  # FIXME: mv ip to client configuration

    configuration = server.retrieve_configuration(client=OS.get_user_name())
    while True:
        time.sleep(configuration.loop_time)

        if OS.is_running(process=configuration.process):
            server.report_use(time_spend=configuration.loop_time)

        configuration = server.retrieve_configuration(client=OS.get_user_name())
        logger.debug(f'spend/limit = {configuration.time_spend_today} / {configuration.daily_limit}')

        warn_if_needed(configuration)
        kill_if_needed(configuration)


if __name__ == '__main__':
    logger = TerminalLogger(file_path=f'{Path(Path.home(), Path(__file__).stem)}.log')
    logger.info(f'Started {60*"-"}')
    main()
