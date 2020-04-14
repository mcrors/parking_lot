from .tariff_type import TariffType


class DailyTariff(TariffType):
    name = 'daily'

    @property
    def mins_per_duration_segment(self):
        return 1440

    @property
    def price_per_duration_segment(self):
        return 20

    @property
    def num_of_free_mins(self):
        return 15

    def calculate_price(self, start, end):
        return super(DailyTariff, self).calculate_price(start, end)
