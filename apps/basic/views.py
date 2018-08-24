import tornado.web

from conf import Session
from apps.basic.exceptions import APIException

import logging
import uuid


class BasicModelRequestHandler(tornado.web.RequestHandler):
    """
    所有的request handler要继承该类
    """
    model_class = None

    def get_queryset(self):

        return self.session.query(self.model_class).filter_by(obj_deleted=False)

    def initialize(self):

        assert self.model_class is not None, (
            "'{0}' should define `model_class` attribute".format(self.__class__.__name__)
        )

        self.logger = logging.getLogger(__name__)

    def prepare(self):

        self.session = Session()

        self.request_id = "{0}".format(uuid.uuid4())

    def on_finish(self):

        self.session.close()

    def write(self, chunk, correct_response=True):
        """
        :param chunk:
        :param correct_response: 当前响应是否为正确的响应
        :return:
        """
        if correct_response:
            data = {
                'RequestId': self.request_id,
                'Data': chunk,
            }
            return super(BasicModelRequestHandler, self).write(data)
        else:
            return super(BasicModelRequestHandler, self).write(chunk)

    def write_error(self, status_code, **kwargs):
        """
        重写write_error
        :param status_code:
        :param kwargs:
        :return:
        """
        exc_info = kwargs.get('exc_info', None)
        rsp_data = self.api_exception_handler(exc_info, **kwargs)
        self.write(rsp_data, correct_response=False)
        self.finish()
        self.flush()

    def api_exception_handler(self, exc_info, **kwargs):
        """
        :param exc_info:
        :param kwargs:
        :return: error response content
        """
        request_id = getattr(self, "request_id", "")
        data = kwargs.get("data", None)
        message = kwargs.get("message", None)
        reason = kwargs.get("reason", None)

        if exc_info and isinstance(exc_info, tuple) and len(exc_info) == 3:
            exc = exc_info[1]
            # 自定义的异常
            if isinstance(exc, APIException):
                reason = exc.reason
                message = exc.message
                data = exc.data

            # 代码内部异常
            elif isinstance(exc, Exception):
                reason = "{0}".format(exc.__class__.__name__)
                message = "{0}".format(exc)
                data = None

        rsp_data = {
            'RequestId': request_id,
            'Error': {
                "Data": data,
                "Message": message,
                "Reason": reason,
            }
        }
        self.logger.error(rsp_data)
        return rsp_data

    def throw(self, status_code=500, **kwargs):
        """
        自定义异常
        :param status_code:
        :param kwargs:
        :return:
        """
        self.send_error(status_code=status_code, **kwargs)

    def get(self, pk):
        instance = self.get_queryset().get(pk)

        if not instance:
            raise Exception("Not Found")

        self.set_status(200)

        self.write(instance.serializer())

