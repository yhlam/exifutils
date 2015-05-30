#########
exifutils
#########
Command line tools to update EXIF tags


Dependencies
============
This project uses gexiv2 to update EXIF tags. See https://wiki.gnome.org/Projects/gexiv2 for installation details.

exifutils requires Python 3.


Usage
=====

Change timezone of date times stored in EXIF tags
-------------------------------------------------

::

  python -m exifutils.adjust_timezone [-h] photo_timezone target_timezone filenames [filenames ...]

  positional arguments:
    photo_timezone   Timezone of time recorded in the photo
    target_timezone  Target timezone
    filenames        File names of photos

  optional arguments:
    -h, --help       show the help message and exit


Add geo tag to photo using Google location history
--------------------------------------------------

The Google location history JSON file can be downloaded from Google takeout.

::

  python -m exifutils.add_geotag [-h] location_history location_history_timezone photo_timezone filenames [filenames ...]

  positional arguments:
    location_history           Location history JSON file
    location_history_timezone  Location history timezone
    photo_timezone             Timezone of time recorded in the photo
    filenames                  File names of photos

  optional arguments:
    -h, --help            show the help message and exit


Timezone Argument
-----------------

The timezone argument should be in "+HH[:MM]" or "-HH[:MM]" format. For example,
"+8", "+8:00", "+08:00" and "-08:00" are all valid timezone input.
