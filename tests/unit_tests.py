import os
from datetime import datetime
import pytest
from app.cars import ParkedCar, Car
from app.parking_lot import ParkingLot
from app.errors import ParkingLotFullError, TariffNotDefinedError, IncorrectLocationError, CarAlreadyParkedError
from app.tariff_factory import TariffFactory
from app.tariff_types.hourly_tariff import HourlyTariff
from app.tariff_types.daily_tariff import DailyTariff


class TestParkingLotShould:

    def test_only_one_parking_lot_exists(self):
        pl1 = ParkingLot()
        pl2 = ParkingLot()
        assert pl1 is pl2

    def test_parking_lot_has_correct_number_of_spaces(self):
        parking_lot = ParkingLot()
        assert len(parking_lot.parking_spaces) == parking_lot.NUM_OF_SPACES

    def test_empty_parking_lot_frees_up_all_locations(self, non_empty_parking_lot):
        assert len(non_empty_parking_lot) == 1
        non_empty_parking_lot.empty_parking_lot()
        assert len(non_empty_parking_lot) == 0

    def test_add_car_to_parking_lot(self, empty_parking_lot):
        car = Car('123456', 'hourly')
        empty_parking_lot.add_car(car)
        assert len(empty_parking_lot) == 1

    def test_remove_car_from_parking_lot(self, empty_parking_lot):
        car = Car('123456', 'hourly')
        parked_car = empty_parking_lot.add_car(car)
        assert len(empty_parking_lot) == 1
        empty_parking_lot.remove_car(1)
        assert len(empty_parking_lot) == 0

    def test_get_available_location_supplies_lowest_possible_location_num(self, empty_parking_lot):
        location_1 = empty_parking_lot.get_next_location()
        assert location_1 == 1
        car_1 = Car('123456', 'hourly')
        parked_car_1 = empty_parking_lot.add_car(car_1)
        location_2 = empty_parking_lot.get_next_location()
        assert location_2 == 2
        car_2 = Car('123457', 'hourly')
        empty_parking_lot.add_car(car_2)
        empty_parking_lot.remove_car(1)
        result = empty_parking_lot.get_next_location()
        expected = 1
        assert result == expected

    def test_raises_error_when_parking_lot_is_full(self, full_car_park):
        with pytest.raises(ParkingLotFullError):
            car = Car('123456', 'hourly')
            full_car_park.add_car(car)

    @staticmethod
    def test_second_call_to_parking_lot_does_not_reset_data(non_empty_parking_lot):
        expected_size = len(non_empty_parking_lot)
        my_parking_lot = ParkingLot()
        assert my_parking_lot is non_empty_parking_lot
        assert len(my_parking_lot) == expected_size

    @staticmethod
    def test_return_the_correct_car(empty_parking_lot):
        car = Car('12345', 'hourly')
        parked_car = empty_parking_lot.add_car(car=car)
        returned_car = empty_parking_lot.remove_car(1)
        assert parked_car["car"] is returned_car["car"]

    @staticmethod
    def test_raises_error_for_non_existing_car(empty_parking_lot):
        with pytest.raises(IncorrectLocationError):
            empty_parking_lot.remove_car(1)

    @staticmethod
    def test_know_which_locations_are_available(empty_parking_lot):
        assert [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12] == empty_parking_lot.free_locations
        car_1 = Car('12345', 'hourly')
        car_2 = Car('12346', 'hourly')
        car_3 = Car('12347', 'hourly')
        car_4 = Car('12348', 'hourly')
        car_5 = Car('12349', 'hourly')
        empty_parking_lot.add_car(car_1)
        empty_parking_lot.add_car(car_2)
        empty_parking_lot.add_car(car_3)
        empty_parking_lot.add_car(car_4)
        empty_parking_lot.add_car(car_5)
        result = empty_parking_lot.free_locations
        expected = [6, 7, 8, 9, 10, 11, 12]
        assert result == expected

        empty_parking_lot.remove_car(3)
        result = empty_parking_lot.free_locations
        expected = [3, 6, 7, 8, 9, 10, 11, 12]
        assert result == expected

    @staticmethod
    def test_len_returns_the_number_of_cars_in_the_parking_lot(full_car_park):
        assert len(full_car_park) == 12
        full_car_park.remove_car(1)
        assert len(full_car_park) == 11

    @staticmethod
    def test_cant_add_the_same_car_twice(empty_parking_lot):
        car1 = Car(reg_num="12345", tariff='hourly')
        empty_parking_lot.add_car(car1)
        with pytest.raises(CarAlreadyParkedError):
            empty_parking_lot.add_car(car1)

    @staticmethod
    def test_knows_if_a_car_is_already_parked(empty_parking_lot):
        car = Car(reg_num="12345", tariff='hourly')
        result = empty_parking_lot._car_already_parked(car)
        assert result is False
        empty_parking_lot.add_car(car)
        result = empty_parking_lot._car_already_parked(car)
        assert result is True
        car_2 = Car(reg_num="12343", tariff='hourly')
        result = empty_parking_lot._car_already_parked(car_2)
        assert result is False


