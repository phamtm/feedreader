from breadability.readable import Article
from article import fetch_readable

import time

# Number of invalid links
num_invalid = 0

with open('urls.txt', 'r') as f:
	num_urls = sum(1 for line in f)

with open('urls.txt', 'r') as f:

	# Measure the average time for each article
	t0 = 0.0

	for idx, url in enumerate(f):
		print '%3d/%d %s' % (idx, num_urls, url)

		t1 = time.time()
		readable_content = fetch_readable(url)
		t2 = time.time()

		# Only measure the time for successful processing
		if readable_content:
			t0 += t2 - t1
		else:
			num_invalid += 1

	print 'Num of links: %d' % num_urls
	print 'Num of invalid links: %d' % num_invalid
	print 'Total time: %.3fs' % t0
	print 'Average: %.3fs' % (t0 / num_urls)