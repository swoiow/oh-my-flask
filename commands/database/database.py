import inspect
import os

from flask.cli import AppGroup

import utils


__doc__ = """ + Helper of database manage. """

database_cli = AppGroup("db", short_help=__doc__)


def _check_dependencies():
    try:
        import pipreqs
    except ImportError:
        RuntimeError("dependencies not found: pipreqs, please use: pkg setup")


def _create_models():
    from . import models_example

    code = inspect.getsource(models_example)
    # print(inspect.getsource(models_example))
    # print(os.path.abspath(inspect.getfile(models_example)))

    cwd = os.path.abspath(os.getcwd())
    full_path = os.path.join(cwd, "models.py")
    if not os.path.exists(full_path):
        with open(full_path, "w") as wf:
            wf.write(code)


@database_cli.command("setup")
def setup():
    """ Install packages: sqlalchemy & alembic """
    utils.install("sqlalchemy<2.0")
    utils.install("alembic")
    print("Installed sqlalchemy alembic!")
    _create_models()


@database_cli.command("dev")
def dev():
    import constants
    print(dir(constants))
