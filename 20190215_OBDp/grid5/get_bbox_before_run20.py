import sys
import os
import pandas as pd
sys.path.insert(0,'../../')
from concatenate_imagelist import translate_xy_coordinate
imgli_dir = '/home/hubo/Projects/juvenile_EM/OBDp_overview/imagelist/grid5/'
infile = os.path.join(imgli_dir, 'without_run020.csv')
bbfile = os.path.join(imgli_dir, 'without_run020_bbox.csv')
imglidf = pd.read_csv(infile, index_col=0)
imglidf, min_xyz, max_xyz = translate_xy_coordinate(imglidf, bbofxile=bbfile)

print(min_xyz, max_xyz)
