import feedparser
from bs4 import BeautifulSoup
from vnstemmer import vnstring_to_ascii as vna

def strip_html(html):
	html = html.replace('nbsp;', ' ')
	soup = BeautifulSoup(html, 'lxml')
	stripped_html = ' '.join(soup.findAll(text = True))
	ascii_text = unicode(vna(stripped_html))

	return unicode(ascii_text)


output = 'docs.txt'

url = 'http://kenh14.vn/home.rss'
entries = feedparser.parse(url).entries
print entries[0].title
print entries[0].summary.strip()
print strip_html(entries[0].summary)


titles = [e.title.strip() for e in entries]
titles = map(vna, titles)

summaries = [e.summary.strip() for e in entries]
summaries = map(strip_html, summaries)

docs = [' '.join([titles[i], summaries[i]]) for i in range(len(titles))]


with open(output, 'a') as f:
	f.write('\n'.join(docs))