import os
import pandas as pd
import logging
import matplotlib.pyplot as plt
from PIL import Image
from mpl_toolkits.mplot3d import Axes3D
from importlib import reload

def plot_tile_pos(df, zname='slicenum'):
    # zname can also be 'z', if df contains a column named 'z'
    ax = plt.figure().gca(projection='3d')
    ax.scatter(df['x'], df['y'], df[zname])
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel(zname)


def calc_slice_image_size(bbox, tile_size_px_py):
    tile_center_size = bbox['max'][0:2] - bbox['min'][0:2]
    image_size = tile_center_size.values + tile_size_px_py
    return image_size
    

def paste_tiles_to_slice(slicedf, bbox, tile_size_px_py,
                         data_root_dir, outdir, stack_name):
    slicenum = slicedf['slicenum'].iloc[0]
    message = 'Pasting slice #{}'.format(slicenum)
    print(message)
    logging.info(message)

    if not (slicedf['slicenum'] == slicenum).all():
        raise Exception('Slice data frame must contain only one slicenum!')
    image_size = calc_slice_image_size(bbox, tile_size_px_py)
    slice_image = Image.new('L', tuple(image_size))
    for idx, row in slicedf.iterrows():
        tile_path = os.path.join(data_root_dir, row['file'])
        tile = Image.open(tile_path)
        xypos = row[['x', 'y']].values
        slice_image.paste(tile, tuple(xypos))
    outfile = '{}_slice{:05d}.tif'.format(stack_name, slicenum)
    outpath = os.path.join(outdir, outfile)
    slice_image.save(outpath)


if __name__ == '__main__':
    platform = 'windows'
    if platform == 'linux':
        data_root_dir = '/run/user/1000/gvfs/smb-share\:server\=tungsten-nas.fmi.ch\,share\=landing_gmicro_sem/'
        imgli_root_dir = '/home/hubo/Projects/juvenile_EM/OBDp_overview'
        result_dir = '/home/hubo/Projects/juvenile_EM/OBDp_overview/imagelist'
    else:
        data_root_dir = 'W:\landing\gmicro_sem'
        imgli_root_dir = 'M:\hubo\juvenile_EM\OBDp_overview\imagelist'
        result_dir = 'Z:\BoHu\juvenile_EM\OBDp_overview'
        
    grid_num = 5
    grid_subdir = 'grid{0:d}'.format(grid_num)
    imgli_dir = os.path.join(imgli_root_dir, grid_subdir)
    stack_image_dir = os.path.join(result_dir, grid_subdir, 'stack_image')
    reload(logging)
    logpath = os.path.join(result_dir, grid_subdir, 'paste_tiles.log')
    logging.basicConfig(filename=logpath, level=logging.DEBUG,
                        format='%(asctime)-15s %(message)s')
    logging.info('Starting to paste tiles ...')

    
    stack_name = '20190215_Bo_juvenile_overviewstackOBDp'
    gridnum = 5
    imgli_file = '{}_stack_grid{:04}_xy_translated_imagelist.csv'.format(stack_name, gridnum)
    # Manually corrected imagelist for missing slices
    imgli_file = imgli_file.replace('.csv', '_add_missing_slice_manually.csv')
    # bboxfile =  '{}_stack_grid{:04}_bbox.csv'.format(stack_name, gridnum)
    bboxfile = 'without_run020_bbox.csv'

    tile_size_px_py = [2048, 1536]  # unit in px
    pixel_size = 50.0  # unit in um
    overlap = 200  # unit in px

    visualize_tile_pos = False

    # Load image list and bounding box
    imgli_path = os.path.join(imgli_dir, imgli_file)
    imgdf = pd.read_csv(imgli_path)
    bbox = pd.read_csv(os.path.join(imgli_dir, bboxfile))
    print(bbox)
    # Visually check whether the tiles are lying on a grid in a stack
    if visualize_tile_pos:
        plot_tile_pos(imgdf[::100])
        plt.show()


    grouped_imgdf = imgdf.groupby('slicenum')
    group_name_list = [name for name, group in grouped_imgdf]

     # for name, group in grouped_imgdf:
 #    for group in subgrouped:
 #        paste_tiles_to_slice(group, bbox, tile_size_px_py,
 #                             data_root_dir,stack_image_dir, stack_name)
    
    # Find breakpoint
    break_slice_num = 3248 # 3733
    y_shift = 1336 # Attention! this is only for correcting tile origin shift due to forgetitng run019...
    break_group_idx = group_name_list.index(break_slice_num)
    print(break_group_idx)
    
    subgrouped = [g[1] for g in list(grouped_imgdf)[break_group_idx:break_group_idx+3]]
    for group in subgrouped:
        group['y'] = group['y'] - y_shift # Attention! this is only for correcting tile origin shift due to forgetitng run019...
        paste_tiles_to_slice(group, bbox, tile_size_px_py,
                             data_root_dir,stack_image_dir, stack_name)
