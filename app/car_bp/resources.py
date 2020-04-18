from datetime import datetime
from http import HTTPStatus
from flask import request, jsonify
from . import car_bp
from app.parked_car import ParkedCar
from app.parking_lot import ParkingLot
from app.errors import AddParameterError, generic_exception_response, MissingLocationError,InvalidLocationError, \
    ParkingLotError
from app.parking_lot_logger import logger


@car_bp.route('/add', methods=['GET'])
def add_car():
    try:
        logger.info(request)
        car = request.args.get('car')
        tariff = request.args.get('tariff')
        if not car or not tariff:
            raise AddParameterError

        parking_lot = ParkingLot()
        parked_car = ParkedCar(reg_num=car,
                               tariff=tariff,
                               location=parking_lot.get_next_location(),
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
    except ParkingLotError as e:
        logger.error(e.response)
        return jsonify(e.response), e.status_code
    except Exception as e:
        logger.error(e.args)
        return jsonify(generic_exception_response(e)), HTTPStatus.INTERNAL_SERVER_ERROR.value


@car_bp.route('/list', methods=['GET'])
def list_cars():
    try:
        logger.info(request)
        parking_lot = ParkingLot()
        cars = parking_lot.get_all_parked_cars()
        resp = {
            "status": "success",
            "cars": cars
        }
        logger.info(resp)
        return jsonify(resp)
    except Exception as e:
        logger.error(e.args)
        return jsonify(generic_exception_response(e)), HTTPStatus.INTERNAL_SERVER_ERROR.value


@car_bp.route('/remove', methods=['GET'])
def remove_cars():
    try:
        logger.info(request)
        car_location = request.args.get('location')
        if not car_location:
            error = MissingLocationError()
            logger.error(error.message)
            raise error
        if not car_location.isdigit():
            error = InvalidLocationError(car_location)
            logger.error(error.message)
            raise error
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
    except ParkingLotError as e:
        logger.error(e.status_code, e.response)
        return jsonify(e.response), e.status_code
    except Exception as e:
        logger.error(e.args)
        return jsonify(generic_exception_response(e)), HTTPStatus.INTERNAL_SERVER_ERROR.value
