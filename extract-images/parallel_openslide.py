import os
from concurrent.futures import ThreadPoolExecutor, as_completed

OPENSLIDE_PATH = 'D:/NSC2024/source-code/openslide_binary/bin'
with os.add_dll_directory(OPENSLIDE_PATH):
    import openslide


def extract_tile(slide, level, x, y, tile_size, output_dir, file_prefix):
    """
    Extract a tile from the slide and save it as an image file.
    
    Args:
    - slide (OpenSlide object): The whole slide image object.
    - level (int): The level of the slide to extract from.
    - x (int): The x-coordinate of the tile's top-left corner.
    - y (int): The y-coordinate of the tile's top-left corner.
    - tile_size (int): The size of the tile (both width and height).
    - output_dir (str): Directory to save the extracted tiles.
    - file_prefix (str): Prefix for the output file names.
    """
    # Extract the tile
    tile = slide.read_region((x, y), level, (tile_size, tile_size))
    tile = tile.convert("RGB")
    
    # Create the output file path
    output_path = os.path.join(output_dir, f"{file_prefix}_{x}_{y}.jpg")
    
    # Save the tile
    tile.save(output_path)

def parallel_tile_extraction(slide_path, output_dir, level=0, tile_size=512, overlap=0, num_workers=4):
    """
    Extract tiles from an SVS file in parallel and save them.
    
    Args:
    - slide_path (str): Path to the SVS file.
    - output_dir (str): Directory to save the extracted tiles.
    - level (int): The level of the slide to extract from (default is 0).
    - tile_size (int): The size of the tile (both width and height, default is 512).
    - overlap (int): The number of pixels by which adjacent tiles overlap (default is 0).
    - num_workers (int): The number of worker threads to use for parallel processing (default is 4).
    """
    # Open the whole slide image
    slide = openslide.OpenSlide(slide_path)
    
    # Get the dimensions of the level
    width, height = slide.level_dimensions[level]
    
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Create a list to store the futures
    futures = []
    
    # Create a ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        for y in range(0, height, tile_size - overlap):
            for x in range(0, width, tile_size - overlap):
                # Submit the task to the executor
                futures.append(executor.submit(extract_tile, slide, level, x, y, tile_size, output_dir, 'tile'))
        
        # Wait for all futures to complete
        for future in as_completed(futures):
            future.result()  # This will raise any exceptions that occurred

if __name__ == "__main__":
    slide_path = r"C:\Users\USER\Desktop\CMU-1.svs"
    output_dir = r"D:\NSC2024\extracted\CMU-1.svs"
    
    parallel_tile_extraction(slide_path, output_dir, level=0, tile_size=256, overlap=0, num_workers=4)
