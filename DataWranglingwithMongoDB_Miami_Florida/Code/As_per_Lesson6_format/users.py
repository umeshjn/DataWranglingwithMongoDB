#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET

"""
This code will find out how many unique users 
have contributed to the map in this particular area.
The function process_map will return a set of unique user IDs ("uid").
"""

def get_user(element):
    if element.tag == "node" or element.tag == "relation" or element.tag == "way":
        if element.get('uid'):
            return element.attrib['uid']



def process_map(filename):
    users = set()
    for _, element in ET.iterparse(filename):
            users.add(get_user(element))   
            element.clear()
    return users


def test():
    users = process_map('miami_florida.osm')
    print "Unique users :::",users
    print "Number of unique users :::",len(users)


if __name__ == "__main__":
    test()