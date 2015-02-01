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