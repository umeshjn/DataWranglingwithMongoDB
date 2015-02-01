"""
This code will iteratively parse the file and clean the State name entries for maintaining the consistency in the state name entries throughout.

Below are the problems with state name handled::
There are few entries for State name which are mentioned as Fl or Florida while the maximum number of entires are FL
Also there are couple of entries where the place names are mentioned as the state name.

Example:
Inverrary Boulevard and West Oakland Park Boulevard

"""
import xml.etree.cElementTree as ET

OSMFILE = "miami_florida.osm"

def is_street_name(elem):
    return (elem.attrib['k'] == "addr:state")


def clean_state_name(osmfile):
    osm_file = open(osmfile, "r")
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    if tag.attrib['v'] != "FL":
                        tag.attrib['v'] = "FL"
        elem.clear()                    

def test():
    clean_state_name(OSMFILE)



if __name__ == '__main__':
    test()