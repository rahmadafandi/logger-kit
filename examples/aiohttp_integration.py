import time
from typing import Awaitable, Callable

from aiohttp import web
from aiohttp.web import middleware

from logger_kit import Logger

# Initialize logger with aiohttp app name
logger = Logger(
    name="aiohttp-app",
    level="INFO",
    extra_fields={"service": "aiohttp-web", "environment": "development"},
)


@middleware
async def logging_middleware(
    request: web.Request, handler: Callable[[web.Request], Awaitable[web.Response]]
) -> web.Response:
    start_time = time.time()

    # Log incoming request
    logger.info(
        "Incoming request",
        extra={
            "method": request.method,
            "path": request.path,
            "remote": request.remote,
            "user_agent": request.headers.get("User-Agent"),
        },
    )

    try:
        response = await handler(request)

        # Log response details
        logger.info(
            "Request completed",
            extra={
                "duration_ms": (time.time() - start_time) * 1000,
                "status_code": response.status,
            },
        )
        return response

    except web.HTTPException as ex:
        # Log HTTP exceptions
        logger.warning(
            "HTTP exception occurred",
            extra={
                "status_code": ex.status,
                "error_message": ex.text,
                "duration_ms": (time.time() - start_time) * 1000,
            },
        )
        raise
    except Exception as e:
        # Log unexpected errors
        logger.error(
            "Request failed",
            extra={
                "error_type": type(e).__name__,
                "error_message": str(e),
                "duration_ms": (time.time() - start_time) * 1000,
            },
        )
        return web.json_response({"error": "Internal server error"}, status=500)


async def index(request):
    logger.info("Processing index request")
    return web.json_response({"message": "Welcome to aiohttp with logger-kit!"})


async def get_user(request):
    user_id = request.match_info["user_id"]

    try:
        if not user_id.isdigit():
            raise ValueError("Invalid user ID format")

        logger.info("Fetching user details", extra={"user_id": user_id})

        return web.json_response({"user_id": user_id, "name": f"User {user_id}"})

    except ValueError as e:
        logger.warning(
            "Invalid user lookup request", extra={"user_id": user_id, "error": str(e)}
        )
        return web.json_response({"error": str(e)}, status=400)


app = web.Application(middlewares=[logging_middleware])
app.router.add_get("/", index)
app.router.add_get("/users/{user_id}", get_user)

if __name__ == "__main__":
    # Enable debug logging for development
    logger.set_level("DEBUG")

    logger.info("Starting aiohttp server", extra={"port": 8080})
    web.run_app(app, port=8080)
