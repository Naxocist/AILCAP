OPENSLIDE_PATH = "D:/NSC2024_dataset/openslide-bin-4.0.0.2-windows-x64/bin"

import os

# Windows 
with os.add_dll_directory(OPENSLIDE_PATH):
    import openslide

from openslide import open_slide, OpenSlide
from openslide.deepzoom import DeepZoomGenerator

from PIL import Image
import numpy as np
from matplotlib import pyplot as plt
from math import log2
import glob

import json

if __name__ == "__main__":
    # Load the svs slide into an object.

    slide = open_slide('D:/NSC2024_dataset/svs/S56-01604_phD_B.svs')


    tiles = DeepZoomGenerator(slide, limit_bounds=True)

    print(slide.dimensions)
    print()
    print(slide.level_dimensions)
    print(slide.level_downsamples)
    print()

    lvl = 3

    level_dims = slide.level_dimensions[lvl]

    level_img = slide.read_region((0, 0), lvl, level_dims)

    level_img_rgb = level_img.convert('RGB')
    # level_img_rgb.show()


    dz = DeepZoomGenerator(slide, tile_size=256, overlap=0)

    lvl = 15
    tile = dz.get_tile(lvl, (30, 70)).convert('RGB')
    pos = dz.get_tile_coordinates(lvl, (30, 70))

    print(dz.level_dimensions)
    print(dz.level_tiles)
    print(pos)

    a, b, c = pos
    region = slide.read_region(a, b, c).convert('RGB')
    region.show()

    W, H = slide.dimensions
    w, h = c
    print(f"[width] from {W} we get just {w}")
    print(f"[height] from {H} we get just {h}")


    zw = log2(W/w)
    zh = log2(H/h)

    print(W/w, H/h)
