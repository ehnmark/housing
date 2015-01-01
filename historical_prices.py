#!/usr/local/bin/python

import os, sys, re, pandas
from common import read_frame, filter_residential_land_only, add_price_per_sqm_series, price_by_area_and_year

def find_csv_files(basedir):
	return [os.path.join(dp, f) \
		for dp, dn, filenames in os.walk(basedir) \
		for f in filenames if os.path.splitext(f)[1] == '.csv']

def read_frame_and_add_date_column(path):
	year = re.search("(20\d\d)", path).groups()[0]
	frame = read_frame(path)
	frame["year"] = year
	return frame

def read_frames(dirname):
	return map(read_frame_and_add_date_column, find_csv_files(dirname))

if __name__ == '__main__':
	script = os.path.basename(sys.argv[0])
	if not len(sys.argv) == 2:
		print "Usage: %s data-dir" % script
		print "Usage: %s var" % script
		print
	else:
		frames = read_frames(sys.argv[1])
		frame = pandas.concat(frames)

		price_per_sqm_series 		= add_price_per_sqm_series(frame)
		filtered_frame 				= filter_residential_land_only(frame)

		report = price_by_area_and_year(filtered_frame, price_per_sqm_series)
		print report
		report.to_csv("report.csv")
