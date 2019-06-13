import os
import glob
import configparser
import pandas as pd


def config_to_dataframe(file_path, section_list, keyli_list):
    file_name = os.path.basename(file_path)
    df = pd.DataFrame([file_name], columns=['file_name'])
    parser = configparser.ConfigParser()
    parser.read(file_path)
    for section, keyli in zip(section_list, keyli_list):
        for key in keyli:
            value = json.loads(parser[section][key]
            colname = '{}.{}'.format(section, key)
            df[colname] = [value]
    return df


def get_file_list(rundir, file_type):
    logdir = os.path.join(rundir, 'meta', 'logs')
    file_pattern = os.path.join(logdir, '{}_*'.format(file_type))
    file_list = sorted(glob.glob(file_pattern))
    return file_list


def concat_config_to_dataframe(data_root_dir, rundir, section_list, keyli_list):
    rundir_fp = os.path.join(data_root_dir, rundir)
    file_list = get_file_list(rundir_fp, 'config')
    df_list = [config_to_dataframe(fi, section_list, keyli_list) for fi in file_list]
    df = pd.concat(df_list)
    df['rundir'] = rundir
    return df


def concat_config_all_run(data_root_dir, rundir_list, section_list, keyli_list):
    all_run_df_list = [concat_config_to_dataframe(data_root_dir, rundir,
                                                  section_list, keyli_list)
                       for rundir in rundir_list]
    all_run_df = pd.concat(all_run_df_list)
    all_run_df = all_run_df.reset_index()
    return all_run_df


if __name__ == '__main__':
    platform = 'linux'
    if platform == 'linux':
        data_root_dir = '/run/user/1000/gvfs/smb-share:server=tungsten-nas.fmi.ch,share=landing_gmicro_sem'
        outdir = '/home/hubo/Projects/juvenile_EM/OBDp_overview/config_list'
    else: 
        data_root_dir = 'W:\landing\gmicro_sem'
        outdir = 'M:\hubo\juvenile_EM\OBDp_overview\config_list'

    stack_name = '20190215_Bo_juvenile_overviewstackOBDp'

    runnum_list = range(20)
    rundir_list = ['{}_run{:03d}'.format(stack_name, x) for x in runnum_list]

    section_list = ['grids', 'acq', 'sem']
    keyli_list = [['origin_sx_sy', 'pixel_size', 'tile_size_px_py'],
                  ['slice_counter', 'slice_thickness']]
    all_run_df = concat_config_all_run(data_root_dir, rundir_list, section_list, keyli_list)
