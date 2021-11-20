from abc import ABC, abstractmethod
from configuration import ClientConfiguration


class CommunicationProtocol(ABC):
    server_ip = '192.168.1.1'
    server_port = 9999

    @abstractmethod
    def sync_configuration(self, time_spend: int) -> ClientConfiguration:
        pass
