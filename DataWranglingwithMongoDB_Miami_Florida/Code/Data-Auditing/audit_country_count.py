#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This code will iteratively parse through the file and check for the country name 
which is present in "tag" tags under node and way tags.

This is used for checking different ways in which the country name is mentioned.
"""

import xml.etree.cElementTree as ET
from collections import Counter

osm_file = open("miami_florida.osm", "r")

def print_sorted_dict(d):
    keys = d.keys()
    keys = sorted(keys, key=lambda s: s.lower())
    for k in keys:
        v = d[k]
        print "%s: %s" % (k, v) 

def is_country(elem):
    return elem.attrib['k'] == "addr:country"

def audit():
    country = []
    
    for event, elem in ET.iterparse(osm_file,events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tags in elem.iter("tag"):
                if is_country(tags):
                    country.append(tags.attrib['v'])  
        elem.clear()
    count = Counter(country)
    print_sorted_dict(dict(count)) 

if __name__ == '__main__':
    audit()