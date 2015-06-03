#!/usr/bin/env python

# Makes a JSON of lat, lon -> neighborhood name. For easier classification of
# neighborhood - you don't have to figure out which neighborhood each point is
# in, just round it off to 3 decimal places and then look it up in the
# point map.

#-122.518, 37.705, -122.350, 37.834

import argparse, numpy, csv, get_nghd

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--granularity', '-g', type=float, default=.001)
    # Defaults are for SF
    parser.add_argument('--min_lat', type=float, default=37.705)
    parser.add_argument('--max_lat', type=float, default=37.834)
    parser.add_argument('--min_lon', type=float, default=-122.518)
    parser.add_argument('--max_lon', type=float, default=-122.350)
    parser.add_argument('--outfile', '-o', default='point_map.csv')
    args = parser.parse_args()

    nghds = get_nghd.load_nghds('neighborhoods/neighborhoods.json')
    tracts = get_nghd.load_tracts('tracts/tracts.json')

    writer = csv.DictWriter(open(args.outfile, 'w'), ['lat', 'lon', 'nghd', 'tract'])
#        'tract', 'block_group', 'block'])
    writer.writerow({'lat': 'lat', 'lon': 'lon', 'nghd': 'nghd', 'tract': 'tract'})
    # no writeheader in python 2.6

    min_lat = args.min_lat
    max_lat = args.max_lat
    min_lon = args.min_lon
    max_lon = args.max_lon
    num_pts = ((max_lon - min_lon)/args.granularity) * ((max_lat - min_lat)/args.granularity)
    print "Number of points to calculate: " + str(num_pts)

    counter = 0
    for lat in numpy.arange(min_lat, max_lat, args.granularity):
        for lon in numpy.arange(min_lon, max_lon, args.granularity):
            lat = round(lat, 3)
            lon = round(lon, 3)
            nghd = get_nghd.get_neighborhood_name(nghds, lon, lat)
            tract = get_nghd.get_tract_name(tracts, lat, lon)
#            group = util.census.get_group_ID(lat, lon)
#            block = util.census.get_block_name(lat, lon)
#            writer.writerow({'lat': lat, 'lon': lon, 'nghd': nghd,
#                'tract': tract, 'block_group': group, 'block': block})
            writer.writerow({'lat': lat, 'lon': lon, 'nghd': nghd, 'tract': tract})
            counter += 1
            if counter % 1000 == 0:
                print counter

