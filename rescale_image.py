import os
import numpy as np
from PIL import Image

def rescale_image(img, scale_factor=(1, 1)):
    original_size = np.array(img.size)
    new_size = tuple(np.floor(original_size / np.array(scale_factor)).astype(int))
    img = img.resize(new_size, Image.BILINEAR)
    return img

if __name__ == '__main__':
    indir = 'Z:\BoHu\juvenile_EM\OBDp_overview\grid5\stack_image'
    infilename = '20190215_Bo_juvenile_overviewstackOBDp_slice02290.tif'
    infile = os.path.join(indir, infilename)
    
    outdir = 'Z:\BoHu\juvenile_EM\OBDp_overview\grid5\stack_image_bin2'
    outfilename = 'test.tif'
    outfile = os.path.join(outdir, outfilename)
    
    scale_factor = (0.5, 0.5)
    img = Image.open(infile)
    rimg = rescale_image(img, scale_factor)
    rimg.save(outfile) 
    