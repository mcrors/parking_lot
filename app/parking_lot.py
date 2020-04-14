from app.errors import IncorrectLocationError, ParkingLotFullError, CarAlreadyParkedError, \
    NonExistantLocationError


class ParkingLot:
    __instance = None
    NUM_OF_SPACES = 12
    parked_cars = []

    def __new__(cls):
        if ParkingLot.__instance is None:
            ParkingLot.__instance = object.__new__(cls)
        return ParkingLot.__instance

    def __str__(self):
        return f'Total Spaces: {self.NUM_OF_SPACES}\n' + \
               f'Remaining Spaces: {self.NUM_OF_SPACES - len(self.parked_cars)}\n' + \
               f'Parked Cars: {self.parked_cars}'

    def __len__(self):
        return len(self.parked_cars)

    def add_car(self, parked_car):
        if len(self.parked_cars) >= self.NUM_OF_SPACES:
            raise ParkingLotFullError
        for car in self.parked_cars:
            if car.reg_num == parked_car.reg_num:
                raise CarAlreadyParkedError
        self.parked_cars.append(parked_car)

    def remove_car(self, location):
        if int(location) > self.NUM_OF_SPACES:
            raise NonExistantLocationError
        found_car = None
        for car in self.parked_cars:
            if car.location == int(location):
                found_car = car
                break
        if found_car is None:
            raise IncorrectLocationError
        self.parked_cars.remove(found_car)
        return found_car

    def get_next_location(self):
        try:
            return min(self.free_locations)
        except ValueError:
            raise ParkingLotFullError

    def empty_parking_lot(self):
        self.parked_cars = []

    @property
    def free_locations(self):
        location_list = []
        for i in range(self.NUM_OF_SPACES):
            location_list.append(i+1)
        if len(self.parked_cars) == 0:
            return location_list
        for car in self.parked_cars:
            location_list.remove(car.location)
        return location_list
