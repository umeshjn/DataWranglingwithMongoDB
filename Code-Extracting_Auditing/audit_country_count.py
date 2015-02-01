#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This code will read through the input file and check for the state names 
which are present in "tag" tags which are under node and way tags.

This basically counts the number of times it appears.

This is used for checking different ways in which the country is mentioned 
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

def is_street_name(elem):
    return elem.attrib['k'] == "addr:country"

def audit():
    street_types = []
    
    for event, elem in ET.iterparse(osm_file,events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tags in elem.iter("tag"):
                if is_street_name(tags):
                    street_types.append(tags.attrib['v'])  
        elem.clear()
    count = Counter(street_types)
    print_sorted_dict(dict(count)) 

if __name__ == '__main__':
    audit()