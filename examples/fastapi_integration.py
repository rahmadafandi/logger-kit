from fastapi import FastAPI, Request
from fastapi.middleware.base import BaseHTTPMiddleware

from logger_kit import Logger

app = FastAPI()

# Initialize logger with FastAPI-specific configuration
logger = Logger(
    name="fastapi.app", level="INFO", extra={"service": "web", "framework": "fastapi"}
)


# Example middleware for request logging
class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Log incoming request
        await logger.ainfo(
            "Incoming request",
            extra={
                "method": request.method,
                "path": request.url.path,
                "client": request.client.host if request.client else None,
            },
        )

        response = await call_next(request)

        # Log response
        await logger.ainfo(
            "Response sent",
            extra={
                "status_code": response.status_code,
                "content_type": response.headers.get("content-type"),
            },
        )

        return response


# Add middleware to app
app.add_middleware(LoggingMiddleware)


# Example endpoint with structured logging
@app.get("/users/{user_id}")
async def get_user(user_id: int):
    try:
        # Simulate user fetch
        user = {"id": user_id, "username": "test_user"}

        await logger.ainfo(
            "User details retrieved", extra={"user_id": user_id, "action": "user_fetch"}
        )

        return user
    except Exception as e:
        await logger.aerror(
            "Error fetching user", extra={"user_id": user_id, "error": str(e)}
        )
        return {"error": "User not found"}


# Example of background task logging
@app.post("/tasks")
async def create_task():
    try:
        # Simulate async task
        task_id = "123"
        await logger.ainfo(
            "Task created", extra={"task_id": task_id, "status": "pending"}
        )
        return {"task_id": task_id}
    except Exception as e:
        await logger.aerror("Task creation failed", extra={"error": str(e)})
        return {"error": "Failed to create task"}
