
import os
import sys, json
import numpy as np
import cv2
from pathlib import Path
from PIL import Image

from concurrent.futures import ThreadPoolExecutor, as_completed

import torch
from torchvision.transforms import ToTensor
import segmentation_models_pytorch as smp

current_dir = Path(__file__).parent
root_dir = current_dir.parent.parent

with os.add_dll_directory(root_dir / "utils/openslide_binary/bin"):
    import openslide

from openslide import open_slide
import time

print("Imported library", flush=True)

eps = 0.0005

file_path = Path(sys.argv[1])
file_name = file_path.name
file_name_without_ext = file_name.split('.')[0]
is_svs = file_path.suffix == ".svs"

output_file_path = current_dir / f"output/{file_name}/{file_name_without_ext}.png"

data_path = current_dir / f"output/{file_name}/data.txt"


output_folder = current_dir / f"output/{file_name}"
output_folder.mkdir(parents=True, exist_ok=True)

classes = ['background', 'solid', 'micropapillary']
subtypes = ["solid", "micropapillary"]
class_num = len(classes)


model_id = 0

arch = ["unet", "unetplusplus"][model_id]
encoder_name = "resnet101"

model = smp.create_model(
    arch=arch, 
    encoder_name=encoder_name, 
    encoder_weights='imagenet', 
    in_channels=3, 
    classes=class_num
)

model_name = "unet_resnet101_20_epochs.pth"
model_path = current_dir / f"models/{arch}_{encoder_name}/{model_name}"
print(model_name, model_path)
model.load_state_dict(torch.load(f=model_path, weights_only=True))



slide = open_slide(file_path) if is_svs else cv2.cvtColor(cv2.imread(file_path), cv2.COLOR_BGR2RGB)
width, height = slide.dimensions if is_svs else (slide.shape[1], slide.shape[0])

tile_size = (512, 512)  # Size of the tile
overlap = 0  # Overlap between tiles
desired_level = 0  # User-defined level
dtype = np.uint8


full_mask_shape = (height, width, 3)
full_mask = np.memmap(current_dir / f"output/{file_name}/full_mask.dat", dtype=dtype, mode='w+', shape=full_mask_shape)

print("Python receive", file_path, flush=True)
print(f"width: {width}px, height: {height}px", flush=True)
print("Linked to numpy memmap", flush=True)

total_tiles = ((width - 1) // (tile_size[0] - overlap) + 1) * \
              ((height - 1) // (tile_size[1] - overlap) + 1)

print(f"there are {total_tiles} tiles to predict", flush=True)

area = width * height
# lepidic acinar solid micropapillary papillary
area_classes = [0, 0, 0, 0, 0]

processed_tiles = 0
batch_start_time = None
tracking_frequency = 10
avg_time_taken = 0

target_width = 1e4
downsample_factor = max(1, width//target_width)


def gray_to_rgb(x):
	expanded_array = np.expand_dims(x, axis=-1)
	x_reshaped = np.repeat(expanded_array, repeats=3, axis=-1)
 
	color_map = {
			0: [0, 0, 0], # Black for background
			1: [255, 0, 0],   # Red for solid
			2: [0, 255, 0],   # Green for micropapillary
		}

	rgb = np.zeros_like(x_reshaped, dtype=x_reshaped.dtype)
	for label, color in color_map.items():
			rgb[x_reshaped[..., 0] == label] = color 
	return rgb


def process(x, y, w, h):
	global processed_tiles
	global tracking_frequency
	global batch_start_time
	global avg_time_taken

	cropped = slide.read_region((x, y), desired_level, (w, h)) if is_svs else slide[y:y+h, x:x+w, :]

	pad_x = tile_size[0] - w
	pad_y = tile_size[1] - h

	cropped = np.asarray(cropped)[:, :, :3]
	
	padded_cropped = np.pad(cropped, pad_width=((0, pad_y), (0, pad_x), (0, 0)), mode='constant', constant_values=0)

	tensor_cropped = ToTensor()(padded_cropped).unsqueeze(0)

	with torch.inference_mode():
		y_preds = model(tensor_cropped).cpu()
		arg_max = torch.argmax(y_preds, dim=1)[:, :h, :w]

		solid = torch.sum(arg_max == 1).item()
		micropapillary = torch.sum(arg_max == 2).item()
  
		area_classes[2] += solid
		area_classes[3] += micropapillary

		rgb = gray_to_rgb(arg_max)
		rgb = rgb.squeeze(0)

		opacity = 0.4
		overlayed = cv2.addWeighted(rgb.astype(dtype), opacity, cropped.astype(dtype), 1 - opacity, 0)
		full_mask[y:y+h, x:x+w, :] = overlayed

	processed_tiles += 1

	if processed_tiles % tracking_frequency == 1:
		batch_start_time = time.time()


	percent = processed_tiles / total_tiles * 100
	print('@' + str(int(percent)), flush=True)
	time.sleep(eps)

	if processed_tiles % tracking_frequency == 0:
		batch_end_time = time.time()
		time_taken = batch_end_time - batch_start_time
		remaining_tiles = total_tiles - processed_tiles

		avg_time_taken += time_taken

		estimated_remaining_time_seconds = (remaining_tiles / tracking_frequency) * time_taken
		estimated_remaining_time_minutes = estimated_remaining_time_seconds / 60

		print(f"Processed {processed_tiles}/{total_tiles} tiles ({percent:.2f}%) in {time_taken:.2f} seconds. \
                Estimated remaining time: {estimated_remaining_time_minutes:.2f} minutes.", flush=True)
		time.sleep(eps)


futures = []
with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
	
	for y in range(0, height, tile_size[1] - overlap):
		for x in range(0, width, tile_size[0] - overlap):

			w, h = tile_size
			if x + w > width: w = width - x
			if y + h > height: h = height - y

			futures.append(executor.submit(process, x, y, w, h))
		
	for future in as_completed(futures):
		future.result()

print("@100", flush=True)
time.sleep(eps)

print(f"Average time taken is {avg_time_taken/total_tiles} seconds.", flush=True)
time.sleep(eps)


n_width, n_height = width//downsample_factor, height//downsample_factor
downsampled_full_mask = cv2.resize(full_mask, (n_width, n_height), interpolation=cv2.INTER_AREA)

segment_output_path = current_dir / f"output/{file_name}/{file_name_without_ext}.png"
image = Image.fromarray(downsampled_full_mask)
image.save(segment_output_path)

print('+' + str(segment_output_path), flush=True)
time.sleep(eps)

# print(downsampled_full_mask.shape, downsampled_full_mask.dtype, flush=True)

all_classes = ["lepidic", "acinar", "solid", "micropapillary", "papillary"]
data = { c: round(area_classes[idx]/area, 2) for idx, c in enumerate(all_classes) }
data = json.dumps(data)

f = open(current_dir / f"output/{file_name}/data.txt", "w")
f.write(data)
f.close()


print('$' + data, flush=True)