from datetime import datetime
from app.parking_lot_logger import logger
from app.cars import ParkedCar
from app.errors import IncorrectLocationError, ParkingLotFullError, CarAlreadyParkedError, \
    NonExistantLocationError


class ParkingLot:
    __instance = None
    NUM_OF_SPACES = 12
    parking_spaces = []

    class Location:

        def __init__(self, location_num):
            self.location_num = location_num
            self.car = None

        def __repr__(self):
            return f"Location: location_num->{self.location_num}, car->{self.car}"

        @property
        def available(self):
            return self.car is None

        def assign(self, car):
            self.car = car

        def unassign(self):
            self.car = None

    def __new__(cls):
        if ParkingLot.__instance is None:
            logger.debug("Creating new Parking Lot")
            ParkingLot.__instance = object.__new__(cls)
            cls.parking_spaces = [ParkingLot.Location(i + 1) for i in range(cls.NUM_OF_SPACES)]
        return ParkingLot.__instance

    def __str__(self):
        return f'Total Spaces: {self.NUM_OF_SPACES}\n' + \
               f'Remaining Spaces: {self.NUM_OF_SPACES - len(self.parking_spaces)}\n' + \
               f'Parking Spaces: {self.parking_spaces}'

    def __len__(self):
        return self.NUM_OF_SPACES - len(self.free_locations)

    def get_all_parked_cars(self):
        return {"status": "success",
                "cars": [location.car.details
                         for location in self.parking_spaces
                         if not location.available]
                }

    def add_car(self, car):
        logger.info(f"Adding car {car.reg_num}")
        if not self.free_locations:
            raise ParkingLotFullError
        if self._car_already_parked(car):
            raise CarAlreadyParkedError(car.reg_num)
        self.get_next_location()
        parked_car = ParkedCar(car, self.get_next_location())
        self.parking_spaces[parked_car.location-1].assign(parked_car)
        logger.info(f"Car {car.reg_num} added to location {parked_car.location}")
        return {
            "status": "success",
            "car": parked_car.reg_num,
            "tariff": parked_car.tariff.name,
            "location": parked_car.location,
            "start": parked_car.start_time
        }

    def remove_car(self, location_num):
        logger.info(f"Removing car from location {location_num}")
        location_num = int(location_num)
        if location_num > self.NUM_OF_SPACES:
            raise NonExistantLocationError(location_num)
        car = self.parking_spaces[location_num - 1].car
        if car is None:
            raise IncorrectLocationError(location_num)
        self.parking_spaces[location_num - 1].unassign()
        logger.info(f"car {car} removed from location {self.parking_spaces[location_num - 1]}")
        resp = {
            "status": "success",
            "car": car.reg_num,
            "tariff": car.tariff.name,
            "location": car.location,
            "start": car.start_time,
            "finish": datetime.now(),
            "fee": car.tariff.calculate_price(car.start_time, datetime.now())
        }
        return resp

    def get_next_location(self):
        try:
            logger.debug("Getting next location")
            return min(self.free_locations)
        except ValueError:
            raise ParkingLotFullError

    def empty_parking_lot(self):
        logger.debug("Emptying the parking lot")
        for location in self.parking_spaces:
            location.unassign()

    @property
    def free_locations(self):
        return [location.location_num for location in self.parking_spaces if location.available]

    def _car_already_parked(self, car):
        return any([location.car.reg_num == car.reg_num for location in self.parking_spaces
                    if location.car])
