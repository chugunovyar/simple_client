from logging import Logger

from tools.logs import get_logger


def test_logs():
    _l = get_logger()
    assert isinstance(_l, Logger)
