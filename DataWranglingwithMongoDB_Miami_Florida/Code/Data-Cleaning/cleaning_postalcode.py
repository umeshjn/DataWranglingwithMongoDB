"""
This code will iteratively parse the file and 
find the postcodes which are not not clean and clean those.

Below are the problems with the postal code which are handled through this code in order to clean them:

There are postal codes which are equal to zero.
One postal code has state name as its value.
One entry has a house number being mentioned as postal code. 
There are postal codes which are having suffix of FL/Fl/FL-
Example:
FL 33016
FL 33026
FL 33033
FL 33126
"""


import xml.etree.cElementTree as ET

OSMFILE = "miami_florida.osm"

def is_street_name(elem):
    return (elem.attrib['k'] == "addr:postcode")


def clean_postalcode(osmfile):
    osm_file = open(osmfile, "r")
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    if tag.attrib['v'] == "0":
                        tag.attrib['v'] = "33326"
                    elif tag.attrib['v'].find("FL ")==-1 and tag.attrib['v'].find("-") !=-1:
                        tag.attrib['v'] = tag.attrib['v'].split('-')[0]
                    elif tag.attrib['v'].find("FL ")!=-1:
                        tag.attrib['v'] = tag.attrib['v'].replace("FL","").strip().split('-')[0]
                    elif tag.attrib['v'].find("FL-")!=-1:
                        tag.attrib['v'] = tag.attrib['v'].replace("FL-","")
                    elif tag.attrib['v'] == 'FL':
                        tag.attrib['v'] = "33185"
                    elif tag.attrib['v'].find("FL")!=-1:
                        tag.attrib['v'] = tag.attrib['v'].replace("FL","")
        elem.clear()                    

def test():
    clean_postalcode(OSMFILE)


if __name__ == '__main__':
    test()