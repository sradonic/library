from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from . import CustomHTTPException
import logging

logger = logging.getLogger("library_api")


def register_exception_handlers(app):
    @app.exception_handler(CustomHTTPException)
    async def custom_http_exception_handler(request: Request, exc: CustomHTTPException):
        user = request.state.user if hasattr(request.state, 'user') else None
        detail = exc.detail if user and user.is_admin else "An error occurred"
        logger.error(f"Custom Error - {exc.status_code}: {detail} triggered by {request.url.path}")
        return JSONResponse(status_code=exc.status_code, content={"message": detail})

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        logger.warning(f"Validation error on {request.url.path}: {exc.errors()}")
        return JSONResponse(status_code=422, content={"message": "Validation error", "errors": exc.errors()})

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        logger.warning(f"HTTP Exception on {request.url.path}: {exc.detail}")
        print(f"HTTP Exception: {exc.detail}")
        return JSONResponse(status_code=exc.status_code, content={"message": exc.detail})

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        logger.critical(f"Unexpected error on {request.url.path}: {str(exc)}", exc_info=True)
        return JSONResponse(status_code=500, content={"message": "Internal Server Error"})
