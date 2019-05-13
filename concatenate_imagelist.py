#!/usr/bin/env python
import shutil
import os
import glob
import re
import pandas as pd


def concatenate_files(infile_list, outfile):
    with open(outfile, 'wb') as fout:
        for infile in infile_list:
            with open(infile, 'rb') as fin:
                shutil.copyfileobj(fin, fout)
            fout.write(os.linesep.encode('utf-8'))


def concatenate_imgli_files(rundir, outfile):
    logdir = os.path.join(rundir, 'meta', 'logs')
    imgli_pattern = os.path.join(logdir, 'imagelist*')
    imgli_list = sorted(glob.glob(imgli_pattern))
    concatenate_files(imgli_list, outfile)


def append_rundir(rundir, imgli_file, outfile=None):
    if outfile is None:
        outfile = imgli_file
    with open(imgli_file, 'r') as f:
        fil = f.read().rstrip('\n')
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
    zdiff = df[3].diff()
    zdiff = zdiff[1:]
    vld_increase_z = zdiff >= 0
    vld_seq_slice = zdiff <= 1
    if not vld_increase_z.all():
        raise Exception('Image list in valid! Image list should be sorted increasingly according to z.')
    if not vld_seq_slice.all():
        
        raise Exception('Image list in valid! Missing slices!')
    return True



def find_bounding_box_3d(df):
    min_xyz = df[[1, 2, 3]].min()
    max_xyz = df[[1, 2, 3]].max()
    return min_xyz, max_xyz


def translate_coordinate(infile, outfile=None, bboxfile=None):
    df = pd.read_csv(infile, delimiter=';', header=None)
    vld = validate_image_list(df)
    min_xyz, max_xyz = find_bounding_box_3d(df)
    df[[1, 2, 3]] = df[[1, 2, 3]] - min_xyz
    if outfile:
        df.to_csv(outfile, header=None)
    if bboxfile:
        bbox_df = pd.concat([min_xyz, max_xyz], axis=1)
        bbox_df = bbox_df.rename(index={1: 'x', 2: 'y', 3: 'z'},
                                 columns={0: 'min', 1: 'max'})
        bbox_df.to_csv(bboxfile)
    return df, min_xyz, max_xyz


if __name__ == '__main__':
    data_root_dir = '/media/FMI/tungsten_landing_gmicro_sem/'
    stack_name = '20190215_Bo_juvenile_overviewstackOBDp'
    runnum_list = range(19)
    outdir = '/home/hubo/Projects/juvenile_EM/OBDp_overview/imagelist'
    rundir_list = ['{}_run{:03d}'.format(stack_name, x) for x in runnum_list]

    os.chdir(outdir)
    # runimgli_list = []
    # for rundir in rundir_list:
    #     indir = os.path.join(data_root_dir, rundir)
    #     outfile = '{}_imagelist.txt'.format(rundir)
    #     runimgli_list.append(outfile)
    #     concatenate_imgli_files(indir, outfile)
    #     append_rundir(rundir, outfile)

    # stack_imgli_file = '{}_stack_imagelist.txt'.format(stack_name)
    # concatenate_files(runimgli_list, stack_imgli_file)

    gridnum = 5
    grid_imgli_file = '{}_stack_grid{:04}_imagelist.txt'.format(stack_name, gridnum)
    # get_stack_imgli(stack_imgli_file, grid_imgli_file, gridnum)

    # df = pd.read_csv(grid_imgli_file, delimiter=';', header=None)
    trans_grid_imgli_file = grid_imgli_file.replace('imagelist.txt',
                                                    'translated_imagelist.csv')
    df, min_xyz, max_xyz = translate_coordinate(grid_imgli_file,
                                                trans_grid_imgli_file)

