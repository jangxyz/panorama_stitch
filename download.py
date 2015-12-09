#!/usr/local/bin/python
# -*- encoding: utf-8 -*-

'''

    Download Naver Map Street View images


'''

usage = ''' Usage: %s pano_id '''

import sys, time, os
import urllib, urllib2, urlparse

def get_filename(url):
    if not url.startswith('http://'):
        url = 'http://' + url
    parsed = urlparse.urlparse(url)
    #
    subdomain = parsed.hostname.split('.')[0]
    query_dict = urlparse.parse_qs(parsed.query)
    reqtype = query_dict['type'][0]
    pano_id = query_dict['pano_id'][0]
    #
    if subdomain == 'pvxml':
        extra = query_dict['rv'][0]
    else:
        extra = query_dict['suffix'][0]
    #
    suffix = reqtype
    if reqtype == 'img':
        suffix = 'jpg'
    #
    return "%s-%s.%s.%s" % (urllib.quote_plus(pano_id), extra, subdomain, suffix)


def download(url, filename):
    if not url.startswith('http://'):
        url = 'http://' + url
    return urllib.urlretrieve(url, filename)

def download_file(filename):
    if filename == '-':
        filename = '/dev/stdin'

    # action
    for i,line in enumerate(open(filename)):
        url = line.strip()
        image_filename = get_filename(url)
        print i+1, url, '-->', image_filename, '...',
        ret = ''
        ret = download(url, image_filename)
        print ret[1]
        #
        time.sleep(0.2)

def generate_h_urls(pano_id):
    #http://pvimgmb.map.naver.com/api/get?type=img&pano_id=uiCt4wVwsRbjcNBVXJcvxQ==&suffix=_M_r_02_02
    directions = ('b', 'd', 'f', 'l', 'r', 'u')
    n = 8
    subdomain = 'pvimgh'
    res = 'H'
    return [
        'http://%s.map.naver.com/api/get?type=img&pano_id=%s&suffix=_%s_%s_%02d_%02d' % (subdomain, pano_id, res, d, x,y)
            for d in directions 
                for x in range(1,n+1) 
                    for y in range(1,n+1)
    ]


#
if __name__ == '__main__':
    if len(sys.argv) < 1:
        print usage
        sys.exit()

    url = sys.argv[1]
    pano_id = urllib.unquote(url)
    os.makedirs(pano_id)
    for i,url in enumerate(generate_h_urls(pano_id)):
        image_filename = get_filename(url)
        print i+1, url, '-->', image_filename, '...',
        ret = download(url, os.path.join(pano_id, image_filename))
        print ret[1]
        #
        time.sleep(0.2)

# vim: sts=4 et
