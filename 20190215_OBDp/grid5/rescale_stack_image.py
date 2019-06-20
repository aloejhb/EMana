import multiprocessing

pp = Pool(4)
scale_factor = (0.5, 0.5)
args = (scale_factor)
pp.map(rescale_image, )
indir = 'Z:\BoHu\juvenile_EM\OBDp_overview\grid5\stack_image'

outdir = 'Z:\BoHu\juvenile_EM\OBDp_overview\grid5\stack_image_bin2'

