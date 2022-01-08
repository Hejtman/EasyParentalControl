import logging
import pickle
import socketserver

from configs import PersistentConfigs

from configuration import ClientConfiguration
from communication_protocol import CommunicationProtocol


# TODO file logger
class ConfigSyncHandler(socketserver.BaseRequestHandler, CommunicationProtocol):
    configs = PersistentConfigs()

    def __init__(self, request, client_address, server):
        self.logger = logging.getLogger('ConfigSyncHandler')
        self.logger.debug(f'__init__: {client_address}')
        socketserver.BaseRequestHandler.__init__(self, request, client_address, server)
        self.timeout = 10

    def handle(self):
        self.request.send(pickle.dumps(
            self.sync_configuration(time_spend=pickle.loads(self.request.recv(64).strip()))
        ))

    def sync_configuration(self, time_spend: int) -> ClientConfiguration:
        client_ip = self.client_address[0]
        self.logger.info(f'time_spend received from {client_ip}: {time_spend} {type(time_spend)}')
        self.configs[client_ip].validate()
        self.configs[client_ip].time_left_today -= time_spend
        self.configs[client_ip].time_spend_today += time_spend
        self.configs.save()
        self.logger.info(f'sending back {client_ip}: {self.configs[client_ip]}')
        return self.configs[client_ip]
