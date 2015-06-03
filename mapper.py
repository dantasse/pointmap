#!/usr/bin/env python

# Mapper for map-reduce building the pointmap.

import sys
sys.path.insert(0, 'pointmap.zip')
import env.lib.geojson as geojson
import fileinput, get_nghd, zipfile

datafile = zipfile.ZipFile('pointmap.zip')
nghds = get_nghd.load_nghds(datafile.open('neighborhoods/neighborhoods.json'))
tracts = get_nghd.load_tracts(datafile.open('tracts/tracts.json'))
for line in fileinput.input():
    lat = float(line.split(',')[0])
    lon = float(line.split(',')[1])
    nghd = get_nghd.get_neighborhood_name(nghds, lon, lat)
    tract = get_nghd.get_tract_name(tracts, lon, lat)
    print ','.join((str(lat), str(lon), str(nghd), str(tract)))

datafile.close()
