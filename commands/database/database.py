import inspect
import os
from functools import wraps

import click
from flask.cli import AppGroup

import utils


__doc__ = """ + A simple helper of database manage. PowerBy alembic. """

database_cli = AppGroup("db", short_help=__doc__)


def _check_dependencies():
    try:
        import pipreqs
    except ImportError:
        RuntimeError("dependencies not found: pipreqs, please use: pkg setup")


def _create_models():
    from commands.database.tpl import models_example as example

    code = inspect.getsource(example)
    # print(inspect.getsource(models_example))
    # print(os.path.abspath(inspect.getfile(models_example)))
    project_working_dir = os.path.abspath(os.getcwd())
    full_path = os.path.join(project_working_dir, "models.py")
    if not os.path.exists(full_path):
        with open(full_path, "w") as wf:
            wf.write(code)


def _create_database():
    from commands.database.tpl import database_example as example

    code = inspect.getsource(example)
    project_working_dir = os.path.abspath(os.getcwd())
    full_path = os.path.join(project_working_dir, "database.py")
    if not os.path.exists(full_path):
        with open(full_path, "w") as wf:
            wf.write(code)


@database_cli.command("setup")
@click.argument("path", required=False, default="migrations")
def setup(path):
    """ Install packages: sqlalchemy & alembic """
    if not utils.check_package("sqlalchemy"):
        utils.install("sqlalchemy<2.0")
    if not utils.check_package("alembic"):
        utils.install("alembic~=1.10")
    _create_models()
    _create_database()
    _setup_alembic(path)
    print("Installed sqlalchemy alembic!")


def _setup_alembic(path):
    from alembic import command
    from alembic.config import Config
    alembic_cfg = Config("alembic.ini")
    command.init(alembic_cfg, path)

    new_lines = """import models\ntarget_metadata = models.Base.metadata\n\n"""
    with open(os.path.join(path, "env.py"), "r+") as rw:
        lines = rw.readlines()
        rw.seek(0)
        rw.write("".join([new_lines if l.startswith("target_metadata =") else l for l in lines]))


def with_alembic_ctx(func):
    @wraps(func)
    def swrap(*args, **kwargs):
        import omf

        from database import engine
        from alembic.config import Config
        alembic_cfg = Config("alembic.ini")

        config_args = omf.DATABASES.get("alembic_options", {})
        for k, v in config_args.items():
            alembic_cfg.set_main_option(k, v)
        if "sqlalchemy.url" not in config_args:
            alembic_cfg.set_main_option("sqlalchemy.url", str(engine.url))
            config_args["sqlalchemy.url"] = str(engine.url)
        alembic_cfg.config_args = config_args
        kwargs["_alembic_cfg"] = alembic_cfg
        return func(*args, **kwargs)

    return swrap


@database_cli.command("makemigrations")
@click.argument("comment", required=True)
@click.argument("is_autogenerate", required=False, default=True)
@with_alembic_ctx
def makemigrations(
    comment, is_autogenerate,
    _alembic_cfg, **kwargs
):
    """ Commit models change to a version """

    from alembic import command

    command.revision(
        _alembic_cfg,
        message=comment,
        autogenerate=is_autogenerate,
    )


@database_cli.command("migrate")
@click.argument("revision", required=False, default="head")
@click.argument("sql", required=False, default=False)
@with_alembic_ctx
def migrate(
    revision, sql,
    _alembic_cfg, **kwargs
):
    """ Push a version(models changed) to database """
    from alembic import command

    command.upgrade(_alembic_cfg, revision=revision, sql=sql)


@database_cli.command("upgrade")
@click.argument("src_rev", required=True)
@click.argument("dst_rev", required=True)
@click.argument("sql", required=False, default=False)
@with_alembic_ctx
def upgrade(
    src_rev, dst_rev, sql,
    _alembic_cfg, **kwargs
):
    """ Do upgrade action with Revision ID """
    from alembic import command

    command.upgrade(_alembic_cfg, revision=f"{src_rev}:{dst_rev}", sql=sql)


@database_cli.command("downgrade")
@click.argument("revision", required=True)
@click.argument("sql", required=False, default=False)
@with_alembic_ctx
def downgrade(
    revision, sql,
    _alembic_cfg, **kwargs
):
    """ Do downgrade action with Revision ID """
    from alembic import command

    command.downgrade(_alembic_cfg, revision=revision, sql=sql)
