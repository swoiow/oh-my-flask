from functools import partial

import click
from flask.cli import AppGroup


__doc__ = """ + Manage of venv. """

venv_cli = AppGroup("venv", short_help=__doc__)
cmd = partial(venv_cli.command, with_appcontext=False)


def _check_dependencies():
    try:
        import venv
    except ImportError:
        RuntimeError("dependencies not found: venv, please upgrade your Python >= 3.3.")


@cmd("create")
@click.argument("venv_dir_name", required=False, default=".venv")
def create_venv(venv_dir_name):
    """ Create venv in current folder. """
    _check_dependencies()
    import venv

    venv.create(venv_dir_name)
    print("Installed .venv in current folder! ")


@cmd("reset")
def reset_venv():
    """ Reset venv packages. Remove all the packages, and install with requirements.txt """
    print("pip uninstall -y -r <(pip freeze)")
