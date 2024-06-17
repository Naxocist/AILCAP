# https://youtu.be/QntLBvUZR5c
"""
OpenSlide can read virtual slides in several formats:

Aperio (.svs, .tif)
Hamamatsu (.ndpi, .vms, .vmu)
Leica (.scn)
MIRAX (.mrxs)
Philips (.tiff)
Sakura (.svslide)
Trestle (.tif)
Ventana (.bif, .tif)
Generic tiled TIFF (.tif)

OpenSlide allows reading a small amount of image data at the resolution 
closest to a desired zoom level.

pip install openslide-python

then download the latest windows binaries
https://openslide.org/download/

Extract the contents to a place that you can locate later.

If you are getting the error: [WinError 126] The specified module could not be found

Open the lowlevel.py file located in:
    lib\site-packages\openslide
    
Add this at the top, after from __future__ import division, in the lowlevel.py
os.environ['PATH'] = "path+to+binary" + ";" + os.environ['PATH']
path+to+binary is the path to your windows binaries that you just downloaded.

In my case, it looks like this.

import os
os.environ['PATH'] = "C:/Users/Admin/anaconda3/envs/py37/lib/site-packages/openslide/openslide-win64-20171122/bin" + ";" + os.environ['PATH']

A few useful commands to locate the sitepackages directory

import sys
for p in sys.path:
    print(p)

"""

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
from math import floor
import glob

import json


def display_svs_information(slide):
    slide_dims = slide.dimensions # 0th level
    slide_props = slide.properties

    pretty_slide_props = json.dumps(dict(slide_props), indent=4)
    print(pretty_slide_props)

    num_lvl = slide_props['openslide.level-count']
    vendor = slide_props['openslide.vendor']
    mpp_x = slide_props['openslide.mpp-x']
    mpp_y = slide_props['openslide.mpp-y']
    objective = float(slide_props['openslide.objective-power'])
    factors = slide.level_downsamples

    print("number of levels is:", num_lvl)
    print("Vendor is:", vendor)
    print("Pixel size of X in um is:", mpp_x)
    print("Pixel size of Y in um is:", mpp_y)
    print("The objective power is: ", objective)
    print("Slide dimension: ", slide_dims)

    print("Each level is downsampled by an amount of: ", factors)


def visualize_svs(slide):
    # get dimensions of all levels
    dims = slide.level_dimensions
    num_lvl = slide.level_count

    # get a thumbnail of the image and visualize
    slide_thumb_600 = slide.get_thumbnail(size=(600, 600))

    # convert to numpy array
    slide_thumb_600_np = np.array(slide_thumb_600)
    plt.figure(figsize=(8,8))
    plt.imshow(slide_thumb_600_np)
    # plt.show()

    # Copy an image from a level
    # level3_dim = dims[2]
    # level3_img = slide.read_region((0,0), 2, level3_dim) # Pillow object, mode=RGBA

    # Convert the image to RGB
    # level3_img_RGB = level3_img.convert('RGB')
    # level3_img_RGB.show()

    # retrieve best approximated level for certain SCALE_FACTOR

    SCALE_FACTOR = 32
    best_level = slide.get_best_level_for_downsample(SCALE_FACTOR)
    print(f"level {best_level} is the best level for {SCALE_FACTOR} scale factor")


