def generic_exception_response(e):
    return {
        'status': 'Error',
        'message': e.args
    }


class ParkingLotError(Exception):

    def __init__(self):
        super().__init__()
        self.message = 'An unidentified error occured on the parking lot server'
        self.status_code = 500

    @property
    def response(self):
        return {
            'status': 'error',
            'message': self.message
        }


class NonExistantLocationError(ParkingLotError):

    def __init__(self):
        super().__init__()
        self.message = 'The location entered does not exist'
        self.status_code = 400


class IncorrectLocationError(ParkingLotError):

    def __init__(self):
        super().__init__()
        self.message = 'Location entered was not occupied'
        self.status_code = 400


class ParkingLotFullError(ParkingLotError):
    def __init__(self):
        super().__init__()
        self.message = 'No free spaces'
        self.status_code = 400


class CarAlreadyParkedError(ParkingLotError):

    def __init__(self):
        super().__init__()
        self.message = 'A car with that registration number is already parked here'
        self.status_code = 400


class TariffNotDefinedError(ParkingLotError):

    def __init__(self):
        super().__init__()
        self.message = 'The tariff type supplied is not available or does not exist'
        self.status_code = 400


class AddParameterError(ParkingLotError):

    def __init__(self):
        super().__init__()
        self.message = 'You must supply both a car registration number and tariff'
        self.status_code = 400


class RemoveParameterError(ParkingLotError):

    def __init__(self):
        super().__init__()
        self.message = 'You must supply a location in the form of a number'
        self.status_code = 400
