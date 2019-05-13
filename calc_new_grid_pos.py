import numpy as np
origin = [-274.32742579896274, -272.631196603877]
tile_size_px_py = [1024, 768]
overlap = 100
pixel_size = 100

ncol = 8
nrow = 10

new_origin = [0, 0]
new_origin = origin[0] - ((tile_size_px_py[0] - overlap)* ncol  +overlap)/pixel_size
