"""
This code will iteratively parse the file and 
find the country name entries which is not consistent and clean those 
to make them consistent and avoid multiple entries for the country.

Below are the problem with the country name entries handled and cleaned::
Majority of the country name entries are mentioned as USA but there are some which are mentioned as US
"""

import xml.etree.cElementTree as ET

OSMFILE = "miami_florida.osm"

def is_street_name(elem):
    return (elem.attrib['k'] == "addr:country")


def clean_country_name(osmfile):
    osm_file = open(osmfile, "r")
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    if tag.attrib['v'] != "USA":
                        tag.attrib['v'] = "USA"
        elem.clear()                    

def test():
    clean_country_name(OSMFILE)


if __name__ == '__main__':
    test()