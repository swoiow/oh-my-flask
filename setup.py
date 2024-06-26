from setuptools import setup

from commands import __omf_cli__


__name__ = "oh-my-flask"
__version__ = "1.0"

setup(
    name=__name__,
    version=__version__,
    url="https://github.com/harmonsir/oh-my-flask",
    license="MIT",
    author="HarmonSir",
    author_email="mail.me@pylab.me",
    description="make flask as same as Django, but much easier.",

    entry_points={
        "flask.commands": __omf_cli__,
        # "console_scripts": [
        #     "omf=commands:init_project",
        #     "oh-my-flask=commands:init_project",
        # ],
    },

    packages=[
        "commands",
        "utils"
    ],
    python_requires=">3.6",
    install_requires=[
        "Flask>2,<3"
    ]
)
