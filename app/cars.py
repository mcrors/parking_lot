from datetime import datetime
import inspect
from app.tariff_types.tariff_type import TariffType
from app.tariff_factory import TariffFactory
from app.errors import TariffNotDefinedError


class Car:

    def __init__(self, reg_num, tariff):
        self.reg_num = reg_num
        self.tariff = tariff

    @property
    def tariff(self):
        return self._tariff

    @tariff.setter
    def tariff(self, value):
        if not issubclass(type(value), TariffType):
            try:
                self._tariff = TariffFactory(value).get_tariff()
            except TariffNotDefinedError:
                raise
        else:
            self._tariff = value


class ParkedCar(Car):

    def __init__(self, car, location, start_time=datetime.now()):
        super().__init__(car.reg_num, car.tariff)
        self.location = location
        self.start_time = start_time

    def __repr__(self):
        return str(self.details)

    @property
    def details(self):
        return {
                "car": self.reg_num,
                "tariff": self._tariff.name,
                "location": self.location,
                "start": self.start_time
                }
