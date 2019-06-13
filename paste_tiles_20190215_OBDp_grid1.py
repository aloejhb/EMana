from paste_tiles_to_grid3d import plot_tile_pos

imgli_dir = '/home/hubo/Projects/juvenile_EM/OBDp_overview/imagelist/correct_xy_grid1/'
imgli_file = '20190215_Bo_juvenile_overviewstackOBDp_stack_grid0001_xy_corrected_xy_translated_imagelist.csv'
imgli_path = os.path.join(imgli_dir, imgli_file)
imgdf = pd.read_csv(imgli_path)
plot_tile_pos(imgdf[::100])

# platform = 'linux'
# if platform == 'linux':
#     data_root_dir = '/run/user/1000/gvfs/smb-share\:server\=tungsten-nas.fmi.ch\,share\=landing_gmicro_sem/'
#     result_dir = '/home/hubo/Projects/juvenile_EM/OBDp_overview'
# else:
#     data_root_dir = 'W:\landing\gmicro_sem'
#     result_dir = 'M:\hubo\juvenile_EM\OBDp_overview'

# imgli_dir = os.path.join(result_dir, 'imagelist')
# stack_image_dir = os.path.join(result_dir, 'stack_image')
# reload(logging)
# logpath = os.path.join(result_dir, 'paste_tiles.log')
# logging.basicConfig(filename=logpath, level=logging.DEBUG,
#                     format='%(asctime)-15s %(message)s')
# logging.info('Starting to paste tiles ...')


# stack_name = '20190215_Bo_juvenile_overviewstackOBDp'
# gridnum = 5
# imgli_file = '{}_stack_grid{:04}_xy_translated_imagelist.csv'.format(stack_name, gridnum)
# bboxfile =  '{}_stack_grid{:04}_bbox.csv'.format(stack_name, gridnum)

# tile_size_px_py = [2048, 1536]  # unit in px
# pixel_size = 50.0  # unit in um
# overlap = 200  # unit in px

# visualize_tile_pos = True

# # Load image list and bounding box
# imgli_path = os.path.join(imgli_dir, imgli_file)
# imgdf = pd.read_csv(imgli_path)
# bbox = pd.read_csv(os.path.join(imgli_dir, bboxfile))
# print(bbox)
# # Visually check whether the tiles are lying on a grid in a stack
# if visualize_tile_pos:
#     plot_tile_pos(imgdf[::100])
