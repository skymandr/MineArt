#! /usr/bin/env python3
"""mineart.py: Simple program for translating images to MineCraft blocks
    Copyright (C) 2020 Andreas Skyman

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
from argparse import ArgumentParser
from math import sqrt
from typing import Optional, Tuple

from PIL import Image

UNKNOWN = ("UNKN.", 0, "UNKNOWN", (0, 0, 0))
COLOURS = (
    ("ABBR.", 1, "GRASS", (127, 178, 56)),
    ("ABBR.", 2, "SAND", (47, 233, 163)),
    ("ABBR.", 3, "WOOL", (199, 199, 199)),
    ("ABBR.", 4, "FIRE", (255, 0, 0)),
    ("ABBR.", 5, "ICE", (160, 160, 255)),
    ("ABBR.", 6, "METAL", (167, 167, 167)),
    ("ABBR.", 7, "PLANT", (0, 124, 0)),
    ("ABBR.", 8, "SNOW", (255, 255, 255)),
    ("ABBR.", 9, "CLAY", (164, 168, 184)),
    ("ABBR.", 10, "DIRT", (151, 109, 77)),
    ("ABBR.", 11, "STONE", (112, 112, 112)),
    ("ABBR.", 12, "WATER", (64, 64, 255)),
    ("ABBR.", 13, "WOOD", (143, 119, 72)),
    ("ABBR.", 14, "QUARTZ", (255, 252, 245)),
    ("ABBR.", 15, "COLOR_ORANGE", (216, 127, 51)),
    ("ABBR.", 16, "COLOR_MAGENTA", (178, 76, 216)),
    ("ABBR.", 17, "COLOR_LIGHT_BLUE", (102, 153, 216)),
    ("ABBR.", 18, "COLOR_YELLOW", (229, 229, 51)),
    ("ABBR.", 19, "COLOR_LIGHT_GREEN", (127, 204, 25)),
    ("ABBR.", 20, "COLOR_PINK", (242, 127, 165)),
    ("ABBR.", 21, "COLOR_GRAY", (76, 76, 76)),
    ("ABBR.", 22, "COLOR_LIGHT_GRAY", (153, 153, 153)),
    ("ABBR.", 23, "COLOR_CYAN", (76, 127, 153)),
    ("ABBR.", 24, "COLOR_PURPLE", (127, 63, 178)),
    ("ABBR.", 25, "COLOR_BLUE", (51, 76, 178)),
    ("ABBR.", 26, "COLOR_BROWN", (102, 76, 51)),
    ("ABBR.", 27, "COLOR_GREEN", (102, 127, 51)),
    ("ABBR.", 28, "COLOR_RED", (153, 51, 51)),
    ("ABBR.", 29, "COLOR_BLACK", (25, 25, 25)),
    ("ABBR.", 30, "GOLD", (250, 238, 77)),
    ("ABBR.", 31, "DIAMOND", (92, 219, 213)),
    ("ABBR.", 32, "LAPIS", (74, 128, 255)),
    ("ABBR.", 33, "EMERALD", (0, 217, 58)),
    ("ABBR.", 34, "PODZOL", (129, 86, 49)),
    ("ABBR.", 35, "NETHER", (112, 2, 0)),
    ("ABBR.", 36, "TERRACOTTA_WHITE", (209, 177, 161)),
    ("ABBR.", 37, "TERRACOTTA_ORANGE", (159, 82, 36)),
    ("ABBR.", 38, "TERRACOTTA_MAGENTA", (149, 87, 108)),
    ("ABBR.", 39, "TERRACOTTA_LIGHT_BLUE", (112, 108, 138)),
    ("ABBR.", 40, "TERRACOTTA_YELLOW", (186, 133, 36)),
    ("ABBR.", 41, "TERRACOTTA_LIGHT_GREEN", (103, 117, 53)),
    ("ABBR.", 42, "TERRACOTTA_PINK", (160, 77, 78)),
    ("ABBR.", 43, "TERRACOTTA_GRAY", (57, 41, 35)),
    ("ABBR.", 44, "TERRACOTTA_LIGHT_GRAY", (135, 107, 98)),
    ("ABBR.", 45, "TERRACOTTA_CYAN", (87, 92, 92)),
    ("ABBR.", 46, "TERRACOTTA_PURPLE", (122, 73, 88)),
    ("ABBR.", 47, "TERRACOTTA_BLUE", (76, 62, 92)),
    ("ABBR.", 48, "TERRACOTTA_BROWN", (76, 50, 35)),
    ("ABBR.", 49, "TERRACOTTA_GREEN", (76, 82, 42)),
    ("ABBR.", 50, "TERRACOTTA_RED", (142, 60, 46)),
    ("ABBR.", 51, "TERRACOTTA_BLACK", (37, 22, 16)),
    ("ABBR.", 52, "CRIMSON_NYLIUM", (189, 48, 49)),
    ("ABBR.", 53, "CRIMSON_STEM", (148, 63, 97)),
    ("ABBR.", 54, "CRIMSON_HYPHAE", (92, 25, 29)),
    ("ABBR.", 55, "WARPED_NYLIUM", (22, 126, 134)),
    ("ABBR.", 56, "WARPED_STEM", (58, 142, 140)),
    ("ABBR.", 57, "WARPED_HYPHAE", (86, 44, 62)),
    ("ABBR.", 58, "WARPED_WART_BLOCK", (20, 180, 133)),
 )


def get_distance(
    rgb1: Tuple[int, int, int],
    rgb2: Tuple[int, int, int],
) -> float:
    return sqrt(
        (rgb2[0] - rgb1[0]) ** 2
        + (rgb2[1] - rgb1[1]) ** 2
        + (rgb2[2] - rgb1[2]) ** 2
    )


def get_best_guess(rgb: Tuple[int, int, int]) -> tuple:
    distances = [get_distance(c[-1], rgb) for c in COLOURS]
    dmin = None
    imin = None
    for i, d in enumerate(distances):
        if dmin is None or d < dmin:
            dmin = d
            imin = i
    return COLOURS[imin]


def get_colour(
    rgb: Tuple[int, int, int],
    guess: bool = False,
) -> Optional[tuple]:
    if guess:
        return get_best_guess(rgb)
    else:
        for c in COLOURS:
            if c[-1] == rgb:
                return c
    return None


def print_image(
    filename: str,
    use_abbr: bool = False,
    guess: bool = False,
) -> None:
    with Image.open(filename) as im:
        rgb_im = im.convert("RGB")
    if use_abbr:
        ind = 0
    else:
        ind = 2

    for y in range(rgb_im.height):
        for x in range(rgb_im.width):
            rgb = rgb_im.getpixel((x, y))
            colour = get_colour(rgb, guess)
            if colour is not None:
                print(f"{colour[ind]} ", end="")
            else:
                print(f"{UNKNOWN[ind]} ", end="")
        print("")


def save_image(
    filename: str,
    savename: str,
    use_abbr: bool = False,
    guess: bool = False,
) -> None:
    with Image.open(filename) as im:
        rgb_im = im.convert("RGB")
    if use_abbr:
        ind = 0
    else:
        ind = 2

    with open(savename, 'w') as savefile:
        for y in range(rgb_im.height):
            for x in range(rgb_im.width):
                rgb = rgb_im.getpixel((x, y))
                colour = get_colour(rgb, guess)
                if colour is not None:
                    savefile.write(f"{colour[ind]} ")
                else:
                    savefile.write(f"{UNKNOWN[ind]} ")
            savefile.write("\n")


def main() -> int:
    parser = ArgumentParser(
        "mineart",
        description="Simple program for translating images to MineCraft blocks",
    )
    parser.add_argument(
        "filename",
        type=str,
        help="image to process",
    )
    parser.add_argument(
        "-a", "--abbreviate",
        action="store_true",
        default=False,
        help="use abbreviated names",
    )
    parser.add_argument(
        "-g", "--guess",
        action="store_true",
        default=False,
        help="guess color if no match",
    )
    parser.add_argument(
        "-s", "--save",
        action="store",
        type=str,
        help="save to specified file instead of printing",
    )
    args = parser.parse_args()
    try:
        if args.save is None:
            print_image(args.filename, args.abbreviate, args.guess)
        else:
            save_image(args.filename, args.save, args.abbreviate, args.guess)
    except Exception as err:
       print(f"Runtime error: {err}")
    return 0


if __name__ == "__main__":
    exit(main())
