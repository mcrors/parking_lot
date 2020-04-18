from datetime import datetime
from app.tariff_types.tariff_type import TariffType
from app.tariff_factory import TariffFactory
from app.errors import TariffNotDefinedError


class ParkedCar:

    def __init__(self, reg_num, tariff, location, start_time=datetime.now()):
        self.reg_num = reg_num
        self.tariff = tariff
        self.location = location
        self.start_time = start_time

    def __repr__(self):
        return str(self.details)

    @property
    def tariff(self):
        return self._tariff

    @tariff.setter
    def tariff(self, value):
        if not issubclass(type(value), TariffType):
            try:
                self._tariff = TariffFactory(value).get_tariff()
            except TariffNotDefinedError:
                raise TariffNotDefinedError(value)
        else:
            self._tariff = value

    @property
    def details(self):
        return {
                "car": self.reg_num,
                "tariff": self._tariff.name,
                "location": self.location,
                "start": self.start_time
                }
