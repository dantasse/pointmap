#!/usr/bin/env python

# Mapper for map-reduce building the pointmap.

import fileinput, get_nghd

nghds = get_nghd.load_nghds('neighborhoods/neighborhoods.json')
tracts = get_nghd.load_tracts('tracts/tracts.json')
for line in fileinput.input():
    lat = float(line.split(',')[0])
    lon = float(line.split(',')[1])
    nghd = get_nghd.get_neighborhood_name(nghds, lon, lat)
    tract = get_nghd.get_tract_name(tracts, lon, lat)
    print ','.join((str(lat), str(lon), nghd, tract))

