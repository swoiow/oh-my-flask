import inspect
import os
from functools import partial

import click
from flask.cli import AppGroup

import utils


CORE_DEPS = "gunicorn"

__doc__ = """ + Run Flask with WSGI HTTP Server. """

prd_cli = AppGroup("prd", short_help=__doc__)
cmd = partial(prd_cli.command, with_appcontext=False)


def _create_gunicorn_conf():
    from . import gunicorn_example

    code = inspect.getsource(gunicorn_example)
    cwd = os.path.abspath(os.getcwd())
    with open(os.path.join(cwd, "gunicorn.conf.py"), "w") as wf:
        wf.write(code)


@cmd("setup")
@click.argument("ver", required=False, default="20.1.0")
def setup(ver=None):
    """ Install package: gunicorn """

    utils.install(f"{CORE_DEPS}=={ver}")
    _create_gunicorn_conf()
    print("Installed gunicorn!")


@cmd("run")
def run():
    """ Run gunicorn """
    from gunicorn.app import wsgiapp
    wsgiapp.run()
