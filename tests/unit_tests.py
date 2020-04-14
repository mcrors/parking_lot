import os
from datetime import datetime
import pytest
from app.parked_car import ParkedCar
from app.parking_lot import ParkingLot
from app.errors import ParkingLotFullError, TariffNotDefinedError, IncorrectLocationError
from app.tariff_factory import TariffFactory
from app.tariff_types.hourly_tariff import HourlyTariff
from app.tariff_types.daily_tariff import DailyTariff


class TestParkingLotShould:

    def test_only_one_parking_lot_exists(self):
        pl1 = ParkingLot()
        pl2 = ParkingLot()
        assert pl1 is pl2

    def test_empty_parking_lot_frees_up_all_locations(self, non_empty_parking_lot):
        assert len(non_empty_parking_lot.parked_cars) == 1
        non_empty_parking_lot.empty_parking_lot()
        assert len(non_empty_parking_lot) == 0

    def test_add_car_to_parking_lot(self, empty_parking_lot):
        parked_car = ParkedCar('123456', 'hourly', 1)
        empty_parking_lot.add_car(parked_car)
        assert len(empty_parking_lot) == 1

    def test_remove_car_from_parking_lot(self, empty_parking_lot):
        parked_car = ParkedCar('123456', 'hourly', 1)
        empty_parking_lot.add_car(parked_car)
        assert len(empty_parking_lot) == 1
        empty_parking_lot.remove_car(parked_car.location)
        assert len(empty_parking_lot) == 0

    def test_get_available_location_supplies_lowest_possible_location_num(self, empty_parking_lot):
        location_1 = empty_parking_lot.get_next_location()
        assert location_1 == 1
        parked_car_1 = ParkedCar('123456', 'hourly', location_1)
        empty_parking_lot.add_car(parked_car_1)
        location_2 = empty_parking_lot.get_next_location()
        assert location_2 == 2
        parked_car_2 = ParkedCar('123457', 'hourly', location_2)
        empty_parking_lot.add_car(parked_car_2)
        empty_parking_lot.remove_car(parked_car_1.location)
        result = empty_parking_lot.get_next_location()
        expected = 1
        assert result == expected

    def test_raises_error_when_parking_lot_is_full(self, full_car_park):
        with pytest.raises(ParkingLotFullError):
            parked_car = ParkedCar('123456', 'hourly', 13)
            full_car_park.add_car(parked_car)

    def test_second_call_to_parking_lot_does_not_reset_data(self, non_empty_parking_lot):
        expected_size = len(non_empty_parking_lot)
        my_parking_lot = ParkingLot()
        assert my_parking_lot is non_empty_parking_lot
        assert len(my_parking_lot) == expected_size

    def test_return_the_correct_car(self, empty_parking_lot):
        car = ParkedCar('12345', 'hourly', empty_parking_lot.get_next_location())
        empty_parking_lot.add_car(parked_car=car)
        returned_car = empty_parking_lot.remove_car(car.location)
        assert car is returned_car

    def test_raises_error_for_non_existing_car(self, empty_parking_lot):
        with pytest.raises(IncorrectLocationError):
            empty_parking_lot.remove_car(1)

    def test_know_which_locations_are_available(self, empty_parking_lot):
        assert [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12] == empty_parking_lot.free_locations
        car_1 = ParkedCar('12345', 'hourly', 1)
        car_2 = ParkedCar('12346', 'hourly', 2)
        car_3 = ParkedCar('12347', 'hourly', 3)
        car_4 = ParkedCar('12348', 'hourly', 4)
        car_5 = ParkedCar('12349', 'hourly', 5)
        empty_parking_lot.add_car(car_1)
        empty_parking_lot.add_car(car_2)
        empty_parking_lot.add_car(car_3)
        empty_parking_lot.add_car(car_4)
        empty_parking_lot.add_car(car_5)
        result = empty_parking_lot.free_locations
        expected = [6, 7, 8, 9, 10, 11, 12]
        assert result == expected

        empty_parking_lot.remove_car(car_3.location)
        result = empty_parking_lot.free_locations
        expected = [3, 6, 7, 8, 9, 10, 11, 12]
        assert result == expected


class TestParkedCarShould:

    def test_details_returns_correct_dict(self):
        parked_car = ParkedCar('123456', 'hourly', 1)
        assert isinstance(parked_car.details, dict)

        expected = ['car', 'tariff', 'location', 'start']
        result = list(parked_car.details.keys())
        assert expected == result

    def test_does_not_allow_initialization_with_incorrect_tariff_type(self):
        with pytest.raises(TariffNotDefinedError):
            ParkedCar('123456', 'something', 1)

    def test_accept_tariffs_as_objects_or_strings(self):
        car_1 = ParkedCar('123456', 'hourly', 1)
        daily_tariff = TariffFactory('DAILY').get_tariff()
        car_2 = ParkedCar('123457', daily_tariff, 2)
        assert car_1.tariff.name == 'hourly'
        assert car_2.tariff.name == 'daily'


class TestTariffFactoryShould:

    def test_does_not_attempt_import_for_dirs_or_inits(self):
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

    def test_gets_correct_class(self):
        factory = TariffFactory('hourly')
        mods = factory._load_modules()
        klass = factory._get_class_by_name_attr(mods)
        assert klass is HourlyTariff

    def test_raises_error_for_non_defined_tariff(self):
        factory = TariffFactory('something_completely_different')
        mods = factory._load_modules()
        with pytest.raises(TariffNotDefinedError):
            factory._get_class_by_name_attr(mods)
        with pytest.raises(TariffNotDefinedError):
            factory.get_tariff()

    def test_returns_correct_instance(self):
        factory = TariffFactory('hourly')
        tariff = factory.get_tariff()
        assert isinstance(tariff, HourlyTariff)


class TestTariffTypeShould:

    def test_get_correct_duration_of_stay_in_minutes(self):
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

    def test_all_tariffs_have_correct_name(self):
        assert HourlyTariff.name == 'hourly'
        assert DailyTariff.name == 'daily'

    @pytest.mark.parametrize('start, end, expected', [
        (datetime(2020, 4, 11, 12), datetime(2020, 4, 11, 13), 2),
        (datetime(2020, 4, 11, 12), datetime(2020, 4, 11, 13, 10), 2),
        (datetime(2020, 4, 11, 12), datetime(2020, 4, 11, 13, 16), 4),
    ])
    def test_calculates_correct_price_for_hourly(self, start, end, expected):
        hourly_tariff = HourlyTariff()
        result = hourly_tariff.calculate_price(start, end)
        assert result == expected

    @pytest.mark.parametrize('start, end, expected', [
        (datetime(2020, 4, 11, 12), datetime(2020, 4, 12, 12), 20),
        (datetime(2020, 4, 11, 12), datetime(2020, 4, 12, 13), 40),
        (datetime(2020, 4, 11, 12), datetime(2020, 4, 11, 13, 16), 20),
    ])
    def test_calculates_correct_price_for_daily(self, start, end, expected):
        daily_tariff = DailyTariff()
        result = daily_tariff.calculate_price(start, end)
        assert result == expected

    def test_allow_15_mins_free_time(self):
        hourly_tariff = HourlyTariff()
        start = datetime(2020, 4, 11, 12, 5)
        end = datetime(2020, 4, 11, 12, 20)
        result = hourly_tariff.calculate_price(start, end)
        assert result == 0

        daily_tariff = DailyTariff()
        start = datetime(2020, 4, 11, 12, 5)
        end = datetime(2020, 4, 11, 12, 20)
        result = hourly_tariff.calculate_price(start, end)
        assert result == 0
