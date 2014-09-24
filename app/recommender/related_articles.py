from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

from app import db
from app.models import FeedArticle
from app.recommender.vnstemmer import VietnameseStemmer

stemmer = VietnameseStemmer()

def compute_similarity(n = 3):

	# Fetch articles from database
	articles = FeedArticle.query.all()
	docs = [' '.join([stemmer.stem(article.title), article.summary]) for article in articles]
	docids = [article.id for article in articles]

	num_docs = len(docs)
	print docids

	tfidf = compute_tfidf(docs)

	# Map from docid to index in the similarity matrix
	idx_id = {i: docids[i] for i in range(num_docs)}
	print idx_id

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

	db.session.commit()


def compute_tfidf(docs):
	# Compute tfidf and cosine similarity
	vect = TfidfVectorizer(min_df = 1)
	tfidf = vect.fit_transform(docs)
