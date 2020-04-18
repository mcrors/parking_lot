from datetime import datetime
from http import HTTPStatus
from flask import request, jsonify
from . import car_bp
from app.parked_car import ParkedCar
from app.parking_lot import ParkingLot
from app.errors import AddParameterError, generic_exception_response, MissingLocationError,InvalidLocationError, \
    ParkingLotError
from app.parking_lot_logger import logger
from .utils import exception_handler


@car_bp.route('/add', methods=['GET'])
@exception_handler
def add_car():
    logger.info(request)
    car = request.args.get('car')
    tariff = request.args.get('tariff')
    if not car or not tariff:
        raise AddParameterError

    parking_lot = ParkingLot()
    parked_car = ParkedCar(reg_num=car,
                           tariff=tariff,
                           location=None,
                           start_time=datetime.now())
    parking_lot.add_car(parked_car)
    resp = {
        "status": "success",
        "car": parked_car.reg_num,
        "tariff": parked_car.tariff.name,
        "location": parked_car.location,
        "start": parked_car.start_time
    }
    logger.info(resp)
    return jsonify(resp)


@car_bp.route('/list', methods=['GET'])
@exception_handler
def list_cars():
    logger.info(request)
    parking_lot = ParkingLot()
    cars = parking_lot.get_all_parked_cars()
    resp = {
        "status": "success",
        "cars": cars
    }
    logger.info(resp)
    return jsonify(resp)


@car_bp.route('/remove', methods=['GET'])
@exception_handler
def remove_cars():
    logger.info(request)
    car_location = request.args.get('location')
    if not car_location:
        raise MissingLocationError()
    if not car_location.isdigit():
        raise InvalidLocationError(car_location)
    parking_lot = ParkingLot()
    parked_car = parking_lot.remove_car(car_location)
    logger.info(parked_car)
    resp = {
        "status": "success",
        "car": parked_car.reg_num,
        "tariff": parked_car.tariff.name,
        "location": parked_car.location,
        "start": parked_car.start_time,
        "finish": datetime.now(),
        "fee": parked_car.tariff.calculate_price(parked_car.start_time, datetime.now())
    }
    logger.info(resp)
    return jsonify(resp)
