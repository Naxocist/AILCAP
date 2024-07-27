import os
import numpy as np
import cv2
from PIL import Image
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

parent_dir = Path(os.path.dirname(os.path.dirname(os.getcwd())))
with os.add_dll_directory(parent_dir / "openslide_binary/bin"):
    import openslide


image = cv2.imread("./assets/test.png", cv2.IMREAD_COLOR)
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
height, width, channels = image.shape


def extract(x, y, len):
    cropped = image[y:y+len,x:x+len,:]
    cropped_img = Image.fromarray(cropped)
    dump = Path("./assets/cropped")
    if not os.path.isdir(dump): os.mkdir(dump)
    cropped_img.save(dump / f"{x}_{y}.png")


SIZE = 512
futures = []
with ThreadPoolExecutor(max_workers=8) as executor:
    for y in range(0, height, SIZE):
        for x in range(0, width, SIZE):
            # Submit the task to the executor
            futures.append(executor.submit(extract, x, y, SIZE))
    
    # Wait for all futures to complete
    for future in as_completed(futures):
        future.result()  # This will raise any exceptions that occurred