def extract(slide, file_name):

    base_dir = r'D:\NSC2024_dataset\extracted'

    try: 
        os.mkdir(base_dir + '\\' + file_name) 
    except: 
        pass

    # Deep Zoom
    tile_size = 256 # px (width, height)
    overlap = 25 # make overlap region when on sides that have a tile next to it

    tiles = DeepZoomGenerator(slide, tile_size=tile_size, overlap=overlap, limit_bounds=False)
    # print("Total number of tiles: ", tiles.tile_count)
    print("The dimensions of data in each level are: ", tiles.level_dimensions)

    num_level_tile = tiles.level_count
    print("The number of levels in the tiles object are: ", num_level_tile)
    print(tiles.level_tiles)

    # selected_levels = [i for i in range(num_level_tile)]
    selected_levels = [15]

    for level_num in selected_levels:

        x, y = tiles.level_tiles[level_num] # tile dimension
        num_tiles = x*y

        print(f"Tile dimension at level {level_num} is: ({x}, {y})")
        print(f"There are {num_tiles} tiles in level {level_num}")

        level_dir = base_dir + f'\\{file_name}\\' + str(level_num)

        if not os.path.isdir(level_dir): os.mkdir(level_dir)
        if not os.path.isdir(level_dir + '\\full'): os.mkdir(level_dir + '\\full')
        if not os.path.isdir(level_dir + '\\partial'): os.mkdir(level_dir + '\\partial')
        if not os.path.isdir(level_dir + '\\blank'): os.mkdir(level_dir + '\\blank')


        # blank_images = []
        # partial_images = []
        # full_images = []

        cnt = 0
        for col in range(x):
            for row in range(y):

                tile = tiles.get_tile(level_num, (col, row))
                tile_RGB = tile.convert('RGB')
                tile_np = np.array(tile_RGB)

                mean, std = mean_std(tile_np * 255) # mean and standard deviation of image pixel values
                folder = 'blank'
                if mean <= 210 and std >= 20:
                    folder = 'full'
                elif mean <= 235 and std >= 13:
                    folder = 'partial'

                sub_dir = level_dir + '\\' + folder
                final_path = os.path.join(sub_dir, '%d_%d' % (col, row))

                percent = floor(cnt*100/num_tiles)
                cnt += 1
                print("Now saving tile with title: ", final_path, f"| PROGRESS: lvl {level_num}, {cnt}/{num_tiles} ({percent}%)")

                plt.imsave(final_path + '.png', tile_np)

                # if folder == 'blank':
                #     blank_images.append(tile)
                # elif folder == 'partial':
                #     partial_images.append(tile)
                # else:
                #     full_images.append(tile)
        
        # if blank_images:
        #     blank_images[0].save(level_dir + '\\blank.tiff', save_all=True, append_images=blank_images[1:], compression='tiff_deflate')
        # if partial_images:
        #     partial_images[0].save(level_dir + '\\partial.tiff', save_all=True, append_images=partial_images[1:], compression='tiff_deflate')
        # if full_images:
        #     full_images[0].save(level_dir + '\\full.tiff', save_all=True, append_images=full_images[1:], compression='tiff_deflate')
        print("=" * 100)

def mean_std(np_img):
    return (np.mean(np_img), np.std(np_img))

if __name__ == "__main__":
    # Load the svs slide into an object.
    svs_list = glob.glob('D:/NSC2024_dataset/svs/*.*')

    for svs in svs_list:
        slide = open_slide(svs)

        if(not isinstance(slide, OpenSlide)):
            raise TypeError(f"Expected an instance of OpenSlide, got {type(slide)}")

        base_dir = 'D:/NSC2024_dataset/extracted'
        file_name = svs.split('\\')[1]

        print(svs)

        # get thumbnail
        if not os.path.exists(base_dir + '/' + file_name + '/thumbnail.png'):
            pass
            # thumbnail = slide.get_thumbnail((2048, 2048))
            # thumbnail_RGB = thumbnail.convert('RGB')
            # thumbnail_np = np.array(thumbnail_RGB)
            # plt.imsave(base_dir + '/' + file_name + '/thumbnail.png', thumbnail_np)


        try: 
            os.mkdir(base_dir + '/' + file_name)
        except: 
            pass

        extract(slide, file_name)
        # display_svs_information(slide)
        # visualize_svs(slide)


    # img = np.asarray(plt.imread('./test-images/blank/blank.png'))* 255
    # mean, std = mean_std(img)
    # print(mean, std)

    # img = np.asarray(plt.imread('./test-images/full/full4.png'))* 255
    # mean, std = mean_std(img)
    # print(mean, std)

    # img = np.asarray(plt.imread('./test-images/partial/partial4.png'))* 255
    # mean, std = mean_std(img)
    # print(mean, std)