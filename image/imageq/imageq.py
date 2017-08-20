#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ImageQ script
# Glenn De Backer <glenn@simplicity.be>
# Last update: 20/08/2017
#
# Filters out images that does not meet certain resolution requirements
#
# usage: python imageq.py image_dir 800x600
#
from __future__ import print_function
import os
import struct
import argparse
import re


class termCodes:
    """
    Ansi terminal codes
    """
    NEWLINE       = '\n'
    ENDC          = '\033[0m'
    COLOR_OK      = '\033[92m'
    COLOR_FAIL    = '\033[91m'


def get_image_size(file_path):
    """
    Return image size

    Args:
        file_path (str): path to an image file

    Returns:
        width (int): widht of the image
        height (int): height of the image
    """
    width = -1
    height = -1
    size = os.path.getsize(file_path)

    with open(file_path, "rb") as input:
        data = input.read(26)

        if ((size >= 24) and data.startswith(b'\211PNG\r\n\032\n') and (data[12:16] == b'IHDR')):
            # PNGs
            w, h = struct.unpack(">LL", data[16:24])
            width = int(w)
            height = int(h)
        elif (size >= 16) and data.startswith(b'\211PNG\r\n\032\n'):
            # older PNGs
            w, h = struct.unpack(">LL", data[8:16])
            width = int(w)
            height = int(h)
        elif (size >= 2) and data.startswith(b'\377\330'):
            # JPEG
            imgtype = JPEG
            input.seek(0)
            input.read(2)
            b = input.read(1)

            while (b and ord(b) != 0xDA):
                while (ord(b) != 0xFF):
                    b = input.read(1)
                while (ord(b) == 0xFF):
                    b = input.read(1)
                if (ord(b) >= 0xC0 and ord(b) <= 0xC3):
                    input.read(3)
                    h, w = struct.unpack(">HH", input.read(4))
                    break
                else:
                    input.read(
                        int(struct.unpack(">H", input.read(2))[0]) - 2)
                b = input.read(1)
            width = int(w)
            height = int(h)

    return width, height

def get_resolution(resolution):
    minimum_width = -1
    minimum_height = -1

    matches = re.match(r"([0-9]+?)x([0-9]+)", resolution)

    if matches:
        minimum_width  = int(matches.group(1))
        minimum_height = int(matches.group(2))

    return minimum_width, minimum_height


def main():
    unfit_images = []

    # setup cli parser
    parser = argparse.ArgumentParser(description='Check if images meet resolution requirements')
    parser.add_argument("image_directory", help="directory containing images")
    parser.add_argument("min_resolution", help="minum resolution e.g 800x600 / 0x600")
    args = parser.parse_args()

    # get mini and maximum resolution
    minimum_width, minimum_height = get_resolution(args.min_resolution)

    if minimum_width is not -1:
        # check if directory exists
        if os.path.isdir(args.image_directory):
            # list files im target directory
            for filename in os.listdir(args.image_directory):
                # check if it is an image
                if re.match('.*\.jpg|.*\.jpeg|.*\.png$', filename):
                    # get image dimensions
                    width, height = get_image_size(os.path.join(args.image_directory, filename))

                    # check if image meets resolutions requirement
                    if width < minimum_width or height < minimum_height:
                        unfit_images.append({'filename' : filename, 'width' : width, 'height' : height})

            # print unfit images
            if len(unfit_images) > 0:
                print("Images that does not meet the minimum resolution requirements:\n")
                for image in unfit_images:
                    print("* {0} [{1}x{2}]".format(image['filename'], image['width'], image['height']))
                print("\n")
            else:
                print(termCodes.COLOR_OK + "All images meet the minimum resolution requirements!" + termCodes.ENDC)

        else:
            print(termCodes.COLOR_FAIL + "[ERROR] Image directory not found!" + termCodes.ENDC)
    else:
        print(termCodes.COLOR_FAIL + "[ERROR] Minimum resolution is not correct!" + termCodes.ENDC)

if __name__ == "__main__":
    main()


#print(termColors.BOLD + "Warning: No active frommets remain. Continue?" + termColors.ENDC)
