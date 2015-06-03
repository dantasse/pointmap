#!/usr/bin/env python

import geojson, shapely.geometry

#pittsburgh_outline = None
#nghds = []

def load_nghds(neighborhoods_filename):
    neighborhoods = geojson.load(open(neighborhoods_filename))
    nghds = neighborhoods['features']
    for nghd in nghds:
        nghd['shape'] = shapely.geometry.asShape(nghd['geometry'])
#    global pittsburgh_outline
#    pittsburgh_outline = nghds[0]['shape']
#    for nghd in nghds:
#        pittsburgh_outline = pittsburgh_outline.union(nghd['shape'])
    return nghds

def get_neighborhood_name(nghds, lon, lat):
#    global pittsburgh_outline # TODO ugh globals
#    if pittsburgh_outline == None:
#        pittsburgh_outline = nghds[0]['shape']
#        for nghd in nghds:
#            pittsburgh_outline = pittsburgh_outline.union(nghd['shape'])
         
    point = shapely.geometry.Point(lon, lat)
#    if not pittsburgh_outline.contains(point):
#        return 'Outside San Francisco'
    
    for nghd in nghds:
        if nghd['shape'].contains(point):
            # Move this nghd to the front of the queue so it's checked first next time
            nghds.remove(nghd)
            nghds.insert(0, nghd)
            return nghd.properties['neighborho'] # not a typo.
    return 'Outside San Francisco'

def load_tracts(tracts_filename):
    tracts = geojson.load(open(tracts_filename))
    tracts = tracts['features']
    for tract in tracts:
        tract['shape'] = shapely.geometry.asShape(tract['geometry'])
    return tracts

# Returns a string that is the number of the tract that they're in, or -1 if
# not in San Francisco.
def get_tract_number(tracts, lon, lat):
    point = shapely.geometry.Point(lon, lat)
    for tract in tracts:
        if tract['shape'].contains(point):
            # Move this to the front of the queue so it's checked first next time
            tracts.remove(tract)
            tracts.insert(0, tract)
            return tract.properties['Tract2010']
    return '-1'


