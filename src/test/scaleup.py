import unittest
from src.services.scaleup.index import SchedulerService
from unittest.mock import patch, Mock

class TestSchedulerService(unittest.TestCase):
    def setUp(self):
        self.scheduler_service = SchedulerService()

    @patch('src.services.scaleup.index.BackgroundScheduler')
    def test_schedule_auto_scaler(self, mock_scheduler):
        mock_payload = Mock()
        mock_payload.interval = 10
        mock_payload.service_url = "http://test.com"
        mock_scheduler.add_job.return_value = None
        response = self.scheduler_service.schedule_auto_scaler(mock_payload)
        self.assertEqual(response, {"message": "Job added successfully"})
        mock_scheduler.add_job.assert_called_once_with(self.scheduler_service.scheduler_operation, 'interval', minutes=mock_payload.interval, args=[mock_payload.service_url])

    @patch('src.services.scaleup.index.BackgroundScheduler')
    def test_schedule_auto_scaler_exception(self, mock_scheduler):
        mock_payload = Mock()
        mock_payload.interval = 10
        mock_payload.service_url = "http://test.com"
        mock_scheduler.add_job.side_effect = Exception("Error")
        with self.assertRaises(Exception):
            self.scheduler_service.schedule_auto_scaler(mock_payload)

    @patch('src.services.scaleup.index.requests')
    def test_scheduler_operation(self, mock_requests):
        mock_payload = Mock()
        mock_payload.service_url = "http://test.com"
        mock_requests.get.return_value = Mock(status_code=200)
        self.scheduler_service.scheduler_operation(mock_payload.service_url)
        mock_requests.get.assert_called_once_with(mock_payload.service_url)

if __name__ == '__main__':
    unittest.main()

