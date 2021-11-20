import pickle

from communication_protocol import CommunicationProtocol
from configuration import ClientConfiguration


class PersistentConfigs:
    """Handles server side loading/saving configuration of connected clients."""
    persistent_storage = './clients_configs.txt'
    date_format = '%Y-%m-%d'

    def __init__(self):
        self.configs = []
        self.load()

    def __getitem__(self, client_ip) -> ClientConfiguration:
        for c in self.configs:
            if c.client_ip == client_ip:
                return c

        # default conf for unknown (new) client
        c = ClientConfiguration(client_ip=client_ip, server_ip=CommunicationProtocol.server_ip, server_connected=True)
        self.configs.append(c)
        return c

    def load(self) -> None:
        try:
            with open(self.persistent_storage, 'rb') as f:
                self.configs = pickle.load(f)
        except FileNotFoundError:
            pass

    def save(self) -> None:
        with open(self.persistent_storage, 'wb') as f:
            pickle.dump(self.configs, f, protocol=0)
