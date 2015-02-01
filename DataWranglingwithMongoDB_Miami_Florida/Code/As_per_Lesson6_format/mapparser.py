#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This code will perform iterative parsing to process the map file and
find out not only what tags are there, but also how many, to get the
feeling on how much of which data you can expect to have in the map.
The output will be a dictionary with the tag name as the key
and number of times this tag can be encountered in the map as value.

"""
import xml.etree.cElementTree as ET
import pprint
from collections import Counter

def count_tags(filename):
        tags = []
        for event,elem in ET.iterparse(filename):
            tags.append(elem.tag)
            elem.clear()
        count = Counter(tags)
        return dict(count)

def test():
    tags = count_tags('miami_florida.osm')
    pprint.pprint(tags)
    

if __name__ == "__main__":
    test()