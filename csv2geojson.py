#!/bin/env python

# {
#   "type": "FeatureCollection",
#   "features": [
#     {
#       "type": "Feature",
#       "id": 1,
#       "properties": {
#         "CASE_ENQUIRY_ID": 101000833162.0,
#         "OPEN_DT": "05/03/2013 11:12:12 AM",
#         "Location": "83-85 Cresthill Rd  Brighton  MA  02135",
#         "LATITUDE": 42.355988,
#         "LONGITUDE": -71.157609
#       },
#       "geometry": {
#         "type": "Point",
#         "coordinates": [
#           -71.157609,
#           42.355988
#         ]
#       }
#     },
#     {
#       "type": "Feature",
#       "id": 2,
#       "properties": {
#         "CASE_ENQUIRY_ID": 101000832197.0,

# Case Number,Date,Year,Type,Country,Area,Location,Activity,Name,Sex,Age,Injury,Fatal,Time,Species,Investigator or Source,Case Number.2,Unnamed: 23,year,month,day,latitude,longitude

import csv
import geojson
import random

id = 0
Feats = [ ]

with open('./sharks_coords.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # Add a title and description based on the relevant fields
        locstr = str(row['Location']) + ', ' + str(row['Area'])
        title = "{:s} ({:d})".format(locstr, int(float(row['year'])))
        description = "{:s}, {:s}, {:s}".format(str(row['Activity']), str(row['Species']), str(row['Injury']))
        row['title'] = title
        row['description'] = description

        # row['marker-color'] = '#ff0000'
        # row['marker-size'] = 'large'

        # "marker-color": "#63b6e5",
        # "marker-size": "large",

        # Add icon descriptor to indicate fatal attacks
        row['icon'] = { 'iconUrl': 'shark-blue.png',
                        'iconSize': [ 35, 90 ],
                        'iconAnchor': [ 17, 45 ],
                        'popupAnchor': [ 17, -45 ],
                        'className': 'dot' }
        if (row['Fatal'] == 'True'):
            row['icon']['iconUrl'] = 'shark-red.png'

        # "icon": {
        #     "iconUrl": "https://www.mapbox.com/mapbox.js/assets/images/astronaut1.png",
        #     "iconSize": [50, 50], // size of the icon
        #     "iconAnchor": [25, 25], // point of the icon which will correspond to marker's location
        #     "popupAnchor": [0, -25], // point from which the popup should open relative to the iconAnchor
        #     "className": "dot"
        # }

        if (row['longitude'] and row['latitude']):
            id += 1
            # Add random jitter of up to approximately 10m (0.0001deg) to visually separate identical locations
            rx = 0.0001*random.random()
            ry = 0.0001*random.random()
            # Create a geojson Point & Feature
            point = geojson.Point((float(row['longitude']) + rx, float(row['latitude']) + ry))
            feat = geojson.Feature(id=id, geometry=point, properties=row)
            Feats.append(feat)

featcoll = geojson.FeatureCollection(Feats)

with open('./sharks_coords.geojson', 'w') as outfile:
    geojson.dump(featcoll, outfile)
