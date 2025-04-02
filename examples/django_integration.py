from django.http import JsonResponse

from logger_kit import Logger

# Initialize logger with Django-specific configuration
logger = Logger(
    name="django.app", level="INFO", extra={"service": "web", "framework": "django"}
)


# Example middleware for request logging
class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Log incoming request
        logger.info(
            "Incoming request",
            extra={
                "method": request.method,
                "path": request.path,
                "ip": request.META.get("REMOTE_ADDR"),
            },
        )

        response = self.get_response(request)

        # Log response
        logger.info(
            "Response sent",
            extra={
                "status_code": response.status_code,
                "content_type": response.get("Content-Type", ""),
            },
        )

        return response


# Example view with structured logging
def user_view(request, user_id):
    try:
        # Simulate user fetch
        user = {"id": user_id, "username": "test_user"}

        logger.info(
            "User details retrieved", extra={"user_id": user_id, "action": "user_fetch"}
        )

        return JsonResponse(user)
    except Exception as e:
        logger.error("Error fetching user", extra={"user_id": user_id, "error": str(e)})
        return JsonResponse({"error": "User not found"}, status=404)
