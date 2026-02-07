from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from src.infrastructure.observability.logger import get_logger

logger = get_logger("http")


class ErrorLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except Exception as exc:
            logger.error(
                "Unhandled exception",
                extra={
                    "extra": {
                        "path": request.url.path,
                        "method": request.method
                    }
                }
            )
            raise
