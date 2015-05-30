import argparse
import bisect
from datetime import datetime
import itertools
import json

from gi.repository import GExiv2

from . import utils


EXIF_DATE_TIME_FIELD = 'Exif.Image.DateTime'


def add_geotag(timestamps, locations, tzinfo, exif):
    time = get_image_utc_time(exif, tzinfo)
    latitude, longitude = get_gps(timestamps, locations, time)
    exif.set_gps_info(longitude, latitude, 0)


def read_location_history(location_file, tzinfo):
    with open(location_file) as f:
        locations = json.load(f)['locations']
    locations.reverse()
    timestamps = [
        datetime.fromtimestamp(
            int(location['timestampMs']) / 1000, tz=tzinfo
        ).timestamp()
        for location in locations
    ]
    latlongs = [
        (location['latitudeE7'] / 10000000, location['longitudeE7'] / 10000000)
        for location in locations
    ]

    data_point_num = len(timestamps)
    low_timestamps = itertools.islice(iter(timestamps), data_point_num - 1)
    high_timestamps = itertools.islice(iter(timestamps), 0, data_point_num)
    timestamp_boundary = [(low + high) / 2
                          for low, high in zip(low_timestamps, high_timestamps)]
    return timestamp_boundary, latlongs


def get_gps(timestamps, locations, target_time):
    index = bisect.bisect_left(timestamps, target_time)
    return locations[index]


def get_image_utc_time(exif, tzinfo):
    time_str = exif[EXIF_DATE_TIME_FIELD]
    time = datetime.strptime(time_str, utils.TIME_FORMAT)
    tz_aware_time = time.replace(tzinfo=tzinfo)
    timestamp = tz_aware_time.timestamp()
    return timestamp


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Add geo tag to photo using Google location history'
    )
    parser.add_argument('location_history', help='Location history JSON file')
    parser.add_argument('location_history_timezone',
                        type=utils.argparse_timezone,
                        help='Location history timezone')
    parser.add_argument('photo_timezone',
                        type=utils.argparse_timezone,
                        help='Timezone of time recorded in the photo')
    parser.add_argument('filenames', nargs='+', help='File names of photos')

    args = parser.parse_args()

    timestamps, locations = read_location_history(
        args.location_history, args.location_history_timezone
    )

    for filename in args.filenames:
        with utils.edit_exif(filename) as exif:
            add_geotag(timestamps, locations, args.photo_timezone, exif)
