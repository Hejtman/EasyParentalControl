from abc import ABC, abstractmethod
from configuration import ClientConfiguration

DEBUG = False


class CommunicationProtocol(ABC):
    server_ip = '127.0.0.1' if DEBUG else '192.168.1.1'
    server_port = 9999
    pickle_protocol = 0  # FIXME: set to -1 when client/server both on python 3.10

    @abstractmethod
    def sync_configuration(self, time_spend: int) -> ClientConfiguration:
        pass
