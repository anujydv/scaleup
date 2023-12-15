"""
This file contains the SchedulerService class for performing scheduler operations.
"""
# SYSTEM IMPORT CLASS
import time

import requests
import urllib3
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.background import BackgroundScheduler

# USER IMPORT CLASS
from src.utility.logger_config import Logger, ScaleupError

logger = Logger().get_logger()


jobstores = {
    'default': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')
}
scheduler = BackgroundScheduler(jobstores=jobstores)
scheduler.start()


class SchedulerService:
    """ Schedule class to help perform scheduler operation """

    def __init__(self):
        self.target_cpu: float = 0.80

    def schedule_auto_scaler(self, payload):
        """Help to schedule auto scale check at defined interval"""
        try:
            scheduler.add_job(self.scheduler_operation, 'interval',
                              seconds=payload.interval, args=[payload.service_url])
            return {"message": "Job added successfully"}
        except Exception as exc:
            logger.error(
                f"Exception while scheduling 'auto_scaler' with interval: {
                    payload.interval}",
                extra={"error": f"{str(exc)}", "status_code": 500})
            raise ScaleupError(status_code=500,
                               error="Error with scheduling auto_scaler") from exc

    def scheduler_operation(self, service_url):
        """Function to perform scheduled operation"""
        try:
            response: requests.Response()
            try:
                response = requests.get(f"{service_url}/app/status", timeout=5)
            except (requests.exceptions.RequestException, requests.exceptions.ConnectionError,
                    urllib3.exceptions.NewConnectionError, urllib3.exceptions.MaxRetryError) as exc:
                logger.error(f"Request exception occurred: {
                             exc}", extra={"status_code": 500})
            data: dict = {}
            if response.status_code == 200:
                data = response.json()
                current_cpu = data['cpu']['highPriority']
                current_replicas = data['replicas']
                desired_replicas = int(
                    current_replicas * (current_cpu / self.target_cpu))
                desired_replicas = max(1, desired_replicas)
                print(f"replica: {desired_replicas} {current_replicas}")
                if desired_replicas != current_replicas:
                    for _ in range(3):
                        try:
                            response = requests.post(f"{service_url}/app/replicas",
                                                     json={
                                "replicas": desired_replicas},
                                timeout=5)
                            response.raise_for_status()
                            break
                        except requests.exceptions.HTTPError as http_err:
                            logger.error(f"HTTP error occurred: {http_err}")
                            time.sleep(2)
                        except Exception as err:
                            logger.error(f"An error occurred: {err}")
                            time.sleep(2)
            else:
                logger.error("Error while getting the service status", extra={
                             "status_code": 500})
        except Exception as exc:
            logger.error(
                f"Exception while performing 'scheduler_operation': {
                    service_url}",
                extra={"error": f"{exc}", "status_code": 500})
