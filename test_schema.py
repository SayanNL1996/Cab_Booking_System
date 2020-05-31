""" Test cases for schema file."""

import mock
from schema import Schema


class TestSchema:

    @mock.patch('mysql.connector.connect')
    def test_setup_admin_success(self, mocksql):
        """ Test setup admin method."""
        sqlite_execute_mock = mock.Mock()
        mocksql.cursor.return_value = sqlite_execute_mock
        sqlite_execute_mock.execute.return_value = sqlite_execute_mock
        sqlite_execute_mock.fetchone.return_value = [0]

        assert Schema(mocksql).setup_admin() is True

    @mock.patch('mysql.connector.connect')
    def test_setup_admin_failure(self, mocksql):
        """ Test setup admin method."""
        mocksql.cursor.side_effect = Exception

        assert Schema(mocksql).setup_admin() is False

    @mock.patch('mysql.connector.connect')
    def test_create_tables_success(self, mocksql):
        """ Test create tables method."""
        sqlite_execute_mock = mock.Mock()
        mocksql.cursor.return_value = sqlite_execute_mock
        sqlite_execute_mock.execute.return_value = sqlite_execute_mock

        assert Schema(mocksql).create_tables() is True

    @mock.patch('mysql.connector.connect')
    def test_create_tables_failure(self, mocksql):
        """ Test create tables method."""
        mocksql.cursor.side_effect = Exception

        assert Schema(mocksql).create_tables() is False
