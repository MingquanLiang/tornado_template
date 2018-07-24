from pymongo import MongoClient
from tcenter.models.options import TaskStatusOption
from conf import settings


class MongodbHandler(object):

    def __enter__(self):
        self.handler = TaskResultHandler(**settings.MONGODB)
        return self.handler

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.handler:
            self.handler.close()


class TaskResultHandler(object):

    result_key = 'task_result'

    status_options = {i for i in TaskStatusOption.__members__.keys()}

    def __init__(self, host=None, port=None, db_name=None, collection=None):
        """
        :param host: use host and port to connect mongod 
        :param port: use host and port to connect mongod 
        :param db_name: db name
        :param collection: collection name
        """
        self.con = MongoClient(host=host, port=port)
        self.db = self.con.get_database(db_name)
        self.collection = self.db.get_collection(collection)

    def insert_init_document(self, _id, **kwargs):
        """
        在任务初始化时插入的数据
        :param _id: 主键，应该和任务的id是一致的
        :param kwargs: 额外的数据, such as group, server等数据
        """
        data = {"_id": _id, self.result_key: {}}

        for status in self.status_options:
            data[self.result_key][status] = []

        data.update(**kwargs)
        self.collection.insert_one(data)

    def update_status_result(self, _id, status, status_result):
        """
        :param _id: 主键，应该和任务的id是一致的
        :param status: 任务状态
        :param status_result: 某个任务状态对应的结果 
        """
        assert status in self.status_options, "status must be in {0}".format(
            self.status_options
        )
        status_key = "{0}.{1}".format(self.result_key, status)
        self.collection.update_one(
            {"_id": _id}, {
                "$set": {status_key: status_result}
            }
        )

    def close(self):
        if self.con:
            self.con.close()
