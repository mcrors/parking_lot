from abc import ABC, abstractmethod


class TariffType(ABC):

    def __init__(self):
        super().__init__()

    @abstractmethod
    def calculate_price(self, start, end):
        parked_minutes = self.get_duration_in_mins(start, end) - self.num_of_free_mins
        if parked_minutes % self.mins_per_duration_segment == 0:
            return (parked_minutes / self.mins_per_duration_segment) * self.price_per_duration_segment
        return ((parked_minutes // self.mins_per_duration_segment) + 1) * self.price_per_duration_segment

    def __repr__(self):
        return str({
            'name': self.name,
        })

    @property
    @classmethod
    @abstractmethod
    def name(cls):
        pass

    @property
    @abstractmethod
    def mins_per_duration_segment(self):
        pass

    @property
    @abstractmethod
    def price_per_duration_segment(self):
        pass

    @property
    @abstractmethod
    def num_of_free_mins(self):
        pass

    @staticmethod
    def get_duration_in_mins(start, end):
        duration = end - start
        return divmod(duration.total_seconds(), 60)[0]
