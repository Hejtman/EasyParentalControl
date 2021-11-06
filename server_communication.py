import logging
import pickle
import socketserver

from configs import PersistentConfigs
from abc import ABC, abstractmethod

from configuration import ClientConfiguration


class CommunicationProtocol(ABC):
    @abstractmethod
    def sync_configuration(self, time_spend: int) -> ClientConfiguration:
        pass


# TODO file logger
class ConfigSyncHandler(socketserver.BaseRequestHandler, CommunicationProtocol):
    configs = PersistentConfigs()

    def __init__(self, request, client_address, server):
        self.logger = logging.getLogger('ConfigSyncHandler')
        self.logger.debug(f'__init__: {client_address}')
        socketserver.BaseRequestHandler.__init__(self, request, client_address, server)

    def handle(self):
        self.request.send(pickle.dumps(
            self.sync_configuration(time_spend=pickle.loads(self.request.recv(64).strip()))
        ))

    def sync_configuration(self, time_spend: int) -> ClientConfiguration:
        # TODO: self.client_address[0] > client
        self.logger.info(f'time_spend received from {self.client_address[0]}: {time_spend} {type(time_spend)}')
        self.configs.configs[0] += time_spend
        self.configs.save()
        self.logger.info(f'sending back {self.client_address[0]}: {self.configs.configs}')
        return self.configs.configs
