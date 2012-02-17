# coding=utf-8

class StopPipeline(Exception):
    """Stop pipeline process exception.
    Raise this exception to stop the rest of the pipeline process.
    """
    pass


class DSAException(ValueError):
    """
    django-social-auth exception. This exception can be showed to user. It is thrown in normal situations – user declined
    access, access token expired, etc.
    """
    pass