import os
import sys
import numpy as np
import cv2
from PIL import Image
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import shutil

current_dir = Path(__file__).parent
# Parent directory
root_dir = current_dir.parent.parent
with os.add_dll_directory(root_dir / "openslide_binary/bin"):
    import openslide

from tensorflow.keras.models import load_model

# ======== TEST MODE ========
from glob import glob
import time

images = glob(str(current_dir / "assets/dummy_cropped_predicted/*") )
for i in images:
    print(i, flush=True)
    time.sleep(0.1)
exit()
# ===========================


model  = load_model(str(current_dir / "demo_model.keras"), compile=False)

# image = cv2.imread("./assets/test.png", cv2.IMREAD_COLOR)
file_path = sys.argv[1]
image = cv2.imread(file_path, cv2.IMREAD_COLOR)
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
height, width, channels = image.shape

dump = current_dir / "assets/cropped_predicted"


def gray_to_rgb(x):
    x = np.expand_dims(x, axis=-1)
    x_reshaped = np.concatenate([x] * 3, axis=-1)
    color_map = {
            1: [255, 0, 0],   # Red for lepidic
            2: [0, 255, 0],   # Green for acinar
            3: [0, 0, 255],    # Blue for micropapillary
            4: [255, 255, 0],  # Yellow for papillary
            5: [255, 0, 255],   # violet for solid
        }
    
    rgb = np.zeros_like(x_reshaped, dtype=np.uint8)
    for label, color in color_map.items():
            rgb[x_reshaped[..., 0] == label] = color 
    return rgb


def extract(x, y, len):
    cropped = image[y:y+len,x:x+len,:]
    expanded = np.expand_dims(cropped, axis=0)

    y_pred = model(expanded)
    y_pred_argmax = np.argmax(y_pred, axis=3)
    y_pred_argmax = np.squeeze(y_pred_argmax, axis=0)
    
    segmented = gray_to_rgb(y_pred_argmax)

    # OVERLAY SEGMENTATION
    opacity = 0.4
    overlayed = cv2.addWeighted(segmented, opacity, cropped, 1 - opacity, 0)
    result = Image.fromarray(overlayed)
    save_path = dump / f"{x}_{y}.png"
    print(save_path, flush=True)
    result.save(save_path)


SIZE = 512
futures = []
with ThreadPoolExecutor(max_workers=8) as executor:

    if os.path.isdir(dump):
        shutil.rmtree(dump)

    os.mkdir(dump)
    for y in range(0, height, SIZE):
        for x in range(0, width, SIZE):
            # Submit the task to the executor
            futures.append(executor.submit(extract, x, y, SIZE))
    
    # Wait for all futures to complete
    for future in as_completed(futures):
        future.result()  # This will raise any exceptions that occurred
