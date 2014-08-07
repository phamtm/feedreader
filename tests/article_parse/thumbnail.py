from BeautifulSoup import BeautifulSoup
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
	if width and height and 		\
	   width < 3 * height and 		\
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
	path = os.path.join('.', filename)
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

	soup = BeautifulSoup(html)

	imgs = soup.findAll('img')

	for img in imgs:
		w, h = get_dimension_attributes(img)

		if not w or not h:
			# Download the image and calculate the dimensions
			path = download_pic(img.get('src'), 'tmp')
			try:
				im = Image.open(path)
			except:
				continue

			w, h = im.size

		# Try to find the dimensions in the width and height attributes
		if is_good_dimensions(w, h):
			return img.get('src')

	return None