""" Test cases for run file."""

import mock
import run
from run import Run


class TestRun:

    @mock.patch('run.connector')
    def test_sql_connection_success(self, mocksql):
        """ Test sql connection method."""
        mocksql.connect().return_value = object

        assert run.sql_connection().return_value == object

    @mock.patch('run.connector')
    def test_sql_connection_failure(self, mocksql):
        """ Test sql connection method."""
        mocksql.connect().return_value = None

        assert run.sql_connection().return_value is None

    @mock.patch('run.connector')
    def test_get_role_success(self, mocksql):
        """ Test get role method."""
        sqlite_execute_mock = mock.Mock()
        mocksql.cursor.return_value = sqlite_execute_mock
        mocksql.execute.return_value = sqlite_execute_mock
        sqlite_execute_mock.fetchone.return_value = ['email', 'pswd', 11]

        assert Run(mocksql).get_role('email', 'pswd') == 11

    @mock.patch('run.connector')
    def test_get_role_failure(self, mocksql):
        """ Test get role method."""
        sqlite_execute_mock = mock.Mock()
        mocksql.cursor.return_value = sqlite_execute_mock
        mocksql.execute.return_value = sqlite_execute_mock
        sqlite_execute_mock.fetchone.return_value = None

        assert Run(mocksql).get_role('email', 'pswd') == 0

    @mock.patch('run.connector')
    def test_get_role_failure_mysql_error(self, mocksql):
        """ Test get role method."""
        mocksql.cursor.side_effect = Exception

        assert Run(mocksql).get_role('email', 'pswd') == 0

    @mock.patch('run.Employee.employee_menu')
    @mock.patch('run.Run.get_role')
    @mock.patch('run.input')
    @mock.patch('run.connector')
    def test_login_menu_employee(self, mocksql, inputs, role, employee):
        """ Test login menu method."""
        role.return_value = 22
        employee.return_value = True
        inputs.side_effect = ['email', 'pswd', '#']

        assert Run(mocksql).login_menu() is True

    @mock.patch('run.Admin.admin_menu', return_value=True)
    @mock.patch('run.Run.get_role')
    @mock.patch('run.input')
    @mock.patch('run.connector')
    def test_login_menu_admin(self, mocksql, inputs, role, admin):
        """ Test login menu method."""
        role.return_value = 11
        admin.return_value = True
        inputs.side_effect = ['email', 'pswd', '#']

        assert Run(mocksql).login_menu() is True

    @mock.patch('run.Run.get_role')
    @mock.patch('run.input')
    @mock.patch('run.connector')
    def test_login_menu_wrong_credentials(self, mocksql, inputs, role):
        """ Test login menu method."""
        role.return_value = 0
        inputs.side_effect = ['email', 'pswd', '#']

        assert Run(mocksql).login_menu() is True

    @mock.patch('run.sql_connection')
    def test_main_if_condition(self, conn):
        """ Test main method."""
        conn.return_value = None

        assert run.main() is False

    @mock.patch('run.Schema.setup_admin')
    @mock.patch('run.Schema.create_tables')
    @mock.patch('run.Run.login_menu')
    @mock.patch('run.sql_connection')
    def test_main_else_condition(self, conn, lm, ct, sa):
        """ Test main method."""
        lm.return_value = True
        ct.return_value = True
        sa.return_value = True
        conn.return_value = mock.Mock()

        assert run.main() is True

    @mock.patch('run.sql_connection')
    def test_main_failure_mysql_error(self, mocksql):
        """ Test main method."""
        mocksql.side_effect = Exception

        assert run.main() is False
