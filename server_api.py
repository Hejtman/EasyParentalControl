import logging
from datetime import datetime
from pathlib import Path

from configuration import ClientConfiguration


# TODO: make server communication protocol by ABC

class ServerAPI:
    persistent_storage = f'{Path.home()}/persistent.txt'  # FIXME: mv to server
    date_format = '%Y-%m-%d 00:00:00'

    def __init__(self, ip):
        self.logger = logging.getLogger(__name__)
        self.ip = ip
        self.server_side_client_configuration = ClientConfiguration(user='D')           # FIXME: mv to server

    @staticmethod
    def _today() -> datetime:                                                           # FIXME: mv to server
        return datetime.strptime(datetime.now().strftime(ServerAPI.date_format), ServerAPI.date_format)

    @staticmethod                                                                       # FIXME: mv to server
    def _new_day_record() -> tuple:
        return 0, ServerAPI._today()

    @staticmethod                                                                       # FIXME: mv to server
    def _read_persistent_config() -> tuple:
        try:
            with open(ServerAPI.persistent_storage) as f:
                sum_time_spend, date_record = f.read().splitlines()
            return int(sum_time_spend), datetime.strptime(date_record, ServerAPI.date_format)
        except FileNotFoundError:
            return ServerAPI._new_day_record()

    def sync_configuration(self, client:str, time_spend: int) -> ClientConfiguration:   # FIXME: mv to server
        self.logger.info(f'Reporting {time_spend}s of use.')

        sum_time_spend, date_record = ServerAPI._read_persistent_config()
        if date_record != ServerAPI._today():
            sum_time_spend, date_record = ServerAPI._new_day_record()

        self.server_side_client_configuration.time_spend_today = sum_time_spend + time_spend

        with open(self.persistent_storage, 'w') as f:
            f.write(f'{self.server_side_client_configuration.time_spend_today}\n{date_record}')

        return self.server_side_client_configuration


# just UNIT TESTs
if __name__ == '__main__':
    server = ServerAPI('192.168.1.1')
    print(server.sync_configuration(client='D', time_spend=60))
    print(server.sync_configuration(client='D', time_spend=60))
    print(server.sync_configuration(client='D', time_spend=60))
