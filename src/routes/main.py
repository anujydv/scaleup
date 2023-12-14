"""This file contains all included routes and service settings."""
import uvicorn
from fastapi import FastAPI
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from src.utility.logger_config import Logger
from src.config.config import settings
from src.routes.scaleup import scheduler_router

log = Logger().get_logger()
app = FastAPI(title="Auto scaler",
              description="scaleup: a service that helps to autoscale other services")


@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(_request, exc):
    """This function helps to create a generic exception message."""
    headers = getattr(exc, "headers", None)

    if headers:
        return JSONResponse(
            {"error": {
                "data": None,
                "message": exc.error
            }},
            status_code=exc.status_code,
            headers=headers
        )
    try:
        if exc.detail:
            log.error("Error while handling error msg conversion",
                      extra={"error": exc.detail, "status_code": 404})
            return JSONResponse({"error": {
                "data": None,
                "message": exc.detail
            }},
                status_code=exc.status_code)
    except BaseException as err:
        log.error("No body error",
                  extra={"error": exc.detail, "status_code": 404})
    return JSONResponse({"error": {
        "data": None,
        "message": exc.error
    }},
        status_code=exc.status_code)


origins = [
    "http://localhost:2000",
]

log.info("Adding CORS middleware", extra={"status_code": "ok"})
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(404)
def not_found_handler(request: Request, exc):
    log.error("Oops! This path does not exist.",
              extra={"error": exc.detail, "status_code": 404})
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"message": "Oops! This path does not exist."},
    )

log.info("Including scheduler router")
app.include_router(
    scheduler_router,
    prefix="/schedule",
    tags=["Auto scaler scheduler"],
)


def main():
    """Main function."""
    log.info(f"Starting server on port {settings.DEFAULT.PORT}")
    uvicorn.run("src.routes.main:app", host=settings.DEFAULT.HOST, port=settings.DEFAULT.PORT,
                reload=True, log_level="debug")


if __name__ == "__main__":
    main()
    log.info(f"Starting started .......")
