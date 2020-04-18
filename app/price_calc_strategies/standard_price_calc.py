from app.parking_lot_logger import logger
from .price_calc import PriceCalc


class StandardPriceCalc(PriceCalc):

    def calculate_price(self, start, end, tariff_type):
        logger.debug(f'Calculating price. start: {start}. end: {end}')
        parked_minutes = self._get_duration_in_mins(start, end) - tariff_type.num_of_free_mins
        if parked_minutes % tariff_type.mins_per_duration_segment == 0:
            return (parked_minutes / tariff_type.mins_per_duration_segment) * tariff_type.price_per_duration_segment
        return ((parked_minutes // tariff_type.mins_per_duration_segment) + 1) * tariff_type.price_per_duration_segment
