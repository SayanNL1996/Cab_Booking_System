""" Test cases for admin file."""

import mock
from admin import Admin

members = [(132, 'fname', 'lname', 'email', '9898989765'),
           (133, 'fname', 'lname', 'email', '9898989765'),
           (134, 'fname', 'lname', 'email', '9898989765')]

cabs_data = [(111, 'UK 07 AW 2323', 'Shubham Bhatt', 7676878789, 4),
             (112, 'UK 07 AW 2333', 'Ramesh Bhatt', 7676877789, 6),
             (113, 'UK 07 AW 2363', 'John Mishra', 7676878389, 4)]

employee_booking_data = [(1021, 1211, 1510, '2020-05-25', '21:36:00', 2, 1, 'UK 07 AQ 5678', 1510, 111, 'hsr',
                         'sarjapur', '10:00:00', 2),
                         (1022, 1211, 1511, '2020-05-20', '11:06:00', 1, 0, 'UK 07 QQ 6780', 1511, 111, 'hsr',
                          'sarjapur', '10:00:00', 2),
                         (1023, 1211, 1514, '2020-05-15', '14:12:00', 4, 2, 'UK 07 AW 8178', 1514, 112, 'hsr',
                          'sarjapur', '10:00:00', 2)]


class TestAdmin:

    @mock.patch('admin.Admin.admin_employees_menu')
    @mock.patch('admin.input')
    def test_admin_menu_choice_1(self, inputs, arg1):
        """ Test admin menu method."""
        arg1.return_value = True
        inputs.side_effect = ['1', '5']

        assert Admin(object).admin_menu('test@gmail.com') is True

    @mock.patch('admin.Admin.admin_cabs_menu')
    @mock.patch('admin.input')
    def test_admin_menu_choice_2(self, inputs, arg1):
        """ Test admin menu method."""
        arg1.return_value = True
        inputs.side_effect = ['2', '5']

        assert Admin(object).admin_menu('test@gmail.com') is True

    @mock.patch('admin.Admin.employee_bookings')
    @mock.patch('admin.input')
    def test_admin_menu_choice_3(self, inputs, arg1):
        """ Test admin menu method."""
        arg1.return_value = True
        inputs.side_effect = ['3', '5']

        assert Admin(object).admin_menu('test@gmail.com') is True

    @mock.patch('admin.Admin.bookings_for_dates')
    @mock.patch('admin.input')
    def test_admin_menu_choice_4(self, inputs, arg1):
        """ Test admin menu method."""
        arg1.return_value = True
        inputs.side_effect = ['4', '5']

        assert Admin(object).admin_menu('test@gmail.com') is True

    @mock.patch('admin.input')
    def test_admin_menu_wrong_choice(self, inputs):
        """ Test admin menu method."""
        inputs.side_effect = ['8', '5']

        assert Admin(object).admin_menu('test@gmail.com') is True

    @mock.patch('admin.Admin.add_employee')
    @mock.patch('admin.input')
    def test_admin_employees_menu_choice_1(self, inputs, arg1):
        """ Test admin member menu method."""
        arg1.return_value = True
        inputs.side_effect = ['1', '5']

        assert Admin(object).admin_employees_menu() is True

    @mock.patch('admin.Admin.update_employee')
    @mock.patch('admin.input')
    def test_admin_employees_menu_choice_2(self, inputs, arg1):
        """ Test admin member menu method."""
        arg1.return_value = True
        inputs.side_effect = ['2', '5']

        assert Admin(object).admin_employees_menu() is True

    @mock.patch('admin.Admin.delete_employee')
    @mock.patch('admin.input')
    def test_admin_employees_menu_choice_3(self, inputs, arg1):
        """ Test admin member menu method."""
        arg1.return_value = True
        inputs.side_effect = ['3', '5']

        assert Admin(object).admin_employees_menu() is True

    @mock.patch('admin.Admin.show_employees')
    @mock.patch('admin.input')
    def test_admin_employees_menu_choice_4(self, inputs, arg1):
        """ Test admin member menu method."""
        arg1.return_value = True
        inputs.side_effect = ['4', '5']

        assert Admin(object).admin_employees_menu() is True

    @mock.patch('admin.input')
    def test_admin_employees_menu_wrong_choice(self, inputs):
        """ Test admin member menu method."""
        inputs.side_effect = ['9', '5']

        assert Admin(object).admin_employees_menu() is True

    @mock.patch('admin.Admin.add_employee_action')
    @mock.patch('admin.input')
    def test_add_employee_success(self, inputs, arg1):
        arg1.return_value = True
        inputs.side_effect = ['fname', 'lname', 'test@xyz.in', 9876567687]

        assert Admin(object).add_employee() is True

    @mock.patch('admin.input')
    def test_add_employee_invalid_email(self, inputs):
        inputs.side_effect = ['fname', 'lname', 'testz.in', 9876567687]

        assert Admin(object).add_employee() is False

    @mock.patch('mysql.connector.connect')
    def test_add_employee_action_success(self, mocksql):
        sqlite_execute_mock = mock.Mock()
        mocksql.cursor.return_value = sqlite_execute_mock
        sqlite_execute_mock.execute.return_value = sqlite_execute_mock
        sqlite_execute_mock.fetchone.return_value = [0]

        assert Admin(mocksql).add_employee_action('fname', 'lname', 'test@xyz.in', '9879879876') is True

    @mock.patch('mysql.connector.connect')
    def test_add_employee_action_failure_invalid_phone(self, mocksql):
        sqlite_execute_mock = mock.Mock()
        mocksql.cursor.return_value = sqlite_execute_mock
        sqlite_execute_mock.execute.return_value = sqlite_execute_mock
        sqlite_execute_mock.fetchone.return_value = [0]

        assert Admin(mocksql).add_employee_action('fname', 'lname', 'test@xyz.in', '987987976') is False

    @mock.patch('mysql.connector.connect')
    def test_add_employee_action_failure_invalid_last_name(self, mocksql):
        sqlite_execute_mock = mock.Mock()
        mocksql.cursor.return_value = sqlite_execute_mock
        sqlite_execute_mock.execute.return_value = sqlite_execute_mock
        sqlite_execute_mock.fetchone.return_value = [0]

        assert Admin(mocksql).add_employee_action('fname', 'lnam8e', 'test@xyz.in', '987987976') is False

    @mock.patch('mysql.connector.connect')
    def test_add_employee_action_failure_invalid_first_name(self, mocksql):
        sqlite_execute_mock = mock.Mock()
        mocksql.cursor.return_value = sqlite_execute_mock
        sqlite_execute_mock.execute.return_value = sqlite_execute_mock
        sqlite_execute_mock.fetchone.return_value = [0]

        assert Admin(mocksql).add_employee_action('fn5ame', 'lname', 'test@xyz.in', '987987976') is False

    @mock.patch('mysql.connector.connect')
    def test_add_employee_action_failure_email_exist(self, mocksql):
        sqlite_execute_mock = mock.Mock()
        mocksql.cursor.return_value = sqlite_execute_mock
        sqlite_execute_mock.execute.return_value = sqlite_execute_mock
        sqlite_execute_mock.fetchone.return_value = [1]

        assert Admin(mocksql).add_employee_action('fname', 'lname', 'test@xyz.in', '987987976') is False

    @mock.patch('mysql.connector.connect')
    def test_add_employee_action_failure_mysql_error(self, mocksql):
        mocksql.cursor.side_effect = Exception

        assert Admin(mocksql).add_employee_action('fname', 'lname', 'test@xyz.in', '9879879576') is False

    @mock.patch('admin.Admin.update_member_validation')
    @mock.patch('mysql.connector.connect')
    @mock.patch('admin.input')
    def test_update_employee_success(self, inputs, mocksql, arg1):
        arg1.return_value = True
        inputs.side_effect = ['test@xyz.in', 'fname', 'lname', 'email@test.in', '9897675675']
        sqlite_execute_mock = mock.Mock()
        mocksql.cursor.return_value = sqlite_execute_mock
        sqlite_execute_mock.execute.return_value = sqlite_execute_mock
        sqlite_execute_mock.fetchone.return_value = [1]

        assert Admin(mocksql).update_employee() is True

    @mock.patch('mysql.connector.connect')
    @mock.patch('admin.input')
    def test_update_employee_failure_no_data(self, inputs, mocksql):
        inputs.side_effect = ['test@xyz.in']
        sqlite_execute_mock = mock.Mock()
        mocksql.cursor.return_value = sqlite_execute_mock
        sqlite_execute_mock.execute.return_value = sqlite_execute_mock
        sqlite_execute_mock.fetchone.return_value = None

        assert Admin(mocksql).update_employee() is False

    @mock.patch('mysql.connector.connect')
    @mock.patch('admin.input')
    def test_update_employee_failure_mysql_error(self, inputs, mocksql):
        inputs.side_effect = ['test@xyz.in']
        mocksql.cursor.side_effect = Exception

        assert Admin(mocksql).update_employee() is False

    @mock.patch('admin.Admin.update_member_action')
    @mock.patch('mysql.connector.connect')
    def test_update_member_validation_success(self, mocksql, arg1):
        arg1.return_value = True
        sqlite_execute_mock = mock.Mock()
        mocksql.cursor.return_value = sqlite_execute_mock
        sqlite_execute_mock.execute.return_value = sqlite_execute_mock
        sqlite_execute_mock.fetchone.return_value = [0]

        assert Admin(mocksql).update_member_validation('fname', 'lanme', 'oldemail@xyz.in', 'email@test.in',
                                                       '9898989898', 34) is True

    @mock.patch('admin.Admin.update_member_action')
    @mock.patch('mysql.connector.connect')
    def test_update_member_validation_success2(self, mocksql, arg1):
        arg1.return_value = True
        sqlite_execute_mock = mock.Mock()
        mocksql.cursor.return_value = sqlite_execute_mock
        sqlite_execute_mock.execute.return_value = sqlite_execute_mock
        sqlite_execute_mock.fetchone.side_effect = [[1], [1]]

        assert Admin(mocksql).update_member_validation('fname', 'lanme', 'oldemail@sdf.in', 'email@test.in',
                                                       '9898989898', 34) is True

    @mock.patch('admin.Admin.update_member_action')
    @mock.patch('mysql.connector.connect')
    def test_update_member_validation_failure_email_exist(self, mocksql, arg1):
        arg1.return_value = True
        sqlite_execute_mock = mock.Mock()
        mocksql.cursor.return_value = sqlite_execute_mock
        sqlite_execute_mock.execute.return_value = sqlite_execute_mock
        sqlite_execute_mock.fetchone.side_effect = [[1], [0]]

        assert Admin(mocksql).update_member_validation('fname', 'lanme', 'olldemail@aa.in', 'email@test.in',
                                                       '9898989898', 34) is False

    @mock.patch('mysql.connector.connect')
    def test_update_member_validation_failure_invalid_email(self, mocksql):
        sqlite_execute_mock = mock.Mock()
        mocksql.cursor.return_value = sqlite_execute_mock

        assert Admin(mocksql).update_member_validation('fname', 'lanme', 'old@email.com', 'emai%$l@.in',
                                                       '9898989898', 34) is False

    @mock.patch('mysql.connector.connect')
    def test_update_member_validation_failure_mysql_error(self, mocksql):
        mocksql.cursor.side_effect = Exception

        assert Admin(mocksql).update_member_validation('fname', 'lanme', 'old@email.com', 'email@test.in',
                                                       '9898989898', 34) is False

    @mock.patch('mysql.connector.connect')
    def test_update_member_action_success(self, mocksql):
        assert Admin(mocksql).update_member_action('fname', 'lanme', 'old@email.com', 'email@test.in',
                                                   '9898989898', 34) is True

    @mock.patch('mysql.connector.connect')
    def test_update_member_action_failure_mysql_error(self, mocksql):
        mocksql.cursor.side_effect = Exception

        assert Admin(mocksql).update_member_action('fname', 'lanme', 'old@email.com', 'email@test.in',
                                                   '9898989898', 34) is False

    def test_update_member_action_failure_invalid_phone(self):
        assert Admin(object).update_member_action('fname', 'lanme', 'old@email.com', 'email@test.in',
                                                  '989898898', 34) is False

    def test_update_member_action_failure_invalid_lastname(self):
        assert Admin(object).update_member_action('fname', 'lan9me', 'old@email.com', 'email@test.in',
                                                  '9898989898', 34) is False

    def test_update_member_action_failure_invalid_firstname(self):
        assert Admin(object).update_member_action('fna9me', 'lanme', 'old@email.com', 'email@test.in',
                                                  '9898989898', 34) is False

    @mock.patch('mysql.connector.connect')
    @mock.patch('admin.input')
    def test_delete_employee_success(self, inputs, mocksql):
        inputs.side_effect = ['email', 'y']
        sqlite_execute_mock = mock.Mock()
        mocksql.cursor.return_value = sqlite_execute_mock
        sqlite_execute_mock.execute.return_value = sqlite_execute_mock
        sqlite_execute_mock.fetchone.return_value = ''

        assert Admin(mocksql).delete_employee() is True

    @mock.patch('mysql.connector.connect')
    @mock.patch('admin.input')
    def test_delete_employee_failure_action_abort(self, inputs, mocksql):
        inputs.side_effect = ['email', 'n']
        sqlite_execute_mock = mock.Mock()
        mocksql.cursor.return_value = sqlite_execute_mock
        sqlite_execute_mock.execute.return_value = sqlite_execute_mock
        sqlite_execute_mock.fetchone.return_value = ''

        assert Admin(mocksql).delete_employee() is False

    @mock.patch('mysql.connector.connect')
    @mock.patch('admin.input')
    def test_delete_employee_failure_no_data(self, inputs, mocksql):
        inputs.side_effect = ['email']
        sqlite_execute_mock = mock.Mock()
        mocksql.cursor.return_value = sqlite_execute_mock
        sqlite_execute_mock.execute.return_value = sqlite_execute_mock
        sqlite_execute_mock.fetchone.return_value = None

        assert Admin(mocksql).delete_employee() is False

    @mock.patch('mysql.connector.connect')
    @mock.patch('admin.input')
    def test_delete_employee_failure_mysql_error(self, inputs, mocksql):
        inputs.side_effect = ['email']
        mocksql.execute.side_effect = Exception

        assert Admin(mocksql).delete_employee() is False

    @mock.patch('mysql.connector.connect')
    def test_show_employees_success(self, mocksql):
        sqlite_execute_mock = mock.Mock()
        mocksql.cursor.return_value = sqlite_execute_mock
        sqlite_execute_mock.execute.return_value = sqlite_execute_mock
        sqlite_execute_mock.fetchall.return_value = members

        assert Admin(mocksql).show_employees() is True

    @mock.patch('mysql.connector.connect')
    def test_show_employees_failure_no_data(self, mocksql):
        sqlite_execute_mock = mock.Mock()
        mocksql.cursor.return_value = sqlite_execute_mock
        sqlite_execute_mock.execute.return_value = sqlite_execute_mock
        sqlite_execute_mock.fetchall.return_value = []

        assert Admin(mocksql).show_employees() is False

    @mock.patch('mysql.connector.connect')
    def test_show_employees_failure_mysql_error(self, mocksql):
        mocksql.cursor.side_effect = Exception

        assert Admin(mocksql).show_employees() is False

    @mock.patch('admin.Admin.add_cab')
    @mock.patch('admin.input')
    def test_admin_cabs_menu_choice_1(self, inputs, arg1):
        arg1.return_value = True
        inputs.side_effect = ['1', '5']

        assert Admin(object).admin_cabs_menu() is True

    @mock.patch('admin.Admin.update_cab')
    @mock.patch('admin.input')
    def test_admin_cabs_menu_choice_2(self, inputs, arg1):
        arg1.return_value = True
        inputs.side_effect = ['2', '5']

        assert Admin(object).admin_cabs_menu() is True

    @mock.patch('admin.Admin.remove_cab')
    @mock.patch('admin.input')
    def test_admin_cabs_menu_choice_3(self, inputs, arg1):
        arg1.return_value = True
        inputs.side_effect = ['3', '5']

        assert Admin(object).admin_cabs_menu() is True

    @mock.patch('admin.Admin.show_cabs')
    @mock.patch('admin.input')
    def test_admin_cabs_menu_choice_4(self, inputs, arg1):
        arg1.return_value = True
        inputs.side_effect = ['4', '5']

        assert Admin(object).admin_cabs_menu() is True

    @mock.patch('admin.input')
    def test_admin_cabs_menu_wrong_choice(self, inputs):
        inputs.side_effect = ['7', '5']

        assert Admin(object).admin_cabs_menu() is True

    @mock.patch('admin.Admin.add_cab_action')
    @mock.patch('admin.input')
    def test_add_cab_success(self, inputs, arg1):
        inputs.side_effect = ['UK 07 AQ 5646', 'rohan mishra', '7676898767', 4]
        arg1.return_value = True

        assert Admin(object).add_cab() is True

    @mock.patch('admin.Admin.update_cab')
    @mock.patch('mysql.connector.connect')
    def test_add_cab_action_success(self, mocksql, arg1):
        arg1.return_value = True
        sqlite_execute_mock = mock.Mock()
        mocksql.cursor.return_value = sqlite_execute_mock
        sqlite_execute_mock.execute.return_value = sqlite_execute_mock

        assert Admin(mocksql).add_cab_action('UK 07 AQ 5646', 'rohan mishra', '7676898767', 4) is True

    @mock.patch('mysql.connector.connect')
    def test_add_cab_action_failure_mysql_error(self, mocksql):
        mocksql.cursor.side_effect = Exception

        assert Admin(mocksql).add_cab_action('UK 07 AQ 5646', 'rohan mishra', '7676898767', 4) is False

    @mock.patch('mysql.connector.connect')
    @mock.patch('admin.input')
    def test_update_cab_success_with_break1(self, inputs, mocksql):
        inputs.side_effect = ['UK 07 AQ 5646', 'source', 'destination', '10:00', '#']
        sqlite_execute_mock = mock.Mock()
        mocksql.cursor.return_value = sqlite_execute_mock
        sqlite_execute_mock.execute.return_value = sqlite_execute_mock
        sqlite_execute_mock.fetchone.return_value = [1211, 4]

        assert Admin(mocksql).update_cab() is True

    @mock.patch('mysql.connector.connect')
    @mock.patch('admin.input')
    def test_update_cab_success_with_break2(self, inputs, mocksql):
        inputs.side_effect = ['UK 07 AQ 5646', 'source', 'destination', '10:00', 'source2', '#']
        sqlite_execute_mock = mock.Mock()
        mocksql.cursor.return_value = sqlite_execute_mock
        sqlite_execute_mock.execute.return_value = sqlite_execute_mock
        sqlite_execute_mock.fetchone.return_value = [1211, 4]

        assert Admin(mocksql).update_cab() is True

    @mock.patch('mysql.connector.connect')
    @mock.patch('admin.input')
    def test_update_cab_success_with_break3(self, inputs, mocksql):
        inputs.side_effect = ['UK 07 AQ 5646', 'source', 'destination', '10:00', 'source2', 'destination2', '#']
        sqlite_execute_mock = mock.Mock()
        mocksql.cursor.return_value = sqlite_execute_mock
        sqlite_execute_mock.execute.return_value = sqlite_execute_mock
        sqlite_execute_mock.fetchone.return_value = [1211, 4]

        assert Admin(mocksql).update_cab() is True

    @mock.patch('mysql.connector.connect')
    @mock.patch('admin.input')
    def test_update_cab_failure_no_data(self, inputs, mocksql):
        inputs.side_effect = ['UK 07 AQ 5646']
        sqlite_execute_mock = mock.Mock()
        mocksql.cursor.return_value = sqlite_execute_mock
        sqlite_execute_mock.execute.return_value = sqlite_execute_mock
        sqlite_execute_mock.fetchone.return_value = ''

        assert Admin(mocksql).update_cab() is False

    @mock.patch('mysql.connector.connect')
    def test_update_cab_failure_mysql_error(self, mocksql):
        mocksql.cursor.side_effect = Exception

        assert Admin(mocksql).update_cab('UK 07 AQ 5646') is False

    @mock.patch('mysql.connector.connect')
    @mock.patch('admin.input')
    def test_remove_cab_success(self, inputs, mocksql):
        inputs.side_effect = ['UK 07 AQ 5646', 'y']
        sqlite_execute_mock = mock.Mock()
        mocksql.cursor.return_value = sqlite_execute_mock
        sqlite_execute_mock.execute.return_value = sqlite_execute_mock
        sqlite_execute_mock.fetchone.return_value = [1211]

        assert Admin(mocksql).remove_cab() is True

    @mock.patch('mysql.connector.connect')
    @mock.patch('admin.input')
    def test_remove_cab_failure_action_abort(self, inputs, mocksql):
        inputs.side_effect = ['UK 07 AQ 5646', 'n']
        sqlite_execute_mock = mock.Mock()
        mocksql.cursor.return_value = sqlite_execute_mock
        sqlite_execute_mock.execute.return_value = sqlite_execute_mock
        sqlite_execute_mock.fetchone.return_value = [1211]

        assert Admin(mocksql).remove_cab() is False

    @mock.patch('mysql.connector.connect')
    @mock.patch('admin.input')
    def test_remove_cab_failure_no_data(self, inputs, mocksql):
        inputs.side_effect = ['UK 07 AQ 5646']
        sqlite_execute_mock = mock.Mock()
        mocksql.cursor.return_value = sqlite_execute_mock
        sqlite_execute_mock.execute.return_value = sqlite_execute_mock
        sqlite_execute_mock.fetchone.return_value = None

        assert Admin(mocksql).remove_cab() is False

    @mock.patch('mysql.connector.connect')
    @mock.patch('admin.input')
    def test_remove_cab_failure_mysql_error(self, inputs, mocksql):
        inputs.side_effect = ['UK 07 AQ 5646']
        mocksql.cursor.side_effect = Exception

        assert Admin(mocksql).remove_cab() is False

    @mock.patch('mysql.connector.connect')
    def test_show_cabs_success(self, mocksql):
        sqlite_execute_mock = mock.Mock()
        mocksql.cursor.return_value = sqlite_execute_mock
        sqlite_execute_mock.execute.return_value = sqlite_execute_mock
        sqlite_execute_mock.fetchall.return_value = cabs_data

        assert Admin(mocksql).show_cabs() is True

    @mock.patch('mysql.connector.connect')
    def test_show_cabs_failure_no_data(self, mocksql):
        sqlite_execute_mock = mock.Mock()
        mocksql.cursor.return_value = sqlite_execute_mock
        sqlite_execute_mock.execute.return_value = sqlite_execute_mock
        sqlite_execute_mock.fetchall.return_value = []

        assert Admin(mocksql).show_cabs() is False

    @mock.patch('mysql.connector.connect')
    def test_show_cabs_failure_mysql_error(self, mocksql):
        mocksql.cursor.side_effect = Exception

        assert Admin(mocksql).show_cabs() is False

    @mock.patch('mysql.connector.connect')
    @mock.patch('admin.input')
    def test_employee_booking_success(self, inputs, mocksql):
        inputs.side_effect = ['employee@email.com']
        sqlite_execute_mock = mock.Mock()
        mocksql.cursor.return_value = sqlite_execute_mock
        sqlite_execute_mock.execute.return_value = sqlite_execute_mock
        sqlite_execute_mock.fetchone.return_value = [1211]
        sqlite_execute_mock.fetchall.return_value = employee_booking_data

        assert Admin(mocksql).employee_bookings() is True

    @mock.patch('mysql.connector.connect')
    @mock.patch('admin.input')
    def test_employee_booking_failure_no_data(self, inputs, mocksql):
        inputs.side_effect = ['employee@email.com']
        sqlite_execute_mock = mock.Mock()
        mocksql.cursor.return_value = sqlite_execute_mock
        sqlite_execute_mock.execute.return_value = sqlite_execute_mock
        sqlite_execute_mock.fetchone.return_value = [1211]
        sqlite_execute_mock.fetchall.return_value = []

        assert Admin(mocksql).employee_bookings() is False

    @mock.patch('mysql.connector.connect')
    @mock.patch('admin.input')
    def test_employee_booking_failure_email_not_found(self, inputs, mocksql):
        inputs.side_effect = ['employee@email.com']
        sqlite_execute_mock = mock.Mock()
        mocksql.cursor.return_value = sqlite_execute_mock
        sqlite_execute_mock.execute.return_value = sqlite_execute_mock
        sqlite_execute_mock.fetchone.return_value = None

        assert Admin(mocksql).employee_bookings() is False

    @mock.patch('mysql.connector.connect')
    @mock.patch('admin.input')
    def test_employee_booking_failure_mysql_error(self, inputs, mocksql):
        inputs.side_effect = ['employee@email.com']
        mocksql.cursor.side_effect = Exception

        assert Admin(mocksql).employee_bookings() is False

    @mock.patch('mysql.connector.connect')
    @mock.patch('admin.input')
    def test_bookings_for_dates_success(self, inputs, mocksql):
        inputs.side_effect = ['2020-05-01', '2020-05-26']
        sqlite_execute_mock = mock.Mock()
        mocksql.cursor.return_value = sqlite_execute_mock
        sqlite_execute_mock.execute.return_value = sqlite_execute_mock
        sqlite_execute_mock.fetchall.return_value = employee_booking_data

        assert Admin(mocksql).bookings_for_dates() is True

    @mock.patch('mysql.connector.connect')
    @mock.patch('admin.input')
    def test_bookings_for_dates_failure_no_data(self, inputs, mocksql):
        inputs.side_effect = ['2020-05-01', '2020-05-26']
        sqlite_execute_mock = mock.Mock()
        mocksql.cursor.return_value = sqlite_execute_mock
        sqlite_execute_mock.execute.return_value = sqlite_execute_mock
        sqlite_execute_mock.fetchall.return_value = []

        assert Admin(mocksql).bookings_for_dates() is False

    @mock.patch('mysql.connector.connect')
    @mock.patch('admin.input')
    def test_bookings_for_dates_failure_mysql_error(self, inputs, mocksql):
        inputs.side_effect = ['2020-05-01', '2020-05-26']
        mocksql.cursor.side_effect = Exception

        assert Admin(mocksql).bookings_for_dates() is False
