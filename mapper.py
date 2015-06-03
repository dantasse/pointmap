#!/usr/bin/env python

# Mapper for map-reduce building the pointmap.

import sys
sys.path.insert(0, 'pointmap.zip')
import geojson
print geojson
import fileinput, get_nghd

nghds = get_nghd.load_nghds('pointmap.zip/neighborhoods/neighborhoods.json')
tracts = get_nghd.load_tracts('pointmap.zip/tracts/tracts.json')
for line in fileinput.input():
    lat = float(line.split(',')[0])
    lon = float(line.split(',')[1])
    nghd = get_nghd.get_neighborhood_name(nghds, lon, lat)
    tract = get_nghd.get_tract_name(tracts, lon, lat)
    print ','.join((str(lat), str(lon), nghd, tract))

