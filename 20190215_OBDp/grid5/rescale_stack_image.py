import multiprocessing

pp = Pool(4)
scale_factor = (0.5, 0.5)
args = (scale_factor)
pp.map(rescale_image, )
