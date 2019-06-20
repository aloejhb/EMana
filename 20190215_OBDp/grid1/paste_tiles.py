import os
import sys
import matplotlib.pyplot as plt
import pandas as pd
import logging

from importlib import reload
emana_path = 'M:\hubo\juvenile_EM\scripts\EMana'
sys.path.insert(0, emana_path)
from paste_tiles_to_grid3d import plot_tile_pos, paste_tiles_to_slice

platform = 'windows'
if platform == 'linux':
    data_root_dir = '/run/user/1000/gvfs/smb-share\:server\=tungsten-nas.fmi.ch\,share\=landing_gmicro_sem/'
    imgli_root_dir = '/home/hubo/Projects/juvenile_EM/OBDp_overview'
    result_root_dir = '/home/hubo/Projects/juvenile_EM/OBDp_overview'
else:
    data_root_dir = 'W:\landing\gmicro_sem'
    imgli_root_dir = 'M:\hubo\juvenile_EM\OBDp_overview'
    result_root_dir = 'Z:\BoHu\juvenile_EM\OBDp_overview'

stack_name = '20190215_Bo_juvenile_overviewstackOBDp'
# gridnum = 1
imgli_dir = os.path.join(imgli_root_dir, 'imagelist/grid1/')
imgli_filename = '20190215_Bo_juvenile_overviewstackOBDp_add_missing_slice.csv'
imgli_file = os.path.join(imgli_dir, 'check_missing_slice', imgli_filename)
visualize_tile_pos = False

bbox_filename =  '20190215_Bo_juvenile_overviewstackOBDp_stack_grid0001_xy_corrected_bbox.csv'
bbox_file = os.path.join(imgli_dir, 'correct_xy', bbox_filename)

tile_size_px_py = [1024, 768]  # unit in pixel
overlap = 200  # unit in pixel

result_dir = os.path.join(result_root_dir, 'grid1')
stack_image_dir = os.path.join(result_dir, 'stack_image')

reload(logging)
logpath = os.path.join(result_dir, 'paste_tiles.log')
logging.basicConfig(filename=logpath, level=logging.DEBUG,
                    format='%(asctime)-15s %(message)s')
logging.info('Starting to paste tiles ...')

    
imgdf = pd.read_csv(imgli_file, index_col=0)
bbox = pd.read_csv(bbox_file)
print(bbox)
if visualize_tile_pos:
    plot_tile_pos(imgdf[::100])
    plt.show()

grouped_imgdf = imgdf.groupby('slicenum')
group_name_list = [name for name, group in grouped_imgdf]

#for name, group in grouped_imgdf:
#    paste_tiles_to_slice(group, bbox, tile_size_px_py,
#                         data_root_dir,stack_image_dir, stack_name)
#      
break_slice_num = 1134
break_group_idx = group_name_list.index(break_slice_num)
print(break_group_idx)

subgrouped = [g[1] for g in list(grouped_imgdf)[break_group_idx:break_group_idx+1]]
for group in subgrouped:
    paste_tiles_to_slice(group, bbox, tile_size_px_py,
                         data_root_dir,stack_image_dir, stack_name)