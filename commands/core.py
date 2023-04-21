import os.path
import urllib.request

import click


static = ["static", "templates"]
core = ["setups", "blueprints", "services", "storages"]
others = ["conf"]

gitignore_url = "https://cdn.jsdelivr.net/gh/github/gitignore@main/Python.gitignore"


def _init_gitignore(fp=".gitignore"):
    body = urllib.request.urlopen(gitignore_url, timeout=30).read()
    with open(fp, "wb") as wf:
        wf.write(body)


@click.command(
    name="init"
)
def init_project():
    """ - Set up the project tree. """
    cwd = os.path.abspath(os.getcwd())
    print(f"Prepare setting up project in: {cwd}")
    for folder in static + others:
        if not os.path.exists(folder):
            os.makedirs(folder)

    for folder in core:
        if not os.path.exists(folder):
            os.makedirs(folder)
        if "__init__.py" not in os.listdir(folder):
            open(os.path.join(folder, "__init__.py"), "w").close()

    if "README.md" not in os.listdir(cwd):
        open(os.path.join(cwd, "README.md"), "w").close()

    if ".gitignore" not in os.listdir(cwd):
        _init_gitignore(os.path.join(cwd, ".gitignore"))


@click.command(
    name="audit"
)
def audit():
    pass
