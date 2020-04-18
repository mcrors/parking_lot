from app.parking_lot import ParkingLot


class TestAddCarShould:

    @staticmethod
    def test_return_success_response(client):
        data = {
            'car': '12345',
            'tariff': 'hourly'
        }
        response = client.get('add', query_string=data)
        assert response.status_code == 200
        response_dict = response.get_json()
        assert response_dict['car'] == '12345'
        assert response_dict['tariff'] == 'hourly'
        assert response_dict['status'] == 'success'

    @staticmethod
    def test_adds_car_to_parking_lot(client, empty_parking_lot):
        data = {
            'car': '12345',
            'tariff': 'hourly'
        }
        client.get('add', query_string=data)
        assert len(empty_parking_lot) == 1
        car = empty_parking_lot.parking_spaces[0].car
        assert car.reg_num == '12345'
        assert empty_parking_lot.free_locations == [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

    @staticmethod
    def test_returns_error_when_parameters_are_missing(client):
        resp = client.get('add')
        assert resp.status_code == 400
        assert resp.get_json()['status'] == 'error'

        resp = client.get('add', query_string={'car': '12345'})
        assert resp.status_code == 400
        assert resp.get_json()['status'] == 'error'

        resp = client.get('add', query_string={'tariff': 'hourly'})
        assert resp.status_code == 400
        assert resp.get_json()['status'] == 'error'

    @staticmethod
    def test_returns_error_when_parking_lot_is_already_full(client, full_car_park):
        data = {
            'car': '12345',
            'tariff': 'hourly'
        }
        resp = client.get('add', query_string=data)
        assert resp.status_code == 400
        assert resp.get_json()['status'] == 'error'
        assert resp.get_json()['message'] == 'No free spaces'


class TestRemoveCarShould:

    @staticmethod
    def test_lowers_number_of_cars_in_parking_lot(client, full_car_park):
        assert len(full_car_park) == 12
        data = {
            'location': '1'
        }
        client.get('remove', query_string=data)
        assert len(full_car_park) == 11
        assert full_car_park.free_locations == [1]

    def test_gets_correct_car(self, client, empty_parking_lot):
        assert len(empty_parking_lot) == 0
        data = {
            'car': '12345',
            'tariff': 'hourly'
        }
        client.get('add', query_string=data)
        response = client.get('remove', query_string={'location': '1'})
        response_dict = response.get_json()
        assert response_dict['car'] == '12345'

    @staticmethod
    def test_returns_error_when_no_location_is_provided(client):
        resp = client.get('remove')
        assert resp.status_code == 400
        assert resp.get_json()['status'] == 'error'
        assert 'must supply a location' in resp.get_json()['message']

    @staticmethod
    def test_returns_error_when_string_is_entered_for_location(client):
        resp = client.get('remove', query_string={'location': 'hi'})
        assert resp.status_code == 400
        assert resp.get_json()['status'] == 'error'
        assert "hi is not an integer" in resp.get_json()['message']

    @staticmethod
    def test_returns_error_when_wrong_location_is_entered(client, empty_parking_lot):
        non_existing_location = empty_parking_lot.NUM_OF_SPACES + 1
        resp = client.get('remove', query_string={'location': f'{non_existing_location}'})
        assert resp.status_code == 400
        assert resp.get_json()['status'] == 'error'
        assert f'The location {non_existing_location} does not exist' in resp.get_json()['message']

    @staticmethod
    def test_returns_error_when_free_location_is_entered(client, empty_parking_lot):
        resp = client.get('remove', query_string={'location': '1'})
        assert resp.status_code == 400
        assert resp.get_json()['status'] == 'error'
        assert resp.get_json()['message'] == 'Location 1 was not occupied'


class TestListCarsShould:

    @staticmethod
    def test_returns_correct_list_of_cars(client, full_car_park):
        resp = client.get('list')
        assert resp.status_code == 200
        parked_cars = resp.get_json()['cars']
        assert len(parked_cars) == 12
