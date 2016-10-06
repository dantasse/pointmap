#!/usr/bin/env python

import numpy, argparse, csv

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--granularity', '-g', type=float, default=.001)
    # Defaults are for SF
    parser.add_argument('--min_lat', type=float, default=37.705)
    parser.add_argument('--max_lat', type=float, default=37.834)
    parser.add_argument('--min_lon', type=float, default=-122.518)
    parser.add_argument('--max_lon', type=float, default=-122.350)
    parser.add_argument('--outfile', '-o', default='points.csv')
    args = parser.parse_args()

    writer = csv.DictWriter(open(args.outfile, 'w'), ['lat', 'lon'])
    writer.writerow({'lat': 'lat', 'lon': 'lon'})

    for lat in numpy.arange(args.min_lat, args.max_lat, args.granularity):
        for lon in numpy.arange(args.min_lon, args.max_lon, args.granularity):
            writer.writerow({'lat': round(lat, 3), 'lon': round(lon, 3)})
