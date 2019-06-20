import os
import sys
import pandas as pd
import numpy as np
import configparser
import json

sys.path.insert(0, '../../')
from map_slicenum_to_zcoord import delete_slice


platform = 'linux'
if platform == 'linux':
    result_dir = '/home/hubo/Projects/juvenile_EM/OBDp_overview'
else:
    result_dir = 'M:\hubo\juvenile_EM\OBDp_overview'

stack_name = '20190215_Bo_juvenile_overviewstackOBDp'
gridnum = 1

imgli_dir = os.path.join(result_dir, 'imagelist', 'grid{0:d}'.format(gridnum))

imgli_file = '20190215_Bo_juvenile_overviewstackOBDp_add_missing_slice.csv'

imgli_path = os.path.join(imgli_dir, 'check_missing_slice', imgli_file)

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

# Save slicenum dataframe
slicenum_df = pd.DataFrame(all_slicenum_list, columns=['slicenum'])

outfile = os.path.join(zcoord_dir, 'slicenum_zstep.csv')
slicenum_df.to_csv(outfile)

# Some code for checking
# print('-----------------------')
# dif_list = all_slicenum_list[1:] - all_slicenum_list[:-1]
# [print(x) for x in all_slicenum_list[np.where(dif_list != 1)]]
