from tqdm import tqdm
import time

# Example list
data = range(100)

# Using tqdm with enumerate
for idx, item in tqdm(enumerate(data), total=len(data), desc="Processing"):
    time.sleep(0.1)  # Simulate some work
    # You can use idx and item here