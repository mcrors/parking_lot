from datetime import datetime
from http import HTTPStatus
from flask import request, jsonify
from . import car_bp
from app.cars import ParkedCar, Car
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
    car = Car(reg_num=car, tariff=tariff)
    resp = parking_lot.add_car(car)
    logger.info(resp)
    return jsonify(resp)


@car_bp.route('/list', methods=['GET'])
@exception_handler
def list_cars():
    logger.info(request)
    parking_lot = ParkingLot()
    resp = parking_lot.get_all_parked_cars()
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
    resp = parking_lot.remove_car(car_location)
    logger.info(resp)
    return jsonify(resp)
