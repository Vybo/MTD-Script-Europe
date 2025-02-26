import os
import requests
from math import log, tan, cos, pi
from tqdm import tqdm

# Define the bounding boxes and zoom levels. Below are random examples.
regions = {
    "brno": (16.069281, 48.839711, 17.148912, 49.545265),
    "praha": (14.210659, 49.903493, 14.738401, 50.242204)
}

zoom_levels = range(1, 15) # Focusing on zoom levels 1 to 14
mapstyle = "atlas"
# mapstyle = "cycle"
# mapstyle = "transport"
# mapstyle = "landscape"
# mapstyle = "outdoors"
# mapstyle = "transport-dark"
# mapstyle = "spinal-map"
# mapstyle = "pioneer"
# mapstyle = "neighbourhood"
# mapstyle = "mobile-atlas"

api_key = "YOUR_KEY_HERE"
output_dir = os.path.join(os.path.expanduser("~"), "Downloads", "tiles")
os.makedirs(output_dir, exist_ok=True)

def lon2tilex(lon, zoom):
    return int((lon + 180.0) / 360.0 * (1 << zoom))

def lat2tiley(lat, zoom):
    return int((1.0 - log(tan(lat * pi / 180.0) + 1.0 / cos(lat * pi / 180.0)) / pi) / 2.0 * (1 << zoom))

def download_tile(zoom, x, y):
    url = f"https://tile.thunderforest.com/{mapstyle}/{zoom}/{x}/{y}.png?apikey={api_key}"
    tile_dir = os.path.join(output_dir, str(zoom), str(x))
    tile_path = os.path.join(tile_dir, f"{y}.png")
    os.makedirs(tile_dir, exist_ok=True)

    if not os.path.exists(tile_path):
        response = requests.get(url)
        if response.status_code == 200:
            with open(tile_path, "wb") as file:
                file.write(response.content)
        else:
            print(f"Failed to download tile {zoom}/{x}/{y}: {response.status_code} {response.reason}")

def main():
    total_tiles = 0

    for zoom in zoom_levels:
        for min_lon, min_lat, max_lon, max_lat in regions.values():  # Corrected unpacking for Europe
            start_x = lon2tilex(min_lon, zoom)
            end_x = lon2tilex(max_lon, zoom)
            start_y = lat2tiley(max_lat, zoom)
            end_y = lat2tiley(min_lat, zoom)

            total_tiles += (end_x - start_x + 1) * (end_y - start_y + 1)

    with tqdm(total=total_tiles, desc="Downloading tiles") as pbar:
        for zoom in zoom_levels:
            for min_lon, min_lat, max_lon, max_lat in regions.values():  # Corrected unpacking for Europe
                start_x = lon2tilex(min_lon, zoom)
                end_x = lon2tilex(max_lon, zoom)
                start_y = lat2tiley(max_lat, zoom)
                end_y = lat2tiley(min_lat, zoom)

                for x in range(start_x, end_x + 1):
                    for y in range(start_y, end_y + 1):
                        download_tile(zoom, x, y)
                        pbar.update(1)

if __name__ == "__main__":
    main()