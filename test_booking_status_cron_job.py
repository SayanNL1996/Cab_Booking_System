import unittest
from datetime import timedelta

import mock
import booking_status_cron_job

class TestBookingStatusCron(unittest.TestCase):

    @mock.patch('builtins.print')
    @mock.patch('booking_status_cron_job.connector')
    def test_update_booking_status(self, mock_db, mock_print):
        mock_db.connect().cursor().fetchall.return_value = [[1,2,3,4,5,6,7,8,9,10,11,timedelta(minutes=30),13]]
        booking_status_cron_job.update_booking_status()
        mock_db.connect().close.assert_called_once()
        self.assertEqual(mock_db.connect().cursor().execute.call_count, 3)


if __name__ == '__main__':
    unittest.main()
