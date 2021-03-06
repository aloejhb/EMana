#!/usr/bin/env python
import shutil
import os
import sys
import warnings
import glob
import re
import pandas as pd

from concatenate_log import concat_files


def concatenate_imgli_files(rundir, outfile):
    logdir = os.path.join(rundir, 'meta', 'logs')
    imgli_pattern = os.path.join(logdir, 'imagelist*')
    imgli_list = sorted(glob.glob(imgli_pattern))
    concatenate_files(imgli_list, outfile)


def append_rundir_to_filepath(rundir, imgli_file, outfile=None):
    if outfile is None:
        outfile = imgli_file
    with open(imgli_file, 'r') as f:
        fil = f.read().rstrip('\n')
    # TODO ignore empty lines!!
    with open(outfile, 'w') as f:
        f.write(re.sub(r'(?m)^', r'{}\\'.format(rundir), fil))


def get_stack_imgli(infile, outfile, gridnum):
    grid_str = 'g{:04}'.format(gridnum)
    with open(outfile, 'w') as fout:
        with open(infile, 'r') as fin:
                for line in fin:
                    if re.search(grid_str, line):
                        fout.write(line)


def validate_image_list(df):
    zdiff = df['slicenum'].diff()
    zdiff = zdiff[1:]
    increase_z = zdiff >= 0
    no_missing_slice = zdiff <= 1
    if not increase_z.all():
        print('Image list in valid! Image list should be sorted increasingly according to z.')
    if not no_missing_slice.all():
        miss_idx = no_missing_slice[~no_missing_slice].index
        print('Image list in valid! Missing slices!')
    else:
        miss_idx = [];
    valid = increase_z.all() and no_missing_slice.all()
    return valid, miss_idx

    
def print_missing_slice(df, miss_idx, outfile=None):
    union_idx = miss_idx.union(miss_idx-1)
    df_miss = df.loc[union_idx.values]
    if outfile:
        df_miss.to_csv(outfile, header=None)
    return df_miss


def find_bounding_box_3d(df):
    min_xyz = df[['x', 'y', 'slicenum']].min()
    max_xyz = df[['x', 'y', 'slicenum']].max()
    return min_xyz, max_xyz


def translate_xy_coordinate(df, outfile=None, bboxfile=None):
    min_xyz, max_xyz = find_bounding_box_3d(df)
    df[['x', 'y']] = df[['x', 'y']] - min_xyz[0:2]

    if outfile:
        df.to_csv(outfile)
    if bboxfile:
        bbox_df = pd.concat([min_xyz, max_xyz], axis=1)
        bbox_df = bbox_df.rename(columns={0: 'min', 1: 'max'})
        bbox_df.to_csv(bboxfile)
    return df, min_xyz, max_xyz


if __name__ == '__main__':
    platform = 'linux'
    if platform == 'linux':
        data_root_dir = '/run/user/1000/gvfs/smb-share:server=tungsten-nas.fmi.ch,share=landing_gmicro_sem'
        outdir = '/home/hubo/Projects/juvenile_EM/OBDp_overview/imagelist'
    else: 
        data_root_dir = 'W:\landing\gmicro_sem'
        outdir = 'M:\hubo\juvenile_EM\OBDp_overview\imagelist'

    imgli_sub_dir = 'run_imagelist'
    stack_name = '20190215_Bo_juvenile_overviewstackOBDp'
    runnum_list = range(20)
    rundir_list = ['{}_run{:03d}'.format(stack_name, x) for x in runnum_list]

    stack_imgli_file = '{}_stack_imagelist.txt'.format(stack_name)
    gridnum = 1
    grid_imgli_file = '{}_stack_grid{:04}_imagelist.txt'.format(stack_name, gridnum)

    os.chdir(outdir)
    if not os.path.isdir(imgli_sub_dir):
        os.mkdir(imgli_sub_dir)
        
    runimgli_list = []
    for rundir in rundir_list:
        indir = os.path.join(data_root_dir, rundir)
        outfile = '{}_imagelist.txt'.format(rundir)
        outfile = os.path.join(imgli_sub_dir, outfile)
        runimgli_list.append(outfile)
        concatenate_imgli_files(indir, outfile)
        append_rundir_to_filepath(rundir, outfile)

    concatenate_files(runimgli_list, stack_imgli_file)

    get_stack_imgli(stack_imgli_file, grid_imgli_file, gridnum)

    df = pd.read_csv(grid_imgli_file, delimiter=';', header=None)
    df.columns = ['file', 'x', 'y', 'slicenum']
    imgli_vld, miss_idx = validate_image_list(df)

    if len(miss_idx):
        miss_slice_file =  grid_imgli_file.replace('imagelist.txt',
                                                   'missed_slice.csv')
        df_miss = print_missing_slice(df, miss_idx, miss_slice_file)
        
    trans_grid_imgli_file = grid_imgli_file.replace('imagelist.txt',
                                                    'xy_translated_imagelist.csv')
    bboxfile = grid_imgli_file.replace('imagelist.txt', 'bbox.csv')
    df, min_xyz, max_xyz = translate_xy_coordinate(df,
                                                   trans_grid_imgli_file,
                                                   bboxfile)

