import argparse
from contextlib import contextmanager
from datetime import timedelta, timezone
import re

from gi.repository import GExiv2


TIME_FORMAT = '%Y:%m:%d %H:%M:%S'


TIMEZONE_REGEX = re.compile(
    r'''(?P<sign>[+-])           # Sign
        (?P<hours>\d{1,2})       # Hours offset
        (?:(?P<minutes>\d{2}))?  # Optional minutes offset''',
    re.VERBOSE
)


def argparse_timezone(timezone_str):
    match = TIMEZONE_REGEX.match(timezone_str)
    if not match:
        msg = 'Invalid timezone format: {}'.format(timezone_str)
        raise argparse.ArgumentTypeError(msg)

    hours = int(match.group('hours'))
    minutes = int(match.group('minutes') or 0)
    offset = timedelta(hours=hours, minutes=minutes)

    if hours > 12 or minutes > 59 or (hours == 12 and minutes > 0):
        msg = 'Invalid timezone offset: {}'.format(timezone_str)
        raise argparse.ArgumentTypeError(msg)

    sign = match.group('sign')
    if sign == '-':
        offset = -offset

    return timezone(offset)


@contextmanager
def edit_exif(filename):
    exif = GExiv2.Metadata(filename)
    yield exif
    exif.save_file()
