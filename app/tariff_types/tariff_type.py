from abc import ABC, abstractmethod
from app.price_calc_strategies.standard_price_calc import StandardPriceCalc
from app.parking_lot_logger import logger


class TariffType(ABC):

    def __init__(self, price_calc=None):
        super().__init__()
        if not price_calc:
            self.price_calc = StandardPriceCalc()
        else:
            self.price_calc = price_calc

    @abstractmethod
    def calculate_price(self, start, end):
        return self.price_calc.calculate_price(start, end, self)

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
        logger.debug(f'Getting {self.name} mins per duration segment')

    @property
    @abstractmethod
    def price_per_duration_segment(self):
        logger.debug(f'Getting {self.name} price per durarion segment')

    @property
    @abstractmethod
    def num_of_free_mins(self):
        logger.debug(f'Getting {self.name} num of free minutes')

    @staticmethod
    def get_duration_in_mins(start, end):
        duration = end - start
        return divmod(duration.total_seconds(), 60)[0]
