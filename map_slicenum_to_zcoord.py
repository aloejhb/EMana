import os
import configparser
import pandas as pd

def transform_z_coordinate(df, zrange_list, shrink, slice_to_del):
    pass
    # This function applies to the stack
    # in which some slices has same distance in z
    # but has index increment bigger than 1
    # if len(slice_to_del):
    #     new_df = df.drop(slice_to_del)
    # for zrange in zrange_list:
    #     # do something

    # return new_df


def delete_single_slice(imgdf, slicenum):
    idx = imgdf.index[imgdf['slicenum'] == slicenum]
    imgdf = imgdf.drop(idx)
    return imgdf


def delete_slice(imgdf, slicenum_list):
    for slicenum in slicenum_list:
        imgdf = delete_single_slice(imgdf, slicenum)
    return imgdf


def delete_duplicated_slice(imgdf, dupslicenum_list, keep_idx_list):
    dupslicenum
    keep_idx

    for k in range(len(dupslicenum)):
        slicenum = dupslicenum[k]
        if k != keep_idx:
            imgdf = delete_single_slice(imgdf, slicenum)
            imgdf = glue_zcoord_gap(imgdf, slicenum)


def adjust_to_cutting_thickness(imgdf, slicenum_range_list,
                                nslict_per_zstep_list):
    slicenum_range
    nslice_per_zstep

    nslice = slicenum_range(2) - slicenum_range(1)  # +nslice_per_zstep?
    nzstep = nslice / nslice_per_zstep

    for zstep in range(nzstep):
        slicenum = slicenum_range(1) + nslice_per_zstep * zstep
        imgdf = glue_zcoord_gap(imdf, slicenum)

    return imgdf
    
if __name__ == '__main__':
    platform = 'linux'
    if platform == 'linux':
        result_dir = '/home/hubo/Projects/juvenile_EM/OBDp_overview'
    else:
        result_dir = 'M:\hubo\juvenile_EM\OBDp_overview'

    stack_name = '20190215_Bo_juvenile_overviewstackOBDp'
    gridnum = 5

    imgli_dir = os.path.join(result_dir, 'imagelist')
    stack_image_dir = os.path.join(result_dir, 'stack_image')

    imgli_file = '{}_stack_grid{:04}_xy_translated_imagelist.csv'.format(stack_name, gridnum)
    imgli_file = imgli_file.replace('.csv', '_add_missing_slice_manually.csv')

    imgli_path = os.path.join(imgli_dir, imgli_file)
    imgdf = pd.read_csv(imgli_path)

    imgdf = imgdf

    zcoord_correct_file = 'zcoord_correction.cfg'
    zcoord_correct_path = os.path.join(imgli_dir, 'zcoord_correction',
                                       zcoord_correct_file)

    zcoord_config = configparser.RawConfigParser()
    zcoord_config.read(zcoord_correct_path)

    imgdf['zstep'] = imgdf['slicenum']

    imgdf = delete_slice(imgdf, zcoord_config['Delete']['slicenum_list'])

    imgdf = delete_duplicated_slice(imgdf, zcoord_config['Duplicate'])

    imgdf = adjust_to_cutting_thickness(imgdf, zcoord_config['AdjustCutting'])
    
