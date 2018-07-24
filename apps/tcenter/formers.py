from sqlalchemy import Column, DateTime, String, SmallInteger


class BasicTaskFormer(object):

    # task status options
    NOTSTART, PENDING, RUNNING, SUCCESS, FAILURE, RETRY = (
        1, 2, 3, 4, 5, 6
    )

    # 对用户可见的任务类型
    AUTH, CANCEL_AUTH, APPLICATION, TEMPLATE, METHOD, JOB_ARRANGE = (
        1, 2, 3, 4, 5, 6
    )

    # 作业编排中的子任务的类型
    JOB_INIT, JOB_CHECK, JOB_APPLICATION, JOB_TEMPLATE, JOB_METHOD = (
        10, 11, 12, 13, 14
    )

    task_uuid = Column(type_=String(length=50), nullable=False, doc="任务唯一标识")

    task_status = Column(type_=SmallInteger, default=NOTSTART, nullable=False, doc="任务状态")

    task_type = Column(type_=SmallInteger, nullable=False, doc="任务类型")

    task_start_time = Column(type_=DateTime, nullable=False, doc="任务开始时间")

    task_end_time = Column(type_=DateTime, nullable=False, doc="任务结束时间")

