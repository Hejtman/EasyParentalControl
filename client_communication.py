import logging
import socket
import pickle

from server_communication import CommunicationProtocol
from configuration import ClientConfiguration


class ClientCommunication(CommunicationProtocol):
    def __init__(self, client_ip: str = CommunicationProtocol.server_ip, port: int = CommunicationProtocol.server_port):
        self.logger = logging.getLogger('Client')
        self.server_ip = client_ip
        self.server_port = port

    def sync_configuration(self, time_spend: int) -> ClientConfiguration:
        self.logger.debug(f'sending time_spend={time_spend} to server {self.server_ip}:{self.server_port}')
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((self.server_ip, self.server_port))
        except ConnectionRefusedError:
            return ClientConfiguration(client_ip='TODO', server_ip=self.server_ip, server_connected=False)

        s.send(pickle.dumps(time_spend, CommunicationProtocol.pickle_protocol))
        raw_data = s.recv(1024)
        self.logger.debug(f'received ({len(raw_data)}): {raw_data}')

        config = pickle.loads(raw_data)
        self.logger.debug(f'received {config}')
        s.close()
        return config
