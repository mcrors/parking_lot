from .tariff_type import TariffType


class HourlyTariff(TariffType):
    name = 'hourly'
    
    @property
    def mins_per_duration_segment(self):
        super().mins_per_duration_segment
        return 60

    @property
    def price_per_duration_segment(self):
        super().price_per_duration_segment
        return 2

    @property
    def num_of_free_mins(self):
        super().num_of_free_mins
        return 15

    def calculate_price(self, start, end):
        return super(HourlyTariff, self).calculate_price(start, end)
