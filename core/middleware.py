import time
import json
from core.logging.logger import get_module_logger

logger = get_module_logger(__name__)


class ASGIMetricsAndErrorMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        start_time = time.perf_counter()
        status_code = 500
        response_started = False

        async def custom_send(message):
            nonlocal status_code, response_started
            if message["type"] == "http.response.start":
                response_started = True
                status_code = message.get("status", 500)

                headers = list(message.get("headers", []))
                process_time_ms = round((time.perf_counter() - start_time) * 1000, 2)
                headers.append(
                    (b"x-process-time-ms", str(process_time_ms).encode("utf-8"))
                )
                message["headers"] = headers

            await send(message)

        try:
            await self.app(scope, receive, custom_send)
        except Exception as exc:
            logger.error(
                "Unhandled Server Exception",
                exc_info=True,
                extra={
                    "extra_fields": {
                        "request_path": scope.get("path", ""),
                        "http_method": scope.get("method", ""),
                        "error_type": type(exc).__name__,
                        "error_message": str(exc),
                    }
                },
            )

            if not response_started:
                response_body = json.dumps(
                    {
                        "status": "error",
                        "message": (
                            "An unexpected internal error occurred. "
                            "Our engineers have been notified."
                        ),
                        "error_code": "INTERNAL_SERVER_ERROR",
                    }
                ).encode("utf-8")

                await send(
                    {
                        "type": "http.response.start",
                        "status": 500,
                        "headers": [
                            (b"content-type", b"application/json"),
                            (
                                b"content-length",
                                str(len(response_body)).encode("utf-8"),
                            ),
                        ],
                    }
                )
                await send({"type": "http.response.body", "body": response_body})
            status_code = 500

        process_time_ms = round((time.perf_counter() - start_time) * 1000, 2)
        logger.info(
            "API Request Processed",
            extra={
                "extra_fields": {
                    "http_method": scope.get("method", ""),
                    "request_path": scope.get("path", ""),
                    "status_code": status_code,
                    "execution_time_ms": process_time_ms,
                }
            },
        )
