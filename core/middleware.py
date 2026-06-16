import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from core.logging.logger import get_module_logger

# Initialize the platform's standard logger
logger = get_module_logger(__name__)


class MetricsMiddleware(BaseHTTPMiddleware):
    "Middleware to measure and log request execution time in JSON format"

    async def dispatch(self, request: Request, call_next):
        # 1. Record the exact start time using a high-resolution hardware timer
        start_time = time.perf_counter()

        # 2. Forward the request to the application's endpoints
        response = await call_next(request)

        # 3. Calculate processing time in milliseconds
        process_time_ms = round((time.perf_counter() - start_time) * 1000, 2)

        # 4. Inject metrics into the structured JSON logging payload
        logger.info(
            "API Request Processed",
            extra={
                "extra_fields": {
                    "http_method": request.method,
                    "request_path": request.url.path,
                    "status_code": response.status_code,
                    "execution_time_ms": process_time_ms,
                }
            },
        )

        # 5. Attach the metric to the response headers for frontend/monitoring usage
        response.headers["X-Process-Time-Ms"] = str(process_time_ms)

        return response
