from fastapi import APIRouter
from fastapi.responses import JSONResponse
from src.services.scaleup.index import SchedulerService
from src.services.scaleup.type import AutosclaerPayload
from src.utility.logger_config import Logger

api_logger = Logger().get_logger()
scheduler_router = APIRouter()


@scheduler_router.post('/auto-scaler')
async def auto_scale(payload: AutosclaerPayload):
    """this route is to auto scale services"""
    try:
        scheduler_service = SchedulerService()
        scheduler_service.schedule_auto_scaler(payload)
        api_logger.info("Auto scaling successful", extra={"status_code": 200})
        return JSONResponse(status_code=200, content={
            "success": {
                "message": "Auto scaling initiated successfully",
            }
        })
    except Exception as e:
        api_logger.error(f"Error in scheduling auto scaling: {str(e)}",
                         extra={"status_code": 500})
        return JSONResponse(status_code=500, content={
            "error": {
                "message": "Error in auto scaling",
                "details": str(e)
            }
        })
