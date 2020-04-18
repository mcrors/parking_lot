from abc import ABC, abstractmethod


class PriceCalc(ABC):

    @abstractmethod
    def calculate_price(self, start, end, tariff_type=None):
        pass

    @staticmethod
    def _get_duration_in_mins(start, end):
        duration = end - start
        return divmod(duration.total_seconds(), 60)[0]
