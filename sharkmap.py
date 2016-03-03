#!/usr/bin/env python

import itertools
import pandas as pd
import numpy as np
import re
import sys
import time
from geopy.geocoders import GoogleV3
from geopy.geocoders import Nominatim

reload(sys)
sys.setdefaultencoding('utf8')


# Clean our Fatal column up
def clean_Fatal(x):
    if x == 'Y':
        return True
    elif x == 'UNKNOWN':
        return ''
    else:
        return False

# Clean up our dates w/ some regex-ing
def year(x):
    res = re.search(r'([0-9]{4})',str(x))
    if res is None:
        return None
    else:
        return int(res.group())

def day(x):
    res = re.search(r'(^|\b)(([0-9]{2}))(?=-)',str(x))
    if res is None:
        return None
    else:
        return int(res.group())

def month(x):
    res = re.search(r'(?!-)(([A-Za-z]{3}))(?=-)',str(x))
    if res is None:
        return None
    else:
        return str(res.group())

# http://stackoverflow.com/questions/12130883/r-expand-grid-function-in-python
def expandgrid(*itrs):
   product = list(itertools.product(*itrs))
   return {'Var{}'.format(i+1):[x[i] for x in product] for i in range(len(itrs))}

def types(x):
    #x = x.encode('utf-8').strip()
    if re.search(r'\bscuba\b',str(x)):
        x='scuba_diving'
        return x
    elif re.search(r"\bspearfishing\b",str(x)) and not(re.search(r'\bscuba\b',str(x))):
        x = 'spear_fishing'
        return x
    elif re.search(r"\bswimming\b",str(x)):
        x = 'swimming'
        return x
    elif re.search(r"\bstanding\b",str(x)):
        x = 'standing'
        return x
    elif re.search("bodysurfing",str(x)) or (re.search("body surfing",str(x))):
        x = 'body_surfing'
        return x
    elif re.search("bodyboarding",str(x)) or (re.search("body-boarding",str(x)))or (re.search("body boarding",str(x))):
        x = 'body_boarding'
        return x
    elif re.search(r"\bsurfing\b",str(x)) or (re.search("surfboard",str(x))):
        x = 'surfing'
        return x
    elif re.search("surf-skiing",str(x)) or (re.search("surf skiing",str(x))) or (re.search("surfskiing",str(x))):
        x = 'surf_skiing'
        return x
    elif re.search("pearl diving",str(x)):
        x = 'pearl_diving'
        return x
    elif re.search(r"\bdiving\b",str(x)):
        x = 'diving'
        return x
    elif re.search(r"\bspear\b",str(x)):
        x = 'spear_fishing'
        return x
    elif re.search(r"\bbathing\b",str(x)):
        x = 'bathing'
        return x
    elif re.search(r"\bfishing\b",str(x)):
        x = 'fishing'
        return x
    elif re.search(r"\bfreediving\b",str(x)) or (re.search("free diving",str(x))):
        x = 'free_diving'
        return x
    elif re.search("boogie",str(x)):
        x = 'boogie_boarding'
        return x
    elif re.search("capsized",str(x)) or (re.search("sank",str(x))) or (re.search("went down",str(x)))     or (re.search("disaster",str(x))) or (re.search("crash",str(x))) or (re.search("wreck",str(x))):
        x = 'sea_disaster'
        return x
    elif re.search(r"\bwading\b",str(x)):
        x = 'wading'
        return x
    else: return x


class GeoLocation(object):
    """Class to hold get_location method."""

    # Initialise internal counter
    count = 1

    def get_location(self, row):
        """Return the latitude & longitude of a descriptive location."""

        time.sleep(.02)
        location = str(row.Location)
        # location = re.sub(r"\s*[\(\[\{\;\:\.\-]\s*", ", ", location)
        location = re.sub(r"\s*[\(\)\[\]\{\}\;\:\,\.\-]\s*", " ", location)
        # location = re.sub(r"[^a-zA-Z0-9\s,]", "", location)
        location = re.sub(r"[^a-zA-Z0-9\s]", "", location)
        location = re.sub(r"(at|in|near|on)\sthe", "the", location)
        # s = re.split(r"\s*(?:at|in|near|on|,)+\s*", location, flags=re.IGNORECASE)
        # if (len(s) > 1):
        #     location = s[1]

        loc = location + ', ' + str(row.Area) + ', ' + str(row.Country)
        for _ in range(1):
            try:
                # try our first geocoder
                gloc = geolocator.geocode(loc)
                print "[{:d}] GoogleV3: {:s} ({:d}) {:s}, {:s}".format(self.count, loc, int(float(row.year)), str(row.Activity), str(row.Species))
                # print row.index
                # print row
                if not gloc==None:
                    lat = gloc[1][0]
                    long = gloc[1][1]
                    self.count += 1
                    return lat, long
                else:
                    try:
                        # try our second geocoder if first one fails
                        gloc = geolocator.geocode2(loc)
                        print "[{:d}] Nominatim: {:s} ({:d}) {:s}, {:s}".format(self.count, loc, int(float(row.year)), str(row.Activity), str(row.Species))
                        # print row.index
                        # print row
                        if not gloc==None:
                            lat = gloc[1][0]
                            long = gloc[1][1]
                            self.count += 1
                            return lat, long
                        else:
                            self.count += 1
                            return None, None
                    except:
                        self.count += 1
                        return None, None
                        continue
            except:
                self.count += 1
                return None, None
                continue
            self.count += 1
            return row.latitude, row.longitude


geolocator = GoogleV3()
# geolocator = Nominatim()

# Read in xls as a dataframe
df = pd.read_excel('./GSAF5a.xls',encoding='utf-8')
# df = pd.read_excel('./GSAF5a.csv',encoding='utf-8')

# Clean our columns
df['Activity'] = df['Activity'].str.lower()
df['Activity'] = df['Activity'].str.replace('-','')
df['Species '] = df['Species '].str.lower()
df['Country'] = df['Country'].str.upper()

df.rename(columns={'Fatal (Y/N)': 'Fatal', 'Species ': 'Species', 'Sex ': 'Sex'}, inplace=True)

df.Fatal = df.Fatal.map(clean_Fatal)

# df.drop(['Case Number.1', 'original order', 'Unnamed: 21', 'Unnamed: 22','pdf', 'href formula', 'href'],inplace=True, axis=1)
df.drop(['Case Number.1', 'original order', 'Unnamed: 22','pdf', 'href formula', 'href'],inplace=True, axis=1)

df['year'] = df['Date'].map(year)
df['month'] = df['Date'].map(month)
df['day'] = df['Date'].map(day)

df.Activity.value_counts()

# People murdered (thrown overboard to sharks)
df[(df.Activity=='murder')][['Date', 'Country', 'Activity', 'Injury']]

df['Activity'] = df['Activity'].map(types)

# Unprovoked attacks in Australia, post 1900
df2 = df[(df.Country=='AUSTRALIA') & (df.year>1900) & (df.Type=='Unprovoked')]

gl = GeoLocation()

# df2 = df2[:10]

# Running the code below takes a while
df2['latitude'], df2['longitude'] = zip(*df2.apply(gl.get_location, axis=1))
df2.to_csv('./sharks_coords.csv',index=False)
