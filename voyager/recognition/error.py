

class BaseError(Exception):
    """Base class for exceptions in this module."""

    def __init__(self, message=""):
        self.message = message

    def __repr__(self):
        return repr(self.message)

class TemplateInputError(BaseError):
    """Resolution input is not right."""