class TestParkedCarShould:

    @staticmethod
    def test_details_returns_correct_dict():
        car = Car('123456', 'hourly')
        parked_car = ParkedCar(car, 1)
        assert isinstance(parked_car.details, dict)

        expected = ['car', 'tariff', 'location', 'start']
        result = list(parked_car.details.keys())
        assert expected == result


class TestCarShould:

    @staticmethod
    def test_does_not_allow_initialization_with_incorrect_tariff_type():
        with pytest.raises(TariffNotDefinedError):
            Car('123456', 'something')

    @staticmethod
    def test_accept_tariffs_as_objects_or_strings():
        car_1 = Car('123456', 'hourly')
        daily_tariff = TariffFactory('DAILY').get_tariff()
        car_2 = Car('123457', daily_tariff)
        assert car_1.tariff.name == 'hourly'
        assert car_2.tariff.name == 'daily'


class TestTariffFactoryShould:

    @staticmethod
    def test_does_not_attempt_import_for_dirs_or_inits():
        factory = TariffFactory('hourly')
        test_dir = os.getcwd()
        result = factory._is_dir_or_init(test_dir)
        assert result is True

        test_init = os.path.join(test_dir, '__init__.py')
        result = factory._is_dir_or_init(test_init)
        assert result is True

        test_module = os.path.join(test_dir, __name__)
        result = factory._is_dir_or_init(test_module)
        assert result is False

    @staticmethod
    def test_gets_correct_class():
        factory = TariffFactory('hourly')
        mods = factory._load_modules()
        klass = factory._get_class_by_name_attr(mods)
        assert klass is HourlyTariff

    @staticmethod
    def test_raises_error_for_non_defined_tariff():
        factory = TariffFactory('something_completely_different')
        mods = factory._load_modules()
        with pytest.raises(TariffNotDefinedError):
            factory._get_class_by_name_attr(mods)
        with pytest.raises(TariffNotDefinedError):
            factory.get_tariff()

    @staticmethod
    def test_returns_correct_instance():
        factory = TariffFactory('hourly')
        tariff = factory.get_tariff()
        assert isinstance(tariff, HourlyTariff)


class TestTariffTypeShould:

    @staticmethod
    def test_get_correct_duration_of_stay_in_minutes():
        hourly_tariff = HourlyTariff()
        start = datetime(2020, 4, 11, 12)
        end = datetime(2020, 4, 11, 13)
        result = hourly_tariff.get_duration_in_mins(start, end)
        assert result == 60
        daily_tariff = DailyTariff()
        start = datetime(2020, 4, 11, 12)
        end = datetime(2020, 4, 12, 13)
        result = daily_tariff.get_duration_in_mins(start, end)
        assert result == 1500

    @staticmethod
    def test_all_tariffs_have_correct_name():
        assert HourlyTariff.name == 'hourly'
        assert DailyTariff.name == 'daily'

    @staticmethod
    @pytest.mark.parametrize('start, end, expected', [
        (datetime(2020, 4, 11, 12), datetime(2020, 4, 11, 13), 2),
        (datetime(2020, 4, 11, 12), datetime(2020, 4, 11, 13, 10), 2),
        (datetime(2020, 4, 11, 12), datetime(2020, 4, 11, 13, 16), 4),
    ])
    def test_calculates_correct_price_for_hourly(start, end, expected):
        hourly_tariff = HourlyTariff()
        result = hourly_tariff.calculate_price(start, end)
        assert result == expected

    @staticmethod
    @pytest.mark.parametrize('start, end, expected', [
        (datetime(2020, 4, 11, 12), datetime(2020, 4, 12, 12), 20),
        (datetime(2020, 4, 11, 12), datetime(2020, 4, 12, 13), 40),
        (datetime(2020, 4, 11, 12), datetime(2020, 4, 11, 13, 16), 20),
    ])
    def test_calculates_correct_price_for_daily(start, end, expected):
        daily_tariff = DailyTariff()
        result = daily_tariff.calculate_price(start, end)
        assert result == expected

    @staticmethod
    def test_allow_15_mins_free_time():
        hourly_tariff = HourlyTariff()
        start = datetime(2020, 4, 11, 12, 5)
        end = datetime(2020, 4, 11, 12, 20)
        result = hourly_tariff.calculate_price(start, end)
        assert result == 0

        daily_tariff = DailyTariff()
        start = datetime(2020, 4, 11, 12, 5)
        end = datetime(2020, 4, 11, 12, 20)
        result = daily_tariff.calculate_price(start, end)
        assert result == 0


class TestLocationShould:

    @staticmethod
    def test_available_is_true_for_empty_location():
        location = ParkingLot.Location(1)
        assert location.available is True

    @staticmethod
    def test_available_is_false_for_occupied_location(non_empty_parking_lot):
        print(non_empty_parking_lot.parking_spaces[0])
        assert non_empty_parking_lot.parking_spaces[0].available is False


class TestCar:

    @staticmethod
    def test_details_contains_correct_attributes():
        pass