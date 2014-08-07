import time

from thumbnail import get_thumbnail_src
from article import fetch_readable

with open('urls.txt', 'r') as f:
	num_urls = sum(1 for line in f)

with open('urls.txt', 'r') as f:
	t0 = 0.0

	for idx, url in enumerate(f):
		print '%3d/%d %s' % (idx, num_urls, url.strip())
		html = fetch_readable(url)
		t1 = time.time()
		print get_thumbnail_src(html)
		print '=============================================================='
		t2 = time.time()

		t0 += t2 - t1

print 'Num links: %d' % num_urls
print 'Total time: %.3f' % t0
print 'Average time: %.3f' % (t0 / num_urls)