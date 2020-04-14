from datetime import datetime
import pytest
from app.parked_car import ParkedCar
from app.parking_lot import ParkingLot
from parking_lot import create_app


@pytest.fixture()
def empty_parking_lot():
    parking_lot = ParkingLot()
    parking_lot.empty_parking_lot()
    return parking_lot


@pytest.fixture()
def non_empty_parking_lot(empty_parking_lot):
    c1 = ParkedCar('123456', 'hourly', 1)
    empty_parking_lot.add_car(c1)
    return empty_parking_lot


@pytest.fixture()
def full_car_park(empty_parking_lot):
    for i in range(empty_parking_lot.NUM_OF_SPACES):
        car = ParkedCar(f'car_{i}', 'hourly', i+1)
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
