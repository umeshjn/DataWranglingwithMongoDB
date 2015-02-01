#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This code will perform iterative parsing to process the map file and
audit the street types

This will fetch the set of entries for each street type.
"""

import xml.etree.cElementTree as ET
from collections import defaultdict
import re

#

osm_file = open("miami_florida.osm", "r")

street_type_re = re.compile(r'\S+\.?$', re.IGNORECASE)
street_types = defaultdict(set)

def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        street_types[street_type].add(street_name)

def print_sorted_dict(d):
    keys = d.keys()
    keys = sorted(keys, key=lambda s: s.lower())
    for k in keys:
        v = d[k]
        print "%s: %s" % (k, v) 

def is_street_name(elem):
    return elem.attrib['k'] == "addr:street"

def audit():
    for event, elem in ET.iterparse(osm_file,events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tags in elem.iter("tag"):
                if is_street_name(tags):
                    audit_street_type(street_types, tags.attrib['v'])   
        elem.clear()
    print_sorted_dict(street_types) 

if __name__ == '__main__':
    audit()