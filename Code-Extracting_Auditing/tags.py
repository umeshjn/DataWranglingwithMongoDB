#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import pprint
import re
"""
This code will check the "k" value for each "<tag>" and see if they can be valid keys in MongoDB,
as well as see if there are any other potential problems.
"""


lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')


def key_type(element, keys):
    if element.tag == "tag":
        if lower.search(element.attrib['k']) != None:
            keys['lower'] += 1
#            print element.attrib
        elif lower_colon.search(element.attrib['k']) != None:
            keys['lower_colon'] += 1
        elif problemchars.search(element.attrib['k']) != None:
            keys['problemchars'] += 1
            print element.attrib
        else:
            keys['other'] += 1
            
        
    return keys



def process_map(filename):
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    for _, element in ET.iterparse(filename,events=("start",)):
        keys = key_type(element, keys)
        element.clear()
    return keys



def test():
    keys = process_map('miami_florida.osm')
    pprint.pprint(keys)


if __name__ == "__main__":
    test()