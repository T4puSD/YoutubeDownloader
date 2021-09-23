class NotFoundException(Exception):
    """Raised when a value is expected but not present"""
    pass


class IllegalArgumentException(Exception):
    """Raised when an expected argument is not valid"""
    pass
