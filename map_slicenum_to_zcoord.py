
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


if __name__ == '__main__':
    platform = 'vm2'
    if platform == 'linux':
        result_dir = '/home/hubo/Projects/juvenile_EM/OBDp_overview'
    else:
        result_dir = 'M:\hubo\juvenile_EM\OBDp_overview'

    stack_name = '20190215_Bo_juvenile_overviewstackOBDp'
    gridnum = 5

    imgli_dir = os.path.join(result_dir, 'imagelist')
    stack_image_dir = os.path.join(result_dir, 'stack_image')

    imgli_file = '{}_stack_grid{:04}_xy_translated_imagelist.csv'.format(stack_name, gridnum)

    imgli_path = os.path.join(imgli_dir, imgli_file)
    imgdf = pd.read_csv(imgli_path)

    imgdf = imgdf
