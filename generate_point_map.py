#!/usr/bin/env python

# Makes a JSON of lat, lon -> neighborhood name. For easier classification of
# neighborhood - you don't have to figure out which neighborhood each point is
# in, just round it off to 3 decimal places and then look it up in the
# point map.

#-123.0137, 37.6040, -122.3549, 37.8324

import argparse, numpy, csv, get_nghd
#import util.util, util.neighborhoods, util.census

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--granularity', '-g', type=float, default=.001)
    parser.add_argument('--outfile', '-o', default='point_map.csv')
    args = parser.parse_args()

    nghds = get_nghd.load_nghds('neighborhoods/neighborhoods.json')

    writer = csv.DictWriter(open(args.outfile, 'w'), ['lat', 'lon', 'nghd'])
#        'tract', 'block_group', 'block'])
    writer.writerow({'lat': 'lat', 'lon': 'lon', 'nghd': 'nghd'})
    # no writeheader in python 2.6

    counter = 0
    for lat in numpy.arange(37.6040, 37.8324, args.granularity):
        for lon in numpy.arange(-123.0137, -122.3549, args.granularity):
            lat = round(lat, 3)
            lon = round(lon, 3)
            nghd = get_nghd.get_neighborhood_name(nghds, lon, lat)
#            tract = util.census.get_tract_name(lat, lon)
#            group = util.census.get_group_ID(lat, lon)
#            block = util.census.get_block_name(lat, lon)
#            writer.writerow({'lat': lat, 'lon': lon, 'nghd': nghd,
#                'tract': tract, 'block_group': group, 'block': block})
            writer.writerow({'lat': lat, 'lon': lon, 'nghd': nghd})
            counter += 1
            if counter % 1000 == 0:
                print counter

