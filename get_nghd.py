#!/usr/bin/env python

import geojson

#pittsburgh_outline = None
#nghds = []

# Implementation from http://geospatialpython.com/2011/01/point-in-polygon.html
def point_in_poly(x,y,poly):
    n = len(poly)
    # crummy handling of multi polygons # TODO fix this
    if len(poly[0]) != 2:
        poly = poly[0]
        n = len(poly)
    inside = False
    p1x,p1y = poly[0]
    for i in range(n+1):
        p2x,p2y = poly[i % n]
        if y > min(p1y,p2y):
            if y <= max(p1y,p2y):
                if x <= max(p1x,p2x):
                    if p1y != p2y:
                        xints = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                    if p1x == p2x or x <= xints:
                        inside = not inside
        p1x,p1y = p2x,p2y
    return inside

def load_nghds(neighborhoods_filename):
    neighborhoods = geojson.load(open(neighborhoods_filename))
    nghds = neighborhoods['features']
    for nghd in nghds:
        nghd['shape'] = nghd['geometry']['coordinates'][0]

# TODO This will fail on multi-polygons

        # nghd['shape'] = shapely.geometry.asShape(nghd['geometry'])
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
         
    # point = shapely.geometry.Point(lon, lat)
#    if not pittsburgh_outline.contains(point):
#        return 'Outside San Francisco'
    
    for nghd in nghds:
        # if nghd['shape'].contains(point):
        if point_in_poly(lon, lat, nghd['shape']):
            # Move this nghd to the front of the queue so it's checked first next time
            nghds.remove(nghd)
            nghds.insert(0, nghd)
            return nghd.properties['neighborho'] # not a typo.
    return 'Outside San Francisco'

def load_tracts(tracts_filename):
    tracts = geojson.load(open(tracts_filename))
    tracts = tracts['features']
    for tract in tracts:
        # tract['shape'] = shapely.geometry.asShape(tract['geometry'])
        tract['shape'] = tract['geometry']['coordinates'][0]
    return tracts

# Returns a string that is the number of the tract that they're in, or -1 if
# not in San Francisco.
def get_tract_name(tracts, lon, lat):
    # point = shapely.geometry.Point(lon, lat)
    for tract in tracts:
        # if tract['shape'].contains(point):
        if point_in_poly(lon, lat, tract['shape']):
            # Move this to the front of the queue so it's checked first next time
            tracts.remove(tract)
            tracts.insert(0, tract)
            return tract.properties['Tract2010']
    return '-1'


