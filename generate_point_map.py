#!/usr/bin/env python

# Makes a JSON of lat, lon -> neighborhood name. For easier classification of
# neighborhood - you don't have to figure out which neighborhood each point is
# in, just round it off to 3 decimal places and then look it up in the
# point map.

# The map will only go as far as the bounding box of all the neighborhoods. If
# you're outside that bounding box, you're outside the city anyway.

import argparse, numpy, csv, get_nghd, geojson, shapely, shapely.geometry
import shapely.ops

def get_nghd_name(nghds, lat, lon):
    point = shapely.geometry.Point(lon, lat)
    for nghd in nghds:
        bounds = nghd['bounds']
        if lon < bounds[0] or lat < bounds[1] or lon > bounds[2] or lat > bounds[3]:
            # Pre-check optimization. If it's outside the bounding box, there's
            # no way it can be within the polygon.
            continue
        if point.within(nghd['shape']):
            # nghds.remove(nghd) # future optimization if necessary
            # nghds.insert(0, nghd)
            return nghd['properties']['hood'] # For pgh_neighborhoods.geojson only.
    return 'None'

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--granularity', '-g', type=float, help="what to round everything to. default=.001.", default=.001)
    parser.add_argument('--output_file', '-o', default='point_map.csv')
    parser.add_argument('--neighborhoods_file', default='neighborhoods/pgh_neighborhoods.geojson')
    args = parser.parse_args()

    writer = csv.DictWriter(open(args.output_file, 'w'), ['lat', 'lon', 'nghd', 'tract'])
    writer.writeheader()

    neighborhoods = geojson.load(open(args.neighborhoods_file))
    nghds = neighborhoods['features']
    for nghd in nghds:
        nghd['shape'] = shapely.geometry.asShape(nghd['geometry'])
        nghd['bounds'] = nghd['shape'].bounds
    overall_shape = shapely.ops.cascaded_union([n['shape'] for n in nghds])
    (min_lon, min_lat, max_lon, max_lat) = overall_shape.bounds

    num_pts = ((max_lon - min_lon)/args.granularity) * ((max_lat - min_lat)/args.granularity)
    print "Number of points to calculate: " + str(round(num_pts))

    counter = 0
    for lat in numpy.arange(min_lat, max_lat, args.granularity):
        for lon in numpy.arange(min_lon, max_lon, args.granularity):
            lat = round(lat, 3)
            lon = round(lon, 3)
            nghd = get_nghd_name(nghds, lat, lon)
            writer.writerow({'lat': lat, 'lon': lon, 'nghd': nghd})
            counter += 1
            if counter % 1000 == 0:
                print counter

