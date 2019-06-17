import os
import shutil
import glob


def get_file_list(rundir, file_type):
    logdir = os.path.join(rundir, 'meta', 'logs')
    file_pattern = os.path.join(logdir, '{}_*'.format(file_type))
    file_list = sorted(glob.glob(file_pattern))
    return file_list


def concat_files(infile_list, outfile, mode='wb'):
    with open(outfile, mode) as fout:
        for infile in infile_list:
            with open(infile, 'rb') as fin:
                shutil.copyfileobj(fin, fout)
            fout.write(os.linesep.encode('utf-8'))
