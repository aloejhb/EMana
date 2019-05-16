import os
import pandas as pd
import logging
import matplotlib.pyplot as plt
from PIL import Image
from mpl_toolkits.mplot3d import Axes3D

def plot_tile_pos(df, zname='slicenum'):
    # zname can also be 'z', if df contains a column named 'z'
    ax = plt.figure().gca(projection='3d')
    ax.scatter(df['x'], df['y'], df[zname])
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel(zname)
    plt.show()


def calc_slice_image_size(bbox, tile_size_px_py):
    tile_center_size = bbox['max'][0:2] - bbox['min'][0:2]
    image_size = tile_center_size.as_matrix() + tile_size_px_py
    return image_size
    

def paste_tiles_to_slice(slicedf, bbox, tile_size_px_py,
                         data_root_dir, outdir, stack_name):
    slicenum = slicedf['slicenum'][1]
    message = 'Pasting slice #{}'.slicenum
    print(message)
    logging.info(message)
    
    if not (slicedf['slicenum'] == slicenum).all():
        raise Exception('Slice data frame must contain only one slicenum!')
    image_size = calc_slice_image_size(bbox, tile_size_px_py)
    slice_image = Image.new('L', tuple(image_size))
    for idx, row in slicedf.iterrows():
        tile_path = os.path.join(data_root_dir, row['file'])
        tile = Image.open(tile_path)
        xypos = row[['x', 'y']].as_matrix()
        slice_image.paste(tile, tuple(xypos))
    outfile = '{}_slice{:05d}.tif'.format(stack_name, slicenum)
    outpath = os.path.join(outdir, outfile)
    slice_image.save(outpath)


if __name__ == '__main__':
    platform = 'linux'
    if platform == 'linux':
        data_root_dir = '/run/user/1000/gvfs/smb-share\:server\=tungsten-nas.fmi.ch\,share\=landing_gmicro_sem/'
        result_dir = '/home/hubo/Projects/juvenile_EM/OBDp_overview'
    else:
        data_root_dir = 'W:\landing\gmicro_sem'
        result_dir = 'M:\hubo\juvenile_EM\OBDp_overview\imagelist'

    imgli_dir = os.path.join(result_dir, 'imagelist')
    stack_image_dir = os.path.join(result_dir, 'stack_image')
    logpath = os.path.join(result_dir, 'paste_tiles.log')
    logging.basicConfig(filename='example.log')

    
    stack_name = '20190215_Bo_juvenile_overviewstackOBDp'
    gridnum = 5
    imgli_file = '{}_stack_grid{:04}_xy_translated_imagelist.csv'.format(stack_name, gridnum)
    bboxfile =  '{}_stack_grid{:04}_bbox.csv'.format(stack_name, gridnum)

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


    grouped_imgdf = imgdf.groupby('slicenum')

    
    subgrouped = [g[1] for g in list(grouped_imgdf)[:5]]
    # for name, group in grouped_imgdf:
    #     print(group)

    for group in subgrouped:
        paste_tiles_to_slice(group, bbox, tile_size_px_py,
                             data_root_dir,stack_image_dir, stack_name)
        

