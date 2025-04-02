import time
import traceback

import tornado.ioloop
import tornado.web

from logger_kit import Logger

# Initialize logger with Tornado app name
logger = Logger(
    name="tornado-app",
    level="INFO",
    extra_fields={"service": "tornado-web", "environment": "development"},
)


class BaseHandler(tornado.web.RequestHandler):
    def initialize(self):
        self.start_time = time.time()

    def prepare(self):
        """Log incoming request details"""
        logger.info(
            "Incoming request",
            extra={
                "method": self.request.method,
                "path": self.request.path,
                "remote_ip": self.request.remote_ip,
                "user_agent": self.request.headers.get("User-Agent"),
            },
        )

    def on_finish(self):
        """Log request completion details"""
        duration_ms = (time.time() - self.start_time) * 1000
        logger.info(
            "Request completed",
            extra={"duration_ms": duration_ms, "status_code": self.get_status()},
        )

    def write_error(self, status_code, **kwargs):
        """Custom error handling with logging"""
        error_details = {"status_code": status_code}

        if "exc_info" in kwargs:
            exc_type, exc_value, exc_traceback = kwargs["exc_info"]
            error_details.update(
                {
                    "error_type": exc_type.__name__,
                    "error_message": str(exc_value),
                    "traceback": traceback.format_exception(*kwargs["exc_info"]),
                }
            )

        logger.error("Request failed", extra=error_details)

        self.finish(
            {"error": str(error_details.get("error_message", "Internal server error"))}
        )


class MainHandler(BaseHandler):
    async def get(self):
        logger.info("Processing main request")
        self.write({"message": "Welcome to Tornado with logger-kit!"})


class UserHandler(BaseHandler):
    async def get(self, user_id):
        try:
            if not user_id.isdigit():
                raise ValueError("Invalid user ID format")

            logger.info("Fetching user details", extra={"user_id": user_id})

            # Simulate async user lookup
            await tornado.gen.sleep(0.1)
            self.write({"user_id": user_id, "name": f"User {user_id}"})

        except ValueError as e:
            logger.warning(
                "Invalid user lookup request",
                extra={"user_id": user_id, "error": str(e)},
            )
            self.set_status(400)
            self.write({"error": str(e)})


def make_app():
    return tornado.web.Application(
        [
            (r"/", MainHandler),
            (r"/users/([^/]+)", UserHandler),
        ]
    )


if __name__ == "__main__":
    # Enable debug logging for development
    logger.set_level("DEBUG")

    app = make_app()
    app.listen(8888)
    logger.info("Tornado server starting", extra={"port": 8888})
    tornado.ioloop.IOLoop.current().start()
