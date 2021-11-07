import pickle
from datetime import date

from configuration import ClientConfiguration


class PersistentConfigs:
    persistent_storage = './clients_configs.txt'
    date_format = '%Y-%m-%d'

    def __init__(self):
        self.configs = self.load()

    def load(self) -> ClientConfiguration:
        try:
            with open(self.persistent_storage, 'rb') as f:
                configs = pickle.load(f)
                if configs.date_recorded != date.today():
                    configs = self._new_day_config()
        except FileNotFoundError:
            configs = self._new_day_config()
        return configs

    def save(self) -> None:
        if self.configs.date_recorded != date.today():
            self.configs = self._new_day_config()
        with open(self.persistent_storage, 'wb') as f:
            pickle.dump(self.configs, f, protocol=0)

    @staticmethod
    def _new_day_config() -> ClientConfiguration:
        return ClientConfiguration(user='D')
