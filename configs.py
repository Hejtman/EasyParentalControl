from datetime import date, datetime


class PersistentConfigs:
    persistent_storage = './clients_configs.txt'
    date_format = '%Y-%m-%d'

    def __init__(self):
        self.configs = self.load()

    def load(self) -> list:
        try:
            with open(self.persistent_storage) as f:
                sum_time_spend, date_record = f.read().splitlines()  # FIXME: dict with proper user selection
                date_record = datetime.strptime(date_record, self.date_format).date()
                if date_record != date.today():
                    return self._new_day_config()
            return [int(sum_time_spend), date_record]
        except FileNotFoundError:
            return self._new_day_config()

    def save(self) -> None:
        if self.configs[1] != date.today():
            self.configs = self._new_day_config()
        with open(self.persistent_storage, 'w') as f:
            f.write(f'{self.configs[0]}\n{self.configs[1]}')

    @staticmethod
    def _new_day_config() -> list:
        time_spent_today = 0
        return [time_spent_today, date.today()]
