#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This code will iteratively parse through the file and check for the city name 
which is present in "tag" tags under node and way tags.

This is used for checking different ways in which the each city name is mentioned. 
"""

import xml.etree.cElementTree as ET
from collections import Counter

osm_file = open("miami_florida.osm", "r")

def print_sorted_dict(d):
    keys = d.keys()
    keys = sorted(keys, key=lambda s: s.lower())
    for k in keys:
        v = d[k]
        print "%s: %d" % (k, v) 

def is_city(elem):
    return elem.attrib['k'] == "addr:city"

def audit():
    city = []
    
    for event, elem in ET.iterparse(osm_file,events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tags in elem.iter("tag"):
                if is_city(tags):
                    city.append(tags.attrib['v'])  
        elem.clear()
    count = Counter(city)
    print_sorted_dict(dict(count)) 

if __name__ == '__main__':
    audit()