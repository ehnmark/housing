#!/usr/local/bin/python

import os, sys, pandas, numpy

# Download data from 
# http://www.land.mlit.go.jp/webland_english/servlet/DownloadServlet
# e.g. http://www.land.mlit.go.jp/webland_english/zip/13_Tokyo_20142_e.zip
# 13 = all of tokyo, 20142 = 2nd qtr 2014 (latest at the time), 

pandas.options.display.float_format = '{:,.0f}'.format
pandas.set_option('display.max_rows', 1000)

def read_frame(path):
	return pandas.read_csv(path) \
		.convert_objects(convert_numeric='force') # Force e.g. area as numeric

def add_price_per_sqm_series(frame):
	name = "Price per sqm"
	txpxcol = "Transaction-price(total)"
	areacol = "Area(m^2)"
	series = frame[txpxcol] / frame[areacol]
	series.name = name
	frame[name] = series
	return series

def add_price_at_wanted_size_series(frame, m2pxseries, sizewanted):
	name = "Price for %d sqm" % sizewanted
	series = m2pxseries * sizewanted
	series.name = name
	frame[name] = series
	return series

def filter_residential_land_only(frame):
	name = "Type"
	value = "Residential Land(Land Only)"
	return frame[frame[name] == value]

def price_by_area(frame, price_per_sqm_series, price_at_wanted_size_series):
	name = "City,Town,Ward,Village"
#	name = "Area"
	return landonly.groupby(name)[price_per_sqm_series.name, price_at_wanted_size_series.name] \
		.aggregate(numpy.median) \
		.sort([price_per_sqm_series.name])

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
		price_at_wanted_size_series = add_price_at_wanted_size_series(frame, price_per_sqm_series, landsize_wanted)

		landonly = filter_residential_land_only(frame)

		print price_by_area(landonly, price_per_sqm_series, price_at_wanted_size_series).dropna()
