from collections import defaultdict
from functools import partial

import click
from flask.cli import AppGroup

import utils


__doc__ = """ + Helper of packages manage. Such as sync/reset. """

pkg_cli = AppGroup("pkg", short_help=__doc__)
cmd = partial(pkg_cli.command, with_appcontext=False)


def _check_dependencies():
    try:
        import pipreqs
    except ImportError:
        RuntimeError("dependencies not found: pipreqs, please use: pkg setup")


@cmd("setup")
@click.argument("ver", required=False, default="0.4.12")
def setup(ver=None):
    """ Install packages: pipreqs """
    utils.install(f"pipreqs=={ver}")
    print("Installed pipreqs!")


@cmd("sync")
@click.argument("path", required=False)
def sync_requirements(path=None):
    """ Sync packages to requirements.txt """
    _check_dependencies()
    from pipreqs import pipreqs
    args = defaultdict(
        lambda: None,
        {"--force": True, "--mode": "compat", "<path>": path}
    )
    pipreqs.init(args)
