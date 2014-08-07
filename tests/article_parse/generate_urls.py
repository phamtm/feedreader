import feedparser

sources = [
		'http://kenh14.vn/home.rss',
		'http://laodong.com.vn/rss/home.rss',
		'http://vnexpress.net/rss/tin-moi-nhat.rss'
	]

urls = []

for source in sources:
	print 'fetching entries for source %s ..' % source
	entries = feedparser.parse(source).entries
	print '\t%d entries fetched' % len(entries)

	article_links = [e.link for e in entries]
	urls.extend(article_links)

print 'Total: %d entries fetched' % len(urls)

print 'Writing to file..'
with open('urls.txt', 'w') as f:
	s = '\n'.join(urls)
	f.write(s)