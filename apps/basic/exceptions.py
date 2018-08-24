import tornado.web


class APIException(tornado.web.HTTPError):
    """
    API 异常
    """
    default_status_code = 500
    default_message = "A request error occurred."
    default_reason = "APIException"
    default_data = None

    def __init__(self, message=None, status_code=None, reason=None, **kwargs):
        self.message = message if message else self.default_message
        self.status_code = status_code if status_code else self.default_status_code
        self.reason = reason if reason else self.default_reason
        self.data = kwargs.get("data", self.default_data)

    def __str__(self):
        return "{0}".format(self.message)


class LackRequiredParameterError(APIException):
    """
    缺少必要的参数
    """
    status_code = 400
    default_message = 'Lack of Required Parameter'
    default_reason = "LackRequiredParameterError"

    def __init__(self, message=None, status_code=None, reason=None, **kwargs):
        try:
            if not message:
                message = "{default_message}: {param_name}".format(
                    default_message=self.default_message,
                    param_name=kwargs['param_name']
                )
        except KeyError:
            pass

        super(LackRequiredParameterError, self).__init__(
            message=message, status_code=status_code, reason=reason, **kwargs
        )

