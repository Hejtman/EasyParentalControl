import socket
import pickle

from logger import TerminalLogger
from server_communication import CommunicationProtocol
from configuration import ClientConfiguration


class ClientCommunication(CommunicationProtocol):
    def __init__(self, ip: str, port: int):
        self.logger = TerminalLogger(file_path=__file__.replace('py', 'log'))  # FIXME: log to project dir
        self.ip = ip
        self.port = port

    def sync_configuration(self, time_spend: int) -> ClientConfiguration:
        self.logger.debug(f'sending time_spend={time_spend} to server {self.ip}:{self.port}')
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.ip, self.port))

        s.send(pickle.dumps(time_spend, -1))
        config = pickle.loads(s.recv(1024))

        self.logger.debug(f'recieved {config}')
        s.close()
        return config
