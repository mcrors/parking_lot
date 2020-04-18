from http import HTTPStatus


def generic_exception_response(e):
    return {
        'status': 'Error',
        'message': e.args
    }


class ParkingLotError(Exception):

    def __init__(self, value=None):
        super().__init__()
        self.message = 'An unidentified error occured on the parking lot server'
        self.status_code = HTTPStatus.INTERNAL_SERVER_ERROR.value
        self.value = value

    @property
    def response(self):
        return {
            'status': 'error',
            'message': self.message
        }


class NonExistantLocationError(ParkingLotError):

    def __init__(self, value=None):
        super().__init__(value)
        self.message = f'The location {value} does not exist'
        self.status_code = HTTPStatus.BAD_REQUEST.value


class IncorrectLocationError(ParkingLotError):

    def __init__(self, value=None):
        super().__init__(value)
        self.message = f'Location {value} was not occupied'
        self.status_code = HTTPStatus.BAD_REQUEST.value


class ParkingLotFullError(ParkingLotError):
    def __init__(self, value=None):
        super().__init__(value)
        self.message = 'No free spaces'
        self.status_code = HTTPStatus.BAD_REQUEST.value


class CarAlreadyParkedError(ParkingLotError):

    def __init__(self, value=None):
        super().__init__(value)
        self.message = f'A car with the registration number {value} is already parked here'
        self.status_code = HTTPStatus.BAD_REQUEST.value


class TariffNotDefinedError(ParkingLotError):

    def __init__(self, value=None):
        super().__init__(value)
        self.message = f'The tariff type {value} is not available or does not exist'
        self.status_code = HTTPStatus.BAD_REQUEST.value


class AddParameterError(ParkingLotError):

    def __init__(self, value=None):
        super().__init__(value)
        self.message = 'You must supply both a car registration number and tariff'
        self.status_code = HTTPStatus.BAD_REQUEST.value


class MissingLocationError(ParkingLotError):

    def __init__(self, value=None):
        super().__init__(value)
        self.message = 'You must supply a location number'
        self.status_code = HTTPStatus.BAD_REQUEST.value


class InvalidLocationError(ParkingLotError):

    def __init__(self, value=None):
        super().__init__(value)
        self.message = f'Location value entered {value} is not an integer. You must supply an integer value'
        self.status_code = HTTPStatus.BAD_REQUEST.value
