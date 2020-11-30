# MineArt
Simple program for translating images to MineCraft blocks

It works best with images that have been prepared with the appropriate
palette in _e.g._ Gimp, but there is a also simple guessing fallback-mode
that can be used.

```console
usage: mineart [-h] [-a] [-g] [-s SAVE] filename

Simple program for translating images to MineCraft blocks

positional arguments:
  filename              image to process

optional arguments:
  -h, --help            show this help message and exit
  -a, --abbreviate      use abbreviated names
  -g, --guess           guess colour if no match
  -s SAVE, --save SAVE  save to specified file instead of printing
```
