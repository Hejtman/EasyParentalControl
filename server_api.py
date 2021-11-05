import logging

from configuration import ClientConfiguration


# TODO: make server communication protocol by ABC

class ServerAPI:

    def __init__(self, ip):
        self.logger = logging.getLogger(__name__)
        self.ip = ip

    def sync_configuration(self, client:str, time_spend: int) -> ClientConfiguration:   # FIXME: mv to server
        self.logger.info(f'Reporting {time_spend}s of use.')

        sum_time_spend = ServerAPI.get_client_config(client)

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
