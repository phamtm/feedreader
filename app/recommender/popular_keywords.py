from nltk.util import ngrams

from app.models import FeedArticle
from app.recommender.vnstemmer import VietnameseStemmer

def top_ngrams(titles, n, num_items):
    """Return the top num_items n-grams"""
    # Get bigrams of each article
    kgrams = [ngrams(title.split(), n) for title in titles]

    # Count the frequency of each bigram
    freq = {}
    for kgrams_list in kgrams:
        for k in kgrams_list:
            if k in freq:
                freq[k] += 1
            else:
                freq[k] = 1
    ff = [(b, freq[b]) for b in freq]
    ff = sorted(ff, key=(lambda a: a[1]), reverse=True)
    return map(lambda x: ' '.join(x[0]), ff[:num_items])

def get_popular_keywords():
    stemmer = VietnameseStemmer()

    # Get all the article titles
    articles = FeedArticle.query.all()
    titles = [article.title for article in articles]
    titles = [stemmer.stem(title) for title in titles]
    top_bigrams = top_ngrams(titles, 2, 10)
    top_trigrams = top_ngrams(titles, 3, 10)

    return top_bigrams + top_trigrams