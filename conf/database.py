from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from conf import settings

database_url = "mysql+{DRIVER}://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}".format(
    **settings.DATABASE
)

database_engine_instance = create_engine(
    database_url, encoding="utf8",
    pool_recycle=settings.DB_POOL_RECYCLE,
    echo=settings.DB_SQL_LOGGING_ECHO,
)

# The sessionmaker factory should be used just once in
# your application global scope, and treated like a configuration setting

SessionFactory = sessionmaker(
        bind=database_engine_instance,
        autoflush=False,
        expire_on_commit=False,
        autocommit=False,
    )

Session = SessionFactory

_SessionScoped = scoped_session(SessionFactory)


class SessionContext(object):

    def __init__(self):
        pass

    def __enter__(self):
        self._session_instance = _SessionScoped()
        return self._session_instance

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        有异常的情况下，不要去提交
        :param exc_type: 
        :param exc_val: 
        :param exc_tb: 
        :return: 
        """

        if exc_tb:
            self._session_instance.close()
            raise exc_tb

        try:
            self._session_instance.commit()
        except Exception as e:
            self._session_instance.rollback()
            raise e
        finally:
            self._session_instance.close()
