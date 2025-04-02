from importlib.metadata import version

from logger_kit import (
    __author__,
    __author_email__,
    __copyright__,
    __license__,
    __version__,
)


def test_version():
    assert __version__ == version("logger-kit")


def test_author():
    assert __author__ == "Rahmad Afandi"


def test_author_email():
    assert __author_email__ == "rahmadafandiii@gmail.com"


def test_copyright():
    assert __copyright__ == "2025, Rahmad Afandi"


def test_license():
    assert __license__ == "MIT"
