import os
import pandas as pd
import matplotlib.pyplot as plt
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
    if not (slicedf['slicenum'] == slicenum).all():
        raise Exception('Slice data frame must contain only one slicenum!')
    image_size = calc_slice_image_size(bbox, tile_size_px_py)
    slice_image = Image.new('L', image_size)
    for row in slicedf.iterrows():
        tile = Image.open(row['file'])
        xypos = row[['x', 'y']].as_matrix()
        slice_image.paste(tile, xypos)
    outfile = '{}_slice{:05d}.tif'.format(stack_name, slicenum)
    outpath = os.path.join(outdir, outfile)
    slice_image.save(outpath)


if __name__ == '__main__':
    data_root_dir = '/media/FMI/tungsten_landing_gmicro_sem/'
    stack_name = '20190215_Bo_juvenile_overviewstackOBDp'
    imgli_dir = '/home/hubo/Projects/juvenile_EM/OBDp_overview/imagelist'
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
    bbox = pd.read_csv(bboxfile)
    print(bbox)
    # Visually check whether the tiles are lying on a grid in a stack
    if visualize_tile_pos:
        plot_tile_pos(imgdf[::100])

    paste_tiles_to_slice(imgdf, bbox, tile_size_px_py)
