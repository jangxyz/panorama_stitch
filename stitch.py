#!/usr/local/bin/python
# -*- coding: utf-8 -*-

'''

    Stitch Naver Map Street View images


'''

usage = ''' Usage: %s pano_id '''


import sys, os
import urllib
from PIL import Image

# filename = 'uiCt4wVwsRbjcNBVXJcvxQ%3D%3D-_M_b_01_01.pvimgmb.jpg',

#pano_id   = 'uiCt4wVwsRbjcNBVXJcvxQ%3D%3D'
pano_id = urllib.unquote(sys.argv[1])
#res       = 'M'
#res       = 'L'
res       = 'H'

#input_dir  = urllib.quote_plus(pano_id).replace('%2B', '+')
input_dir  = pano_id
output_dir = 'stitched'

#subdomain = 'pvimgmb'
#subdomain = 'pvimgm'
subdomain = 'pvimgh'

directions = ('b', 'd', 'f', 'l', 'r', 'u')
#n = 2
#n = 4
n = 8

TILE_SIZE = 256

def get_filename(subdomain, pano_id, res, direction, x, y):
    pano_id = urllib.quote_plus(pano_id).replace('%2B', '+')
    return '%s-_%s_%s_%02d_%02d.%s.jpg' % (pano_id, res, direction, x, y, subdomain)

def stitch_per_direction(direction, subdomain, pano_id, res):
    size = TILE_SIZE
    result_img = Image.new("RGB", (size * n,size * n), "white")
    #
    for x in range(1,n+1):
        for y in range(1,n+1):
            filename = get_filename(subdomain, pano_id, res, direction, x, y)
            filename = os.path.join(input_dir, filename)
            #
            image = Image.open(filename)
            result_img.paste(image.copy(), (size * (x-1),size * (y-1), size * x,size * y))
    #
    return result_img

def stitch_6_directions(images):
    size = images.values()[0].width
    #
    result_img = Image.new("RGB", (size * 6, size * 1), "white")
    #
    result_img.paste(images['l'].copy(), (size * 0,0, size * 1,size))
    result_img.paste(images['f'].copy(), (size * 1,0, size * 2,size))
    result_img.paste(images['r'].copy(), (size * 2,0, size * 3,size))
    result_img.paste(images['b'].copy(), (size * 3,0, size * 4,size))
    result_img.paste(images['d'].copy(), (size * 4,0, size * 5,size))
    result_img.paste(images['u'].copy(), (size * 5,0, size * 6,size))
    #
    return result_img


#
if __name__ == '__main__':

    # stitch per direction
    images = {}
    for d in directions:
        outfilename = '%s-%s-%s.%s.jpg' % (pano_id, res, d, subdomain)
        outfilepath = os.path.join(output_dir, outfilename)
        try:
            os.mkdir(os.path.dirname(outfilepath))
        except OSError, e:
            print e
            pass
        img = stitch_per_direction(d, subdomain, pano_id, res)
        img.save(outfilepath, 'JPEG')
        print '%s:' % d, outfilename
        # 
        images[d] = img
    # stitch 6 directions
    outfilename = '%s-%s.%s.jpg' % (pano_id, res, subdomain)
    stitched6 = stitch_6_directions(images)
    stitched6.save(os.path.join(output_dir, outfilename), 'JPEG')
    print 'stitched 6:', outfilename


# vim: sts=4 et
