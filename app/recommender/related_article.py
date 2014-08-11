from app import db
from app.models import FeedArticle

from vnstemmer import vnstring_to_ascii as vna
from sklearn.feature_extraction.text import TfidfVectorizer


def compute_tfidf(n = 5):

	# Fetch articles from database
	articles = FeedArticle.query.all()
	docs = [' '.join([vna(article.title), article.summary_ascii]) for article in articles]
	docids = [article.id for article in articles]

	num_docs = len(docs)
	print docids

	# Map from docid to index in the similarity matrix
	id_idx = {docids[i]: i for i in range(num_docs)}
	idx_id = {i: docids[i] for i in range(num_docs)}
	print idx_id

	# Compute tfidf and cosine similarity
	vect = TfidfVectorizer(min_df = 1)
	tfidf = vect.fit_transform(docs)
	similarity = (tfidf * tfidf.T).A

	# Return top n results for each document
	res = []
	for i in range(num_docs):
		score_tups = [(similarity[i][j], idx_id[j]) for j in range(num_docs)]
		score_tups = sorted(score_tups, reverse = True)
		top_n = [doc[1] for doc in score_tups[1:n+1]]
		print top_n

		# Update in database the relevant articles for each article
		article = FeedArticle.query.get(idx_id[i])
		if article:
			related = ' '.join(map(str, top_n))
			article.related_articles = related
			print related

	db.session.commit()


def get_related_article(article_id):
	pass