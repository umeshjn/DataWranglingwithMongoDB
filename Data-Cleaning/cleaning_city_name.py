import xml.etree.cElementTree as ET

OSMFILE = "miami_florida.osm"

def is_city_name(elem):
    return (elem.attrib['k'] == "addr:city")


def clean_city_names(osmfile):
    cleaned = []
    osm_file = open(osmfile, "r")
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_city_name(tag):
                    if tag.attrib['v'] == "boca raton" or tag.attrib['v'].find("Boca Raton") !=-1:
                        tag.attrib['v'] = "Boca Raton"
                        cleaned.append(tag.attrib['v'])
                    elif tag.attrib['v']== "delray beach":
                        tag.attrib['v'] = "Delray Beach"
                        cleaned.append(tag.attrib['v'])
                    elif tag.attrib['v'] == "Fort lauderdale" or tag.attrib['v'] == "Ft Lauderdale":
                        tag.attrib['v'] = "Fort Lauderdale"
                        cleaned.append(tag.attrib['v'])
                    elif tag.attrib['v'] == "miami" or tag.attrib['v'] == "Miami, FL" or tag.attrib['v'] == "Miami, Florida":
                        tag.attrib['v'] = "Miami"
                        cleaned.append(tag.attrib['v'])
                    elif tag.attrib['v'] == "miami beach":
                        tag.attrib['v'] = "Miami Beach"
                        cleaned.append(tag.attrib['v'])
                    elif tag.attrib['v'] == "miami Shores":
                        tag.attrib['v'] = "Miami Shores"
                        cleaned.append(tag.attrib['v'])
                    elif tag.attrib['v'] == "sunny Isles Beach":
                        tag.attrib['v'] = "Sunny Isles Beach"
                        cleaned.append(tag.attrib['v'])
                    elif tag.attrib['v'] == "sunrise":
                        tag.attrib['v'] = "Sunrise"
                        cleaned.append(tag.attrib['v'])
        elem.clear()  
    print cleaned                  

def test():
    clean_city_names(OSMFILE)


if __name__ == '__main__':
    test()