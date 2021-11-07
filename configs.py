import pickle

from configuration import ClientConfiguration


class PersistentConfigs:
    persistent_storage = './clients_configs.txt'
    date_format = '%Y-%m-%d'

    def __init__(self):
        self.configs = []
        self.load()

    def __getitem__(self, ip) -> ClientConfiguration:
        for c in self.configs:
            if c.ip == ip:
                return c
        c = ClientConfiguration(ip=ip)
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
