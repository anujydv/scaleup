# SYSTEM IMPORT CLASS
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from fastapi import status
from apscheduler.schedulers.background import BackgroundScheduler
import requests
# USER IMPORT CLASS

from src.utility.logger_config import ScaleupError
from src.utility.logger_config import Logger
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
            print(exc)
            logger.error(
                "Exception while scheduling 'auto_scaler' with interval: %s" %
                payload.interval, extra={"error": f"{str(exc)}", "status_code": 500})
            raise ScaleupError(status_code=500,
                               error="Error with scheduling auto_scaler") from exc

    def scheduler_operation(self, service_url):
        """Function to perform scheduled operation"""
        try:
            response = requests.get(f"{service_url}/app/status")
            print(response)
            if response.status_code == 200:
                data = response.json()
                print(data)
                current_cpu = data['cpu']['highPriority']
                current_replicas = data['replicas']
                desired_replicas = int(
                    current_replicas * (current_cpu / self.target_cpu))
                desired_replicas = max(1, desired_replicas)
                print(f"replica: {desired_replicas} {current_replicas}")
                if desired_replicas != current_replicas:
                    requests.put(f"{service_url}/app/replicas",
                                 json={"replicas": desired_replicas})
            else:
                logger.error("Error while getting the service status", extra={
                             "status_code": 500})
                raise ScaleupError(
                    status_code=500, error="Error while getting the service status")
            data = {
                "cpu_usage": data["cpu"]['highPriority'],
            }
            status_code = status.HTTP_200_OK
        except Exception as exc:
            print(exc)
            logger.error(
                "Exception while performing 'scheduler_operation': %s" %
                service_url, extra={"error": f"{exc}", "status_code": 500})
            raise ScaleupError(status_code=500,
                               error="Error while performing scheduler operation") from exc
        return data, status_code
