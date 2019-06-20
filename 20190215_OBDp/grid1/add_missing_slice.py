import os
import sys
import pandas as pd
import numpy as np
import re
from copy import deepcopy
sys.path.insert(0,'../../')
from concatenate_imagelist import validate_image_list

def modify_slice(template_slice, slicenum):
    new_slice = deepcopy(template_slice)
    new_slice['slicenum'] = slicenum
    old_slicenum_pattern = r'_s\d{5}.tif'
    new_slicenum_str = '_s{0:05d}.tif'.format(slicenum)
    new_slice['file'] = [re.sub(old_slicenum_pattern, new_slicenum_str, x) for x in new_slice['file']]
    return new_slice


def insert_dataframe(df1, df2, index):
    """Insert df2 into df1 at specified index (based on iloc)"""
    df1before = df1.iloc[0:index]
    df1after = df1.iloc[index+1:]
    df_merge = pd.concat([df1before, df2, df1after])
    return df_merge


def add_missing_slice(imglidf, miss_slice_list):
    for k in range(0, len(miss_slice_list), 2):
        miss_range = miss_slice_list[k:k+2]
        print(miss_range)
        template_slice = imglidf[imglidf['slicenum'] == (miss_range[0]-1)]

        drop_idx = (imglidf['slicenum'] >= miss_range[0]) & \
                   (imglidf['slicenum'] <= miss_range[1])

        insert_idx = np.where(drop_idx)[0][0]
        imglidf = imglidf.drop(imglidf[drop_idx].index)
        slice_to_add = pd.DataFrame()
        slicenum_list = range(miss_range[0], miss_range[1]+1)
        for slicenum in slicenum_list:
            newslice = modify_slice(template_slice, slicenum)
            slice_to_add = slice_to_add.append(newslice)

        print(insert_idx)
        print(len(slice_to_add))

        imglidf = insert_dataframe(imglidf, slice_to_add, insert_idx)
        imglidf = imglidf.reset_index(drop=True)
    return imglidf


if __name__=='__main__':
    stack_name = '20190215_Bo_juvenile_overviewstackOBDp'
    result_dir = '/home/hubo/Projects/juvenile_EM/OBDp_overview/imagelist/grid1/'
    indir = os.path.join(result_dir, 'correct_xy')
    infilename = '20190215_Bo_juvenile_overviewstackOBDp_stack_grid0001_xy_corrected_xy_translated_imagelist.csv'
    infile = os.path.join(indir, infilename)

    miss_slice_filename = '20190215_Bo_juvenile_overviewstackOBDp_stack_grid0001_missed_slice.csv'
    miss_slice_file = os.path.join(result_dir, miss_slice_filename)

    outfilename = '{}_add_missing_slice.csv'.format(stack_name)
    outfile = os.path.join(result_dir, 'check_missing_slice', outfilename)

    imglidf = pd.read_csv(infile, index_col=0)
    missdf = pd.read_csv(miss_slice_file, header=None)

    # miss_slice_list = missdf[4].tolist()
    miss_slice_list = [388, 395, 453, 458, 1129, 1134]

    if len(miss_slice_list) % 2:
        raise Exception('miss_slice_list should be pairs')

    imglidf2 = add_missing_slice(imglidf, miss_slice_list)
    valid_imgli, still_missing_idx = validate_image_list(imglidf2)
    imglidf2.to_csv(outfile)
