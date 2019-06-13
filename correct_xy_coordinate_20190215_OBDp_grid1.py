import os
import math
import pandas as pd
import numpy as np

from concatenate_imagelist import translate_xy_coordinate

def compute_transform_mat(scale_x, scale_y, rot_x, rot_y):
    angle_diff = rot_x - rot_y
    A = math.cos(rot_y) / math.cos(angle_diff)
    B = math.sin(rot_x) / math.cos(angle_diff)
    C = (-1) * math.sin(rot_y) / math.cos(angle_diff)
    D = math.cos(rot_x) / math.cos(angle_diff)
    return (A, B, C, D)


def convert_to_d(s_coordinates, transform_mat, scale_x, scale_y):
    """Convert stage coordinates into SEM coordinates"""
    A, B, C, D = transform_mat
    stage_x, stage_y = s_coordinates
    stage_x /= scale_x
    stage_y /= scale_y
    dx = ((stage_y + stage_x * (-D/C))/
          (B + A * (-D/C)))
    dy = ((stage_y - dx * B) / D)
    return [dx, dy]


def convert_to_p(d_coordinates, pixel_size):
    p_coord = (np.array(d_coordinates) *1000 / pixel_size).astype('int')
    return p_coord


def compute_correct_origin(configdf, CS_PIXEL_SIZE=10):
    scale_x = configdf.loc[0, 'stage_scale_factor_x']
    scale_y = configdf.loc[0, 'stage_scale_factor_y']
    rot_x = configdf.loc[0, 'stage_rotation_angle_x']
    rot_y = configdf.loc[0, 'stage_rotation_angle_y']
    transform_mat = compute_transform_mat(scale_x, scale_y, rot_x, rot_y)

    origin_d_list = [convert_to_d([row['origin_sx'], row['origin_sx']],
                                  transform_mat, scale_x, scale_y)
                     for idx, row in configdf.iterrows()]

    wrong_origin_list = [convert_to_p(dc, CS_PIXEL_SIZE)for dc in origin_d_list]

    pixel_size = configdf.loc[0, 'pixel_size']
    correct_origin_list = [convert_to_p(dc, pixel_size)for dc in origin_d_list]
    slicenum_list = configdf['slice_counter'].tolist()

    return (wrong_origin_list, correct_origin_list, slicenum_list)


def correct_xy_coord(imglidf, wrong_origin_list, correct_origin_list, slicenum_list):
    slicenum_list.append(imglidf.iloc[-1, 3]+1)
    for k in range(len(slicenum_list)-1):
        wrong_origin = wrong_origin_list[k]
        correct_origin = correct_origin_list[k]
        slice_range = slicenum_list[k:k+2]
        tile_idx = (imglidf['slicenum'] >= slice_range[0])*\
                   (imglidf['slicenum'] < slice_range[1])
        newx = imglidf.loc[tile_idx, 'x'] - wrong_origin[0] + correct_origin[0]
        newy = imglidf.loc[tile_idx, 'y'] - wrong_origin[1] + correct_origin[1]
        imglidf.set_value(tile_idx, 'x', newx)
        imglidf.set_value(tile_idx, 'y', newy)
    return imglidf
        

if __name__ == '__main__':
    platform = 'linux'
    if platform == 'linux':
        data_root_dir = '/run/user/1000/gvfs/smb-share:server=tungsten-nas.fmi.ch,share=landing_gmicro_sem'
        resultdir = '/home/hubo/Projects/juvenile_EM/OBDp_overview/'
    else: 
        data_root_dir = 'W:\landing\gmicro_sem'
        resultdir = 'M:\hubo\juvenile_EM\OBDp_overview\\'
        
    imageli_dir = os.path.join(resultdir, 'imagelist')
    configdir = os.path.join(resultdir, 'config_list')
    outdir = os.path.join(imageli_dir, 'correct_xy_grid1')

    imageli_filename = '20190215_Bo_juvenile_overviewstackOBDp_stack_grid0001_imagelist.txt'
    imageli_filepath = os.path.join(imageli_dir, imageli_filename)
    imglidf = pd.read_csv(imageli_filepath, delimiter=';', header=None)
    imglidf.columns = ['file', 'x', 'y', 'slicenum']
    
    config_filename = 'origin_shift_grid1.csv'
    config_filepath = os.path.join(configdir, config_filename)
    configdf = pd.read_csv(config_filepath)

    wrong_origin_list, correct_origin_list, slicenum_list = compute_correct_origin(configdf)

    correct_imglidf = correct_xy_coord(imglidf, wrong_origin_list, correct_origin_list, slicenum_list)

    outfilename =  imageli_filename.replace('imagelist.txt',
                                            'xy_corrected_imagelist.csv')
    outfile = os.path.join(outdir, outfilename)
    correct_imglidf.to_csv(outfile)

    trans_imgli_file = outfile.replace('imagelist.csv',
                                       'xy_translated_imagelist.csv')
    bboxfile = outfile.replace('imagelist.csv', 'bbox.csv')
    df, min_xyz, max_xyz = translate_xy_coordinate(correct_imglidf,
                                                   trans_imgli_file,
                                                   bboxfile)
