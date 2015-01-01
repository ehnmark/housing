#!/usr/local/bin/python

import os, sys
from common import read_frame, filter_residential_land_only, add_price_per_sqm_series, add_desired_area_price_series, price_by_area

# Download data from Ministry of Land, Infrastructure, Transport, Tourism
# http://www.land.mlit.go.jp/webland_english/servlet/DownloadServlet
# e.g. http://www.land.mlit.go.jp/webland_english/zip/13_Tokyo_20142_e.zip

if __name__ == '__main__':
	script = os.path.basename(sys.argv[0])
	if not len(sys.argv) == 3:
		print "Usage: %s data-file wanted-size-m2" % script
		print "Usage: %s data/myfile 100" % script
		print
	else:
		landsize_wanted = int(sys.argv[2])
		frame = read_frame(sys.argv[1])

		price_per_sqm_series 		= add_price_per_sqm_series(frame)
		desired_area_price_series 	= add_desired_area_price_series \
			(frame, price_per_sqm_series, landsize_wanted)
		filtered_frame 				= filter_residential_land_only(frame)

		print price_by_area \
			(filtered_frame, price_per_sqm_series, desired_area_price_series) \
			.dropna()
