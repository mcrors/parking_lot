from functools import wraps
from http import HTTPStatus
from flask import jsonify
from app.parking_lot_logger import logger
from app.errors import ParkingLotError, generic_exception_response


def exception_handler(view_func):
    @wraps(view_func)
    def wrapper(*pargs, **kwargs):
        try:
            return view_func(*pargs, *kwargs)
        except ParkingLotError as e:
            logger.error(e.response)
            return jsonify(e.response), e.status_code
        except Exception as e:
            logger.error(e.args)
            return jsonify(generic_exception_response(e)), HTTPStatus.INTERNAL_SERVER_ERROR.value
    return wrapper
