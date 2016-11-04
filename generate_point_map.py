#!/usr/bin/env python

# Makes a JSON of lat, lon -> neighborhood name. For easier classification of
# neighborhood - you don't have to figure out which neighborhood each point is
# in, just round it off to 3 decimal places and then look it up in the
# point map.

# The map will only go as far as the bounding box of all the neighborhoods. If
# you're outside that bounding box, you're outside the city anyway.

import argparse, numpy, csv, geojson, shapely, shapely.geometry
import shapely.ops, multiprocessing, time

def init_worker(args):
    nghds = args[0] # Each process gets a version of the nghds to use later.

def get_nghd_name(latlon):
    lat, lon = latlon
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
            return [lat, lon, nghd['properties'][args.nghd_param_name]]
            # 'hood' is for pgh_neighborhoods.geojson only.
    return [lat, lon, 'None']

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--neighborhoods_file', default='neighborhoods/pgh_neighborhoods.geojson')
    parser.add_argument('--num_processes', type=int, default=multiprocessing.cpu_count())
    parser.add_argument('--nghd_param_name', default='hood', help='what field in the geojson properties means "the neighborhood name"')
    parser.add_argument('--output_file', '-o', default='point_map.csv')
    args = parser.parse_args()

    writer = csv.writer(open(args.output_file, 'w'))
    writer.writerow(['lat', 'lon', 'nghd', 'tract'])

    print "%s\tReading neighborhoods file." % time.asctime()
    neighborhoods = geojson.load(open(args.neighborhoods_file))
    nghds = neighborhoods['features']
    for nghd in nghds:
        nghd['shape'] = shapely.geometry.asShape(nghd['geometry'])
        nghd['bounds'] = nghd['shape'].bounds
    overall_shape = shapely.ops.cascaded_union([n['shape'] for n in nghds])
    (min_lon, min_lat, max_lon, max_lat) = overall_shape.bounds

    num_pts = ((max_lon - min_lon)/.001) * ((max_lat - min_lat)/.001)
    print "%s\tNumber of points to calculate: %s" % (time.asctime(), str(round(num_pts)))

    worker_pool = multiprocessing.Pool(args.num_processes, init_worker, (nghds,))
    counter = 0
    coords = []
    for lat in numpy.arange(min_lat, max_lat, 0.001):
        for lon in numpy.arange(min_lon, max_lon, 0.001):
            coords.append((round(lat, 3), round(lon, 3)))
    
    results = worker_pool.map(get_nghd_name, coords)
    # Synchronous map; can't go on until this is done.

    print "%s\tCalculated neighborhoods, writing output." % time.asctime()

    for result in results:
        writer.writerow(result + [''])
 
