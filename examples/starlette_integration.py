import time

import uvicorn
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from starlette.routing import Route

from logger_kit import Logger

# Initialize logger with Starlette app name
logger = Logger(
    name="starlette-app",
    level="INFO",
    extra_fields={"service": "starlette-web", "environment": "development"},
)


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start_time = time.time()

        # Log incoming request
        logger.info(
            "Incoming request",
            extra={
                "method": request.method,
                "path": request.url.path,
                "client": request.client.host,
                "user_agent": request.headers.get("user-agent"),
            },
        )

        try:
            response = await call_next(request)

            # Log response details
            logger.info(
                "Request completed",
                extra={
                    "duration_ms": (time.time() - start_time) * 1000,
                    "status_code": response.status_code,
                },
            )
            return response

        except Exception as exc:
            # Log error details
            logger.error(
                "Request failed",
                extra={
                    "error_type": type(exc).__name__,
                    "error_message": str(exc),
                    "duration_ms": (time.time() - start_time) * 1000,
                },
            )
            return JSONResponse({"error": "Internal server error"}, status_code=500)


async def homepage(request):
    logger.info("Processing homepage request")
    return JSONResponse({"message": "Welcome to Starlette with logger-kit!"})


async def get_user(request):
    user_id = request.path_params["user_id"]

    try:
        if not user_id.isdigit():
            raise ValueError("Invalid user ID format")

        logger.info("Fetching user details", extra={"user_id": user_id})

        return JSONResponse({"user_id": user_id, "name": f"User {user_id}"})

    except ValueError as e:
        logger.warning(
            "Invalid user lookup request", extra={"user_id": user_id, "error": str(e)}
        )
        return JSONResponse({"error": str(e)}, status_code=400)


routes = [Route("/", homepage), Route("/users/{user_id}", get_user)]

middleware = [Middleware(LoggingMiddleware)]

app = Starlette(debug=True, routes=routes, middleware=middleware)

if __name__ == "__main__":
    # Enable debug logging for development
    logger.set_level("DEBUG")

    logger.info("Starting Starlette server", extra={"port": 8000})
    uvicorn.run(app, host="0.0.0.0", port=8000)
