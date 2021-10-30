from configuration import ClientConfiguration


class ServerAPI:
    def __init__(self, ip):
        self.ip = ip
        self.server_side_client_configuration = ClientConfiguration(user='D')       # FIXME: mv to server

    def report_use(self, time_spend: int) -> None:
        self.server_side_client_configuration.time_spend_today += time_spend        # FIXME: mv to server

    def retrieve_configuration(self, client:str) -> ClientConfiguration:
        return self.server_side_client_configuration                                # FIXME: mv to server
