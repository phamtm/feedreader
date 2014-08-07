from app import db
from app.utils import wilson_score
from ..Base import Base

from BeautifulSoup import BeautifulSoup
import urllib2

MIN_AREA = 250 * 100


class FeedArticle(db.Model):

	__tablename__ 		= 'feedarticle'

	__table_args__		= (
			db.UniqueConstraint('link', 'source_id'),
		)

	id 					= db.Column(db.Integer, primary_key = True)
	title 				= db.Column(db.Unicode(255, convert_unicode = True), nullable = False)
	link 				= db.Column(db.String(511))
	summary				= db.Column(db.UnicodeText(convert_unicode = True))
	thumbnail_url 		= db.Column(db.String(511))
	time_published		= db.Column(db.DateTime, default = db.func.current_timestamp())

	# Readablility processed article
	readable_content 	= db.Column(db.UnicodeText(convert_unicode = True), nullable = True)

	# Vote records
	upvote				= db.Column(db.Integer, default = 0)
	downvote			= db.Column(db.Integer, default = 0)
	wilson_score		= db.Column(db.Float, default = 0.0)
	views				= db.Column(db.Integer, default = 0)

	source_id 			= db.Column(db.Integer, db.ForeignKey('feedsource.id'))


	def update_wilson_score(self):
		self.wilson_score = wilson_score(self.upvote, self.upvote + self.downvote)


	def get_thumbnail_src(self):
		"""
		Extract the thumbnail for an article
		Ignore thumbnail whose:
		width > 3 * height (horizontal strip is likely ads)
		area < MIN_AREA
		"""

		html = ''

		try:
			html = urllib2.urlopen(self.link).read()
		except:
			print('invalid URL: %s' % self.link)

		soup = BeautifulSoup(html, fromEncoding = 'utf-8')

		ims = soup.findAll('img')

		for im in ims:

			# Potential errors here
			w = im.get('width')
			h = im.get('height')

			if not (w and h):
				w = im.get('w')
				h = im.get('h')

			if w and h:
				if w.endswith('px'):
					w = w[0:-2]
				if h.endswith('px'):
					h = h[0:-2]

				w = int(w)
				h = int(h)
				if w < 3 * h and w * h > MIN_AREA:
					self.image_url = im.get('src')
					return


	def __repr__(self):
		return '<FeedArticle %s %s>' % (self.title.encode('utf-8'), self.link.encode('utf-8'))




