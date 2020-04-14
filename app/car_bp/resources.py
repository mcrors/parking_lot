from datetime import datetime
from flask import request, jsonify
from . import car_bp
from app.parked_car import ParkedCar
from app.parking_lot import ParkingLot
from app.errors import AddParameterError, CarAlreadyParkedError, ParkingLotFullError, TariffNotDefinedError, \
    generic_exception_response, RemoveParameterError, IncorrectLocationError, NonExistantLocationError


@car_bp.route('/add', methods=['GET'])
def add_car():
    car = request.args.get('car')
    tariff = request.args.get('tariff')
    try:
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
        return jsonify(resp)
    except (AddParameterError, CarAlreadyParkedError, ParkingLotFullError, TariffNotDefinedError) as e:
        return jsonify(e.response), e.status_code
    except Exception as e:
        return jsonify(generic_exception_response(e)), 500


@car_bp.route('/list', methods=['GET'])
def list_cars():
    try:
        parking_lot = ParkingLot()
        cars = []
        for parked_car in parking_lot.parked_cars:
            cars.append(parked_car.details)
        ret_value = {
            "status": "success",
            "cars": cars
        }
        return jsonify(ret_value)
    except Exception as e:
        return jsonify(generic_exception_response(e)), 500


@car_bp.route('/remove', methods=['GET'])
def remove_cars():
    try:
        car_location = request.args.get('location')
        if not car_location or not car_location.isdigit():
            raise RemoveParameterError
        parking_lot = ParkingLot()
        parked_car = parking_lot.remove_car(car_location)
        ret_value = {
            "status": "success",
            "car": parked_car.reg_num,
            "tariff": parked_car.tariff.name,
            "location": parked_car.location,
            "start": parked_car.start_time,
            "finish": datetime.now(),
            "fee": parked_car.tariff.calculate_price(parked_car.start_time, datetime.now())
        }
        return jsonify(ret_value)
    except (RemoveParameterError, IncorrectLocationError, NonExistantLocationError) as e:
        return jsonify(e.response), 400
    except Exception as e:
        return jsonify(generic_exception_response(e)), 500
