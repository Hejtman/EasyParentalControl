import logging
import socket
import pickle

from server_communication import CommunicationProtocol
from configuration import ClientConfiguration


class ClientCommunication(CommunicationProtocol):
    def __init__(self, ip: str = CommunicationProtocol.ip, port: int = CommunicationProtocol.port):
        self.logger = logging.getLogger('Client')
        self.ip = ip
        self.port = port

    def sync_configuration(self, time_spend: int) -> ClientConfiguration:
        self.logger.debug(f'sending time_spend={time_spend} to server {self.ip}:{self.port}')
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.ip, self.port))

        s.send(pickle.dumps(time_spend, -1))
        raw_data = s.recv(1024)
        self.logger.debug(f'recieved ({len(raw_data)}): {raw_data}')

        config = pickle.loads(raw_data)
        self.logger.debug(f'recieved {config}')
        s.close()
        return config
