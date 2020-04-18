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
        self.status = 'Fatel'

    @property
    def response(self):
        return {
            'status': self.status,
            'message': self.message
        }


class ParkingLotBadRequestError(ParkingLotError):

    def __init__(self, value=None):
        super().__init__(value)
        self.status = 'error'
        self.status_code = HTTPStatus.BAD_REQUEST.value


class NonExistantLocationError(ParkingLotBadRequestError):

    def __init__(self, value=None):
        super().__init__(value)
        self.message = f'The location {value} does not exist'


class IncorrectLocationError(ParkingLotBadRequestError):

    def __init__(self, value=None):
        super().__init__(value)
        self.message = f'Location {value} was not occupied'


class ParkingLotFullError(ParkingLotBadRequestError):
    def __init__(self, value=None):
        super().__init__(value)
        self.message = 'No free spaces'


class CarAlreadyParkedError(ParkingLotBadRequestError):

    def __init__(self, value=None):
        super().__init__(value)
        self.message = f'A car with the registration number {value} is already parked here'


class TariffNotDefinedError(ParkingLotBadRequestError):

    def __init__(self, value=None):
        super().__init__(value)
        self.message = f'The tariff type {value} is not available or does not exist'


class AddParameterError(ParkingLotBadRequestError):

    def __init__(self, value=None):
        super().__init__(value)
        self.message = 'You must supply both a car registration number and tariff'


class MissingLocationError(ParkingLotBadRequestError):

    def __init__(self, value=None):
        super().__init__(value)
        self.message = 'You must supply a location number'


class InvalidLocationError(ParkingLotBadRequestError):

    def __init__(self, value=None):
        super().__init__(value)
        self.message = f'Location value entered {value} is not an integer. You must supply an integer value'
