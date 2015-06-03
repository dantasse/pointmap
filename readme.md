# Point map

Tools to generate a mapping that looks like this:

    lat,lon,nghd,tract
    37.779,-122.426,Western Addition,16100
    37.779,-122.425,Western Addition,16100
    37.779,-122.424,Western Addition,16100
    37.779,-122.423,Downtown/Civic Center,16200
    37.779,-122.422,Downtown/Civic Center,16200
    37.779,-122.421,Downtown/Civic Center,16200
    37.779,-122.42,Downtown/Civic Center,12402
    37.779,-122.419,Downtown/Civic Center,12402
    37.779,-122.418,Downtown/Civic Center,12402
    37.779,-122.417,Downtown/Civic Center,12402
    37.779,-122.416,Downtown/Civic Center,12402
    37.779,-122.415,Downtown/Civic Center,12402
    37.779,-122.414,South of Market,17601
    37.779,-122.413,South of Market,17601
    37.779,-122.412,South of Market,17601

This is to help make it easier to classify a point into a neighborhood (somewhat imperfectly). You just take a lat/lon, round to the nearest .001, and pull out the neighborhood and census tract from this mapping here.

The completed thing is point_map.csv.

You can just run generate_point_map.py, but it takes hours. mapper.py is a little experiment trying to get it to run on the grid as a MapReduce streaming job.
