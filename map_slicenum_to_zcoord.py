import os
import configparser
import json
import numpy as np
import pandas as pd


def delete_slice(all_slicenum_list, slice_to_delete):
    delete_idx = [np.where(all_slicenum_list == x) for x in slice_to_delete]
    all_slicenum_list = np.delete(all_slicenum_list, delete_idx)
    print(len(all_slicenum_list))
    return all_slicenum_list

def get_slice_to_delete(duplicate_config):
    dupslicenum_list = json.loads(duplicate_config['dupslicenum_list'])
    keep_idx_list = json.loads(duplicate_config['keep_idx_list'])
    slice_to_delete = []
    for k in range(len(dupslicenum_list)):
        dupslicenum = dupslicenum_list[k]
        keep_idx = keep_idx_list[k]
        del dupslicenum[keep_idx]
        slice_to_delete.append(dupslicenum)
    return slice_to_delete


def check_substack(all_slicenum_list, slicenum_range, nslice_per_zstep):
    start_idx = np.where(all_slicenum_list == slicenum_range[0])
    start_idx = start_idx[0][0]
    substack_should_be = np.arange(slicenum_range[0],
                                   slicenum_range[1]+nslice_per_zstep,
                                   nslice_per_zstep)
    substack_real = all_slicenum_list[start_idx:start_idx+len(substack_should_be)]
    substack_is_correct = substack_real == substack_should_be
    return substack_is_correct


def check_cutting_thickness(all_slicenum_list, cutting_config):
    slicenum_range_list = json.loads(cutting_config['slicenum_range_list'])
    nslice_per_zstep_list = json.loads(cutting_config['nslice_per_zstep_list'])

    cutting_correct = np.empty(len(slicenum_range_list))
    for k in range(len(slicenum_range_list)):
        slicenum_range = slicenum_range_list[k]
        nslice_per_zstep = nslice_per_zstep_list[k]
        substack_is_correct = check_substack(all_slicenum_list,slicenum_range,
                                             nslice_per_zstep)
        if substack_is_correct.all():
            cutting_correct[k] = True
        else:
            msg = 'Slice number not matched to cutting thickness between slice {:d} to slice {:d}, number of slice per zstep {:d}'.format(slicenum_range[0], slicenum_range[1],nslice_per_zstep)
            print(msg)
            cutting_correct[k] = False

    return cutting_correct.all()

if __name__ == '__main__':
    platform = 'linux'
    if platform == 'linux':
        result_dir = '/home/hubo/Projects/juvenile_EM/OBDp_overview'
    else:
        result_dir = 'M:\hubo\juvenile_EM\OBDp_overview'

    stack_name = '20190215_Bo_juvenile_overviewstackOBDp'
    gridnum = 5

    imgli_dir = os.path.join(result_dir, 'imagelist')

    imgli_file = '{}_stack_grid{:04}_xy_translated_imagelist.csv'.format(stack_name, gridnum)
    imgli_file = imgli_file.replace('.csv', '_add_missing_slice_manually.csv')

    imgli_path = os.path.join(imgli_dir, imgli_file)

    zcoord_dir = os.path.join(imgli_dir, 'zcoord_correction')
    zcoord_config_file = 'zcoord_correction.cfg'
    zcoord_config_path = os.path.join(zcoord_dir, zcoord_config_file)

    imgdf = pd.read_csv(imgli_path)
    all_slicenum_list = np.sort(imgdf['slicenum'].unique())
    print(len(all_slicenum_list))

    zcoord_config = configparser.RawConfigParser()
    zcoord_config.read(zcoord_config_path)

    slice_to_delete = json.loads(zcoord_config['Delete']['slicenum_list'])
    all_slicenum_list = delete_slice(all_slicenum_list, slice_to_delete)
                      
    dupslice_to_delete = get_slice_to_delete(zcoord_config['Duplicate'])
    all_slicenum_list = delete_slice(all_slicenum_list, dupslice_to_delete)

    if 'AdjustCutting' in zcoord_config:
        cutting_correct = check_cutting_thickness(all_slicenum_list,
                                                  zcoord_config['AdjustCutting'])
        if not cutting_correct:
            raise Exception('Substack with altered cutting thickness has unexpected slicenum')
    
    # Save slicenum dataframe
    slicenum_df = pd.DataFrame(all_slicenum_list, columns=['slicenum'])

    outfile = os.path.join(zcoord_dir, 'slicenum_zstep.csv')
    slicenum_df.to_csv(outfile)
    
    # Some code for checking
    # print('-----------------------')
    # dif_list = all_slicenum_list[1:] - all_slicenum_list[:-1]
    # [print(x) for x in all_slicenum_list[np.where(dif_list != 1)]]
