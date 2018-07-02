errors = {
    "not found": 404,
    "bad request": 400,
    "authentication error": 401,
    "authorization error": 401,
    "internal server error": 500,
    "timeout": 504,
    "method not allowed": 405
}


class APIException(Exception):

    def __init__(self, message):
        if ":" not in message:
            self.message = "Internal server error: "+ message +" (unclassified error)"
        else:
            self.message = message
        self.code = self._get_code(message)

    def _get_code(self, message):
        """ Assign error code based on error message """
        error_type = message.split(":")[0].lower()
        
        code = errors.get(error_type, 500)
        return code

