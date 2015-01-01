import pandas, numpy

# Download data from Ministry of Land, Infrastructure, Transport, Tourism
# http://www.land.mlit.go.jp/webland_english/servlet/DownloadServlet
# e.g. http://www.land.mlit.go.jp/webland_english/zip/13_Tokyo_20142_e.zip

pandas.options.display.float_format = '{:,.0f}'.format
pandas.set_option('display.max_rows', 1000)

def read_frame(path):
	return pandas.read_csv(path) \
		.convert_objects(convert_numeric='force') # Force e.g. area as numeric

def add_price_per_sqm_series(frame):
	name = "Price per sqm"
	txprice_series_name = "Transaction-price(total)"
	area_series_name = "Area(m^2)"
	series = frame[txprice_series_name] / frame[area_series_name]
	series.name = name
	frame[name] = series
	return series

def add_desired_area_price_series(frame, price_per_sqm_series, landsize_wanted):
	name = "%d sqm price" % landsize_wanted
	series = price_per_sqm_series * landsize_wanted
	series.name = name
	frame[name] = series
	return series

def filter_residential_land_only(frame):
	return frame[(frame["Type"] == "Residential Land(Land Only)") \
		& (frame["Region"] == "Residential Area")]

def price_by_area(frame, price_per_sqm_series, desired_area_price_series):
	name = "City,Town,Ward,Village"
#	name = "Area"
	return frame.groupby(name) \
		[price_per_sqm_series.name, desired_area_price_series.name] \
		.aggregate(numpy.median) \
		.sort([price_per_sqm_series.name])

def price_by_area_and_year(frame, price_per_sqm_series):
	return pandas.pivot_table(frame, \
			values=price_per_sqm_series.name, \
			index=['year'], \
			columns=['City,Town,Ward,Village'],
			aggfunc=numpy.median)
