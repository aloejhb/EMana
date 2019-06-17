import os
import pandas as pd
import numpy as np
import concatenate_config as ccfg

platform = 'linux'
if platform == 'linux':
    data_root_dir = '/run/user/1000/gvfs/smb-share:server=tungsten-nas.fmi.ch,share=landing_gmicro_sem'
    outdir = '/home/hubo/Projects/juvenile_EM/OBDp_overview/config_list'
else: 
    data_root_dir = 'W:\landing\gmicro_sem'
    outdir = 'M:\hubo\juvenile_EM\OBDp_overview\config_list'


if not os.path.isdir(outdir):
    os.mkdir(outdir)

stack_name = '20190215_Bo_juvenile_overviewstackOBDp'

runnum_list = range(20)
rundir_list = ['{}_run{:03d}'.format(stack_name, x) for x in runnum_list]

section_list = ['grids', 'acq', 'microtome']
keyli_list = [['origin_sx_sy', 'pixel_size', 'tile_size_px_py', 'active_tiles'],
              ['slice_counter', 'slice_thickness'],
              ['stage_scale_factor_x', 'stage_scale_factor_y',
               'stage_rotation_angle_x', 'stage_rotation_angle_y']]
stack_df = ccfg.concat_config_all_run(data_root_dir, rundir_list,
                                      section_list, keyli_list)


# Check wether stage parameter changed
# print(stack_df.nunique())

gridnum = 1
grid1df = pd.DataFrame()
grid1df['origin_sx'] = [x[1][0] for x in stack_df['grids.origin_sx_sy']]
grid1df['origin_sy'] = [x[1][1] for x in stack_df['grids.origin_sx_sy']]

grid1df['pixel_size'] = [x[1] for x in stack_df['grids.pixel_size']]
grid1df['tile_size_px'] = [x[1][0] for x in stack_df['grids.tile_size_px_py']]
grid1df['tile_size_py'] = [x[1][1] for x in stack_df['grids.tile_size_px_py']]

grid1df['slice_counter'] = stack_df['acq.slice_counter']
grid1df['slice_thickness'] = stack_df['acq.slice_thickness']

grid1df['stage_scale_factor_x'] = stack_df['microtome.stage_scale_factor_x']
grid1df['stage_scale_factor_y'] = stack_df['microtome.stage_scale_factor_y']
grid1df['stage_rotation_angle_x'] = stack_df['microtome.stage_rotation_angle_x']
grid1df['stage_rotation_angle_y'] = stack_df['microtome.stage_rotation_angle_y']


grid1df['active_tiles'] = [x[1] for x in stack_df['grids.active_tiles']]
grid1df['active'] = [bool(x) for x in grid1df['active_tiles']]
grid1df = grid1df.loc[grid1df['active']]
grid1df = grid1df.drop('active_tiles', axis=1)

nuniq = grid1df.nunique()

col_uniq = ['pixel_size', 'tile_size_px', 'tile_size_py', 'slice_thickness', 'active', 'stage_scale_factor_x', 'stage_scale_factor_y', 'stage_rotation_angle_x', 'stage_rotation_angle_y']
col_todrop = ['slice_thickness', 'active']
for col in col_uniq:
    if nuniq[col] == 1:
        if col in col_todrop:
            grid1df = grid1df.drop(col, axis=1)
    else:
        raise Exception('Column {} is not unique!'.format(col))

grid1df['diff_origin_sx'] = grid1df['origin_sx'].diff()
grid1df['diff_origin_sy'] = grid1df['origin_sy'].diff()

diff_idx_sx = np.where(grid1df['diff_origin_sx'])[0]
diff_idx_sy = np.where(grid1df['diff_origin_sy'])[0]

diff_idx = set().union(diff_idx_sx, diff_idx_sy)
# diff_idx.remove(0)
diff_idx = sorted(diff_idx)
# diff_idx_pair = sorted(diff_idx + list(np.array(diff_idx) - 1))


orishift_df = grid1df.loc[diff_idx]
print(orishift_df)

outfile = os.path.join(outdir, 'origin_shift_grid1.csv')
orishift_df.to_csv(outfile)
