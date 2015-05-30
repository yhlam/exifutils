import argparse
from datetime import datetime

from gi.repository import GExiv2

from . import utils


EXIF_DATE_TIME_FIELDS = (
    'Exif.Image.DateTime',
    'Exif.Photo.DateTimeDigitized',
    'Exif.Photo.DateTimeOriginal',
)


def fix_image_time(photo_timezone, target_timezone, exif):
    for field in EXIF_DATE_TIME_FIELDS:
        fix_image_time_field(photo_timezone, target_timezone, field, exif)


def fix_image_time_field(photo_timezone, target_timezone, field, exif):
    try:
        time_str = exif[field]
    except KeyError:
        return

    time = datetime.strptime(time_str, utils.TIME_FORMAT)
    tz_aware_time = time.replace(tzinfo=photo_timezone)
    new_time = tz_aware_time.astimezone(target_timezone)
    new_time_str = datetime.strftime(new_time, utils.TIME_FORMAT)
    exif[field] = new_time_str


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Change the timezone of photos'
    )
    parser.add_argument('photo_timezone',
                        type=utils.argparse_timezone,
                        help='Timezone of time recorded in the photo')
    parser.add_argument('target_timezone',
                        type=utils.argparse_timezone,
                        help='Target timezone')
    parser.add_argument('filenames', nargs='+', help='File names of photos')

    args = parser.parse_args()

    for filename in args.filenames:
        with utils.edit_exif(filename) as exif:
            fix_image_time(args.photo_timezone, args.target_timezone, exif)
