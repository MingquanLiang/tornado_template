import sys

from apps.ext.models import DeclarativeBaseModel
from conf import database_engine_instance


def create_table():
    print("creating all table ...")
    DeclarativeBaseModel.metadata.create_all(database_engine_instance)


def shell():
    print("in shell")
    from IPython import start_ipython
    start_ipython(argv=[])


if __name__ == "__main__":
    try:
        command = sys.argv[1]
    except IndexError:
        print("python manage.py {0}".format("$command"))
        sys.exit(0)
    print("command is", command)
    exec("{0}()".format(command))
