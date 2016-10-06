
`pgh_neighborhoods.geojson` is `Pittsburgh_Neighborhoods.geojson` from the City of Pittsburgh, [link](https://data.wprdc.org/dataset/pittsburgh-neighborhoods2de67)

sf_neighborhoods boundaries from
https://data.sfgov.org/Geographic-Locations-and-Boundaries/Neighborhood-Groups-Map/qc6m-r4ih

GeoJSON file created with:
ogr2ogr -f GeoJSON -t_srs EPSG:4326 sf_neighborhoods.json planning_neighborhoods.shp
