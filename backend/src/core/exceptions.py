class TagYoureItBackendException(Exception):
    pass


class ObjectNotFound(TagYoureItBackendException):
    pass


class TagTimeNullError(TagYoureItBackendException):
    pass
