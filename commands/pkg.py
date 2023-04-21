from collections import defaultdict

import click
from flask.cli import AppGroup

import utils


__doc__ = """ + Helper of packages manage. """

pkg_cli = AppGroup("pkg", short_help=__doc__)


def _check_dependencies():
    try:
        import pipreqs
    except ImportError:
        RuntimeError("dependencies not found: pipreqs, please use: pkg setup")


@pkg_cli.command("setup")
def setup():
    """ Install packages: pipreqs """
    utils.install("pipreqs==0.4.12")
    print("Installed pipreqs!")


@pkg_cli.command("sync")
@click.argument("path", required=False)
def sync_requirements(path=None):
    """ Sync packages to requirements.txt """
    _check_dependencies()
    from pipreqs import pipreqs
    args = defaultdict(lambda: None, {"--force": True, "--mode": "compat", "<path>": path})
    pipreqs.init(args)


@pkg_cli.command("reset")
def reset_venv():
    """ Reset venv packages. Remove all the packages, and install with requirements.txt """
    print("pip uninstall -y -r <(pip freeze)")
