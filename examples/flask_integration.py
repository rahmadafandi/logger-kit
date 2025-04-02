import time
from functools import wraps

from flask import Flask, g, request

from logger_kit import Logger

app = Flask(__name__)

# Initialize logger with Flask app name
logger = Logger(
    name="flask-app",
    level="INFO",
    extra_fields={
        "service": "flask-web",
        "environment": app.config.get("ENV", "development"),
    },
)


def log_request():
    """Middleware to log request details"""

    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            # Store request start time
            g.start_time = time.time()

            # Log incoming request
            logger.info(
                "Incoming request",
                extra={
                    "method": request.method,
                    "path": request.path,
                    "remote_addr": request.remote_addr,
                    "user_agent": request.headers.get("User-Agent"),
                },
            )

            try:
                response = f(*args, **kwargs)
                # Log response time on success
                logger.info(
                    "Request completed",
                    extra={
                        "duration_ms": (time.time() - g.start_time) * 1000,
                        "status_code": response.status_code,
                    },
                )
                return response
            except Exception as e:
                # Log error details
                logger.error(
                    "Request failed",
                    extra={
                        "error": str(e),
                        "error_type": type(e).__name__,
                        "duration_ms": (time.time() - g.start_time) * 1000,
                    },
                )
                raise

        return wrapped

    return decorator


@app.route("/")
@log_request()
def index():
    logger.info("Processing index request")
    return {"message": "Welcome to Flask with logger-kit!"}


@app.route("/users/<user_id>")
@log_request()
def get_user(user_id):
    try:
        # Simulate user lookup
        if not user_id.isdigit():
            raise ValueError("Invalid user ID format")

        logger.info("Fetching user details", extra={"user_id": user_id})

        # Simulate successful response
        return {"user_id": user_id, "name": f"User {user_id}"}

    except ValueError as e:
        logger.warning(
            "Invalid user lookup request", extra={"user_id": user_id, "error": str(e)}
        )
        return {"error": str(e)}, 400


@app.errorhandler(Exception)
def handle_error(error):
    logger.error(
        "Unhandled exception",
        extra={"error_type": type(error).__name__, "error_message": str(error)},
    )
    return {"error": "Internal server error"}, 500


if __name__ == "__main__":
    # Enable debug logging for development
    logger.set_level("DEBUG")
    app.run(debug=True)
