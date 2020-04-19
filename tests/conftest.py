import logging
import pytest
from app.cars import ParkedCar, Car
from app.parking_lot import ParkingLot
from parking_lot import create_app


@pytest.fixture(autouse=True)
def set_logging_level():
    logging.basicConfig(filename='test.log', level=logging.DEBUG)
    yield


@pytest.fixture()
def empty_parking_lot():
    parking_lot = ParkingLot()
    parking_lot.empty_parking_lot()
    return parking_lot


@pytest.fixture()
def non_empty_parking_lot(empty_parking_lot):
    c1 = Car('123456', 'hourly')
    empty_parking_lot.add_car(c1)
    return empty_parking_lot


@pytest.fixture()
def full_car_park(empty_parking_lot):
    for i in range(empty_parking_lot.NUM_OF_SPACES):
        car = Car(f'car_{i}', 'hourly')
        empty_parking_lot.add_car(car)
    return empty_parking_lot


@pytest.fixture()
def client():
    app = create_app('test')
    app_cntxt = app.app_context()
    app_cntxt.push()
    test_client = app.test_client()
    yield test_client
    app_cntxt.pop()
