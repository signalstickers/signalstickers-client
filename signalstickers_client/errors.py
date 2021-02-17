class SignalException(Exception):
    """Base class for all exceptions explicitly raised by this library."""

class HTTPException(SignalException):
    """Base class for all exceptions caused by HTTP errors"""
    def __init__(self, response, message):
        self.response = response
        self.status_code = response.status_code
        super().__init__(f'{response.status_code}: {message}')

class NotFound(HTTPException):
    pass

class Unauthorized(HTTPException):
    pass

class RateLimited(HTTPException):
    pass
