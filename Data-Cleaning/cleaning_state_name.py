"""
Your task in this exercise has two steps:

- audit the OSMFILE and change the variable 'mapping' to reflect the changes needed to fix 
    the unexpected street types to the appropriate ones in the expected list.
    You have to add mappings only for the actual problems you find in this OSMFILE,
    not a generalized solution, since that may and will depend on the particular area you are auditing.
- write the update_name function, to actually fix the street name.
    The function takes a string with street name as an argument and should return the fixed name
    We have provided a simple test so that you see what exactly is expected
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
                        print tag.attrib['v']
        elem.clear()                    

def test():
    clean_state_name(OSMFILE)



if __name__ == '__main__':
    test()