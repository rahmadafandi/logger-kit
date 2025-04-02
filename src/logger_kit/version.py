import tomli


def get_pyproject():
    with open("pyproject.toml", "rb") as f:
        return tomli.load(f)


__version__ = get_pyproject()["project"]["version"]
__author__ = get_pyproject()["project"]["authors"][0]["name"]
__author_email__ = get_pyproject()["project"]["authors"][0]["email"]
__license__ = get_pyproject()["project"]["license"]
__copyright__ = get_pyproject()["project"]["copyright"]
