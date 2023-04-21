from .core import *
from .database import *
from .demo import *
from .pkg import *


__omf_cli__ = [
    "init=commands:init_project",
    "pkg=commands:pkg_cli",
    "db=commands:database_cli",
    "demo=commands:demo_cli",
]
