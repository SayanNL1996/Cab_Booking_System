"""Test caess for employee file."""

import mock
from employee import Employee
from datetime import datetime, timedelta

routes_data = [(1510, 111, 'sarjapur', 'whitefield', '11:30:00', 3),
               (1511, 111, 'hsr', 'sarjapur', '10:30:00', 4)]

bookings_data = [(1021, 1211, 1510, '2020-05-25', '21:36:00', 2, 1, 'UK 07 AQ 5678', 1510, 111, 'hsr',
                  'sarjapur', '10:00:00', 2),
                 (1022, 1211, 1511, '2020-05-20', '11:06:00', 1, 0, 'UK 07 QQ 6780', 1511, 111, 'hsr',
                  'sarjapur', '10:00:00', 2),
                 (1023, 1211, 1514, '2020-05-15', '14:12:00', 4, 2, 'UK 07 AW 8178', 1514, 112, 'hsr',
                  'sarjapur', '10:00:00', 2)]


class TestEmployee:

    @mock.patch('employee.Employee.new_booking')
    @mock.patch('employee.input')
    def test_admin_menu_choice_1(self, inputs, arg1):
        """ Test employee menu method."""
        arg1.return_value = True
        inputs.side_effect = ['1', '4']

        assert Employee(object).employee_menu('test@gmail.com') is True

    @mock.patch('employee.Employee.past_bookings')
    @mock.patch('employee.input')
    def test_admin_menu_choice_2(self, inputs, arg1):
        """ Test employee menu method."""
        arg1.return_value = True
        inputs.side_effect = ['2', '4']

        assert Employee(object).employee_menu('test@gmail.com') is True

    @mock.patch('employee.Employee.upcoming_bookings')
    @mock.patch('employee.input')
    def test_admin_menu_choice_3(self, inputs, arg1):
        """ Test employee menu method."""
        arg1.return_value = True
        inputs.side_effect = ['3', '4']

        assert Employee(object).employee_menu('test@gmail.com') is True

    @mock.patch('employee.input')
    def test_admin_menu_wrong_choice(self, inputs):
        """ Test employee menu method."""
        inputs.side_effect = ['8', '4']

        assert Employee(object).employee_menu('test@gmail.com') is True

    @mock.patch('employee.Employee.validate_route_id')
    @mock.patch('employee.Employee.new_booking_action')
    @mock.patch('mysql.connector.connect')
    @mock.patch('employee.input')
    def test_new_booking_success(self, inputs, mocksql, arg1, arg2):
        """ Test new booking method."""
        arg1.return_value = True
        arg2.return_value = True
        inputs.side_effect = ['source', 'destination', '9:00', 2, 1511]
        sqlite_execute_mock = mock.Mock()
        mocksql.cursor.return_value = sqlite_execute_mock
        sqlite_execute_mock.execute.return_value = sqlite_execute_mock
        sqlite_execute_mock.fetchall.return_value = routes_data

        assert Employee(mocksql).new_booking('test@gmail.com') is True

    @mock.patch('mysql.connector.connect')
    @mock.patch('employee.input')
    def test_new_booking_failure_no_cabs(self, inputs, mocksql):
        """ Test new booking method."""
        inputs.side_effect = ['source', 'destination', '9:00', 2, 1511]
        sqlite_execute_mock = mock.Mock()
        mocksql.cursor.return_value = sqlite_execute_mock
        sqlite_execute_mock.execute.return_value = sqlite_execute_mock
        sqlite_execute_mock.fetchall.return_value = []

        assert Employee(mocksql).new_booking('test@gmail.com') is False

    @mock.patch('mysql.connector.connect')
    @mock.patch('employee.input')
    def test_new_booking_failure_mysql_error(self, inputs, mocksql):
        """ Test new booking method."""
        inputs.side_effect = ['source', 'destination', '9:00', 2, 1511]
        mocksql.cursor.side_effect = Exception

        assert Employee(mocksql).new_booking('test@gmail.com') is False

    @mock.patch('mysql.connector.connect')
    def test_validate_route_id_success(self, mocksql):
        """ Test validate route id method."""
        sqlite_execute_mock = mock.Mock()
        mocksql.cursor.return_value = sqlite_execute_mock
        sqlite_execute_mock.execute.return_value = sqlite_execute_mock
        sqlite_execute_mock.fetchone.return_value = routes_data[0]

        assert Employee(mocksql).validate_route_id(1211) is True

    @mock.patch('mysql.connector.connect')
    def test_validate_route_id_failure(self, mocksql):
        """ Test validate route id method."""
        sqlite_execute_mock = mock.Mock()
        mocksql.cursor.return_value = sqlite_execute_mock
        sqlite_execute_mock.execute.return_value = sqlite_execute_mock
        sqlite_execute_mock.fetchone.return_value = ''

        assert Employee(mocksql).validate_route_id(1211) is False

    @mock.patch('mysql.connector.connect')
    def test_validate_route_id_failure_mysql_error(self, mocksql):
        """ Test validate route id method."""
        mocksql.cursor.side_effect = Exception

        assert Employee(mocksql).validate_route_id(1211) is False

    @mock.patch('mysql.connector.connect')
    @mock.patch('employee.input')
    def test_new_booking_action_success(self, inputs, mocksql):
        """ Test new booking action method."""
        inputs.side_effect = ['y']
        sqlite_execute_mock = mock.Mock()
        mocksql.cursor.return_value = sqlite_execute_mock
        sqlite_execute_mock.execute.return_value = sqlite_execute_mock
        sqlite_execute_mock.fetchone.return_value = [101]

        assert Employee(mocksql).new_booking_action(1211, 4, 'email@xyz.in') is True

    @mock.patch('mysql.connector.connect')
    @mock.patch('employee.input')
    def test_new_booking_action_failure_mysql_error(self, inputs, mocksql):
        """ Test new booking action method."""
        inputs.side_effect = ['y']
        mocksql.cursor.side_effect = Exception

        assert Employee(mocksql).new_booking_action(1211, 2, 'email@xyz.in') is None

    @mock.patch('employee.input')
    def test_new_booking_action_failure_action_abort(self, inputs):
        """ Test new booking action method."""
        inputs.side_effect = ['n']

        assert Employee(object).new_booking_action(1211, 4, 'email@xyz.in') is False

    @mock.patch('mysql.connector.connect')
    def test_past_bookings_success(self, mocksql):
        """ Test past bookings method."""
        sqlite_execute_mock = mock.Mock()
        mocksql.cursor.return_value = sqlite_execute_mock
        sqlite_execute_mock.execute.return_value = sqlite_execute_mock
        sqlite_execute_mock.fetchall.return_value = bookings_data

        assert Employee(mocksql).past_bookings('email@xyz.in') is True

    @mock.patch('mysql.connector.connect')
    def test_past_bookings_failure_no_data(self, mocksql):
        """ Test past bookings method."""
        sqlite_execute_mock = mock.Mock()
        mocksql.cursor.return_value = sqlite_execute_mock
        sqlite_execute_mock.execute.return_value = sqlite_execute_mock
        sqlite_execute_mock.fetchall.return_value = []

        assert Employee(mocksql).past_bookings('email@xyz.in') is False

    @mock.patch('mysql.connector.connect')
    def test_past_bookings_failure_mysql_error(self, mocksql):
        """ Test past bookings method."""
        mocksql.cursor.side_effect = Exception

        assert Employee(mocksql).past_bookings('email@xyz.in') is False

    @mock.patch('employee.Employee.validate_booking_id')
    @mock.patch('employee.Employee.cancel_booking')
    @mock.patch('mysql.connector.connect')
    @mock.patch('employee.input')
    def test_upcoming_bookings_success(self, inputs, mocksql, arg1, arg2):
        """ Test upcoming bookings method."""
        arg1.return_value = True
        arg2.return_value = True
        inputs.side_effect = [1222]
        sqlite_execute_mock = mock.Mock()
        mocksql.cursor.return_value = sqlite_execute_mock
        sqlite_execute_mock.execute.return_value = sqlite_execute_mock
        sqlite_execute_mock.fetchall.return_value = bookings_data

        assert Employee(mocksql).upcoming_bookings('email@xyz.in') is True

    @mock.patch('mysql.connector.connect')
    def test_upcoming_bookings_failure_no_data(self, mocksql):
        """ Test upcoming bookings method."""
        sqlite_execute_mock = mock.Mock()
        mocksql.cursor.return_value = sqlite_execute_mock
        sqlite_execute_mock.execute.return_value = sqlite_execute_mock
        sqlite_execute_mock.fetchall.return_value = []

        assert Employee(mocksql).upcoming_bookings('email@xyz.in') is False

    @mock.patch('mysql.connector.connect')
    def test_upcoming_bookings_failure_mysql_error(self, mocksql):
        """ Test upcoming bookings method."""
        mocksql.cursor.side_effect = Exception

        assert Employee(mocksql).upcoming_bookings('email@xyz.in') is False

    @mock.patch('mysql.connector.connect')
    def test_validate_booking_id_success(self, mocksql):
        """ Test validate booking id method."""
        sqlite_execute_mock = mock.Mock()
        mocksql.cursor.return_value = sqlite_execute_mock
        sqlite_execute_mock.execute.return_value = sqlite_execute_mock
        sqlite_execute_mock.fetchone.return_value = routes_data[0]

        assert Employee(mocksql).validate_booking_id(1211) is True

    @mock.patch('mysql.connector.connect')
    def test_validate_booking_id_failure(self, mocksql):
        """ Test validate booking id method."""
        sqlite_execute_mock = mock.Mock()
        mocksql.cursor.return_value = sqlite_execute_mock
        sqlite_execute_mock.execute.return_value = sqlite_execute_mock
        sqlite_execute_mock.fetchone.return_value = ''

        assert Employee(mocksql).validate_booking_id(1211) is False

    @mock.patch('mysql.connector.connect')
    def test_validate_booking_id_failure_mysql_error(self, mocksql):
        """ Test validate booking id method."""
        mocksql.cursor.side_effect = Exception

        assert Employee(mocksql).validate_booking_id(1211) is False

    @mock.patch('mysql.connector.connect')
    @mock.patch('employee.input')
    def test_cancel_booking_success(self, inputs, mocksql):
        """ Test validate booking id method."""
        inputs.side_effect = ['y']
        t = datetime.strptime("20:20:25", "%H:%M:%S")
        delta = timedelta(hours=t.hour, minutes=t.minute, seconds=t.second)
        sqlite_execute_mock = mock.Mock()
        mocksql.cursor.return_value = sqlite_execute_mock
        sqlite_execute_mock.execute.return_value = sqlite_execute_mock
        sqlite_execute_mock.fetchone.side_effect = [[delta], [2322, 3]]

        assert Employee(mocksql).cancel_booking(1211) is True

    @mock.patch('mysql.connector.connect')
    @mock.patch('employee.input')
    def test_cancel_booking_failure_canoot_cancel(self, inputs, mocksql):
        """ Test validate booking id method."""
        inputs.side_effect = ['y']
        t = datetime.strptime("05:20:25", "%H:%M:%S")
        delta = timedelta(hours=t.hour, minutes=t.minute, seconds=t.second)
        sqlite_execute_mock = mock.Mock()
        mocksql.cursor.return_value = sqlite_execute_mock
        sqlite_execute_mock.execute.return_value = sqlite_execute_mock
        sqlite_execute_mock.fetchone.side_effect = [[delta], [2322, 3]]

        assert Employee(mocksql).cancel_booking(1211) is False

    @mock.patch('mysql.connector.connect')
    @mock.patch('employee.input')
    def test_cancel_booking_failure_mysql_error(self, inputs, mocksql):
        """ Test validate booking id method."""
        inputs.side_effect = ['y']
        mocksql.cursor.side_effect = Exception

        assert Employee(mocksql).cancel_booking(1211) is False

    @mock.patch('employee.input')
    def test_cancel_booking_failure_action_abort(self, inputs):
        """ Test validate booking id method."""
        inputs.side_effect = ['n']

        assert Employee(object).cancel_booking(1211) is False
