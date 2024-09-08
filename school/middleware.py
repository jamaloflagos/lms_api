# myapp/middleware.py
import logging

logger = logging.getLogger(__name__)

class LogRequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Print the request payload to the console
        if request.method in ['POST', 'PUT', 'PATCH']:
            logger.info("Request payload: %s", request.body)
        response = self.get_response(request)
        return response
