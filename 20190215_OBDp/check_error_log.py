import os
# import sys
# sys.path.insert(0, '/path/to/application/app/folder')
data_root_dir = '/run/user/1000/gvfs/smb-share:server=tungsten-nas.fmi.ch,share=landing_gmicro_sem'
result_dir = '/home/hubo/Projects/juvenile_EM/OBDp_overview/'

os.chdir(data_root_dir)
stack_name = '20190215_Bo_juvenile_overviewstackOBDp'
error_file_name = 'error_list.txt'
error_file = os.path.join(result_dir, error_file_name)
cmd = 'cat {}*/meta/logs/error_* > {}'.format(stack_name, error_file)
# print(cmd)
os.system(cmd)

