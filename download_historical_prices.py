#!/usr/local/bin/python

import os, sys, urllib, urllib2, time, zipfile

def create_unless_exists(dirname):
	def split(d, acc):
		p = os.path.dirname(d)
		if p == '': return acc
		else: return split(p, [p] + acc)
	for d in split(dirname, [dirname]): 
		if not os.path.isdir(d): os.mkdir(d)

def extract_and_cleanup(dirname):
	zipfilter = lambda x: x.upper().endswith("ZIP")
	for file in filter(zipfilter, os.listdir(dirname)):
		path = os.path.join(dirname, file)
		with zipfile.ZipFile(path, "r") as z:
			z.extractall(dirname)
		os.unlink(path)

def download_uri(uri, path):
	urllib.URLopener().retrieve(uri, path)

def try_download(prefecture, town, year, quarter, dstdir):
	create_unless_exists(dstdir)
	rq_uri = "http://www.land.mlit.go.jp/webland_english/servlet/DownloadServlet?DLF=true&TTC=%(year)d%(quarter)d&TDK=%(prefecture)d&SKC=%(prefecture)d%(town)d" % locals()
	dl_uri = "http://www.land.mlit.go.jp/webland_english/zip/%(prefecture)d%(town)d_%(year)d%(quarter)d_e.zip" % locals()
	path = os.path.join(dstdir, os.path.basename(dl_uri))
	try:
		urllib2.urlopen(rq_uri).read()
		time.sleep(2)	
		download_uri(dl_uri, path)
		time.sleep(2)	
		print "Downloaded", dl_uri
	except Exception, e:
		print "Skipping", dl_uri, e

# Looks like there are no combined (all-Japan or all-Tokyo) archives
# for past data, but there are per-town archives

if __name__ == '__main__':
	script = os.path.basename(sys.argv[0])

	prefecture = 13 # tokyo
	towns = [101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 218, 219, 220, 221, 222, 223, 224, 225, 227, 228, 229, 303, 305, 307, 308, 361, 362, 363, 364, 381, 382, 401, 402, 421]
	years = range(2005, 2015)
	quarters = range(1, 5)
	combinations = [(y, q) for q in quarters for y in years]

	for town in towns:
		dstdir = os.path.join("var", "%d-%d" % (prefecture, town))
		for (y, q) in combinations:	
			try_download(prefecture, town, y, q, dstdir)
		extract_and_cleanup(dstdir)	
