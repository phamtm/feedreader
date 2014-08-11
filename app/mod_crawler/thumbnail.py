from bs4 import BeautifulSoup
import urllib
import urllib2
import os

from flask import current_app
from PIL import Image

"""
Extract the thumbnail for an article

Ignore thumbnail whose:
   width > 3 * height (horizontal strip is likely ads)
   area < 150 * 100

Determine the dimensions:
    First we examine the width and height attribute of each image.
    Then if width and height attributes do not present, the image is downloaded and
    the dimension is retrieved

Storing the thumbnail:
    Location: thumbs
    Original File: <article_id>.<img_extension>
    Resized File: <article_id>_<width>x<height>.<img_extension>
"""

MIN_AREA = 250 * 100


def is_good_dimensions(width, height):
    if width and height and         \
       width < 3 * height and       \
       width * height > MIN_AREA:
        return True
    return False


def get_dimension_attributes(dom):
    w = dom.get('width') or dom.get('w')
    h = dom.get('height') or dom.get('h')

    if not w or not h:
        return (None, None)

    if w.endswith('px'):
        w = w[0:-2]
    if h.endswith('px'):
        h = h[0:-2]

    # do some regex here

    return (int(w), int(h))


def download_pic(url, filename):
    path = os.path.join(current_app.config['THUMBNAIL_DIR'], filename)
    f = urllib.URLopener()

    if url:
        try:
            f.retrieve(url, path)
            return path
        except:
            print 'Cannot download url: ' + url

    return None


def get_thumbnail_src(html):
    if not html:
        return None

    soup = BeautifulSoup(html, 'lxml')

    imgs = soup.findAll('img')

    for img in imgs:
        w, h = get_dimension_attributes(img)

        if not w or not h:
            # Download the image and calculate the dimensions
            path = download_pic(img.get('src'), 'tmp_thumbnail')
            try:
                im = Image.open(path)
            except:
                continue

            w, h = im.size

        # Try to find the dimensions in the width and height attributes
        if is_good_dimensions(w, h):
            return img.get('src')

    return None


if __name__ == '__main__':
    url ='http://kenh14.vn/doi-song/rot-nuoc-mat-vi-gia-canh-khon-cung-cua-a-khoa-29-diem-dh-y-ha-noi-20140802112753999.chn'
    url2 = 'http://www.tinhte.vn/threads/vi-sao-nen-bat-den-khi-di-trong-mua.2336700/'
    url3 = 'http://www.tinhte.vn/threads/hinh-anh-chi-tiet-yamaha-r25-tai-viet-nam-xe-250-cc-nhung-cong-suat-tuong-duong-300-cc.2337018/'
    url4 = 'http://www.tinhte.vn/threads/gioi-thieu-xe-con-tay-va-cach-chay-xe-con-tay.2332010/'
    url5 = 'http://www.triethocduongpho.com/2014/02/28/su-ao-tuong-ve-gia-tri-bang-cap-cua-nguoi-viet/'
    url6 = 'http://cafebiz.vn/quan-tri/chien-luoc-doi-pho-voi-nhung-nhan-vien-dung-nui-nay-trong-nui-no-2014080400265629718ca57.chn'
    url7 = 'http://kenh14.vn/xa-hoi/chim-pha-cho-theo-it-nhat-200-nguoi-o-bangladesh-20140804032054134.chn'
    print 'getting'
    print get_thumbnail_src(url7)