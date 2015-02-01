import xml.etree.cElementTree as ET
import re

OSMFILE = "miami_florida.osm"

def is_street_type(elem):
    return (elem.attrib['k'] == "addr:street")


def clean_streettypes(osmfile):
    cleaned = []
    osm_file = open(osmfile, "r")
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_type(tag):
                    if tag.attrib['v'].endswith("Ave") or tag.attrib['v'].endswith("Ave.") or tag.attrib['v'].endswith("ave"):
                        tag.attrib['v'] = re.sub("Ave.$|Ave$|ave$","Avenue",tag.attrib['v'])
                        cleaned.append(tag.attrib['v'])
                    elif tag.attrib['v'].endswith("BLVD") or tag.attrib['v'].endswith("Blvd.") or tag.attrib['v'].endswith("Blvd"):
                        tag.attrib['v'] = re.sub("Blvd.$|Blvd$|BLVD$","Boulevard",tag.attrib['v'])
                        cleaned.append(tag.attrib['v'])
                    elif tag.attrib['v'].endswith("Bnd"):
                        tag.attrib['v'] = re.sub("Bnd$","Bend",tag.attrib['v'])
                        cleaned.append(tag.attrib['v'])
                    elif tag.attrib['v'].endswith("Cir") or tag.attrib['v'].endswith("Cirlce"):
                        tag.attrib['v'] = re.sub("Cir$|Cirlce$","Circle",tag.attrib['v'])
                        cleaned.append(tag.attrib['v'])
                    elif tag.attrib['v'].endswith("Ct"):
                        tag.attrib['v'] = re.sub("Ct$","Court",tag.attrib['v'])
                        cleaned.append(tag.attrib['v'])
                    elif tag.attrib['v'].endswith("Cres"):
                        tag.attrib['v'] = re.sub("Cres$","Crescent",tag.attrib['v'])
                        cleaned.append(tag.attrib['v'])
                    elif tag.attrib['v'].endswith("Dr"):
                        tag.attrib['v'] = re.sub("Dr$","Drive",tag.attrib['v'])
                        cleaned.append(tag.attrib['v'])
                    elif tag.attrib['v'].endswith("Hwy") or tag.attrib['v'].endswith("HWY") or tag.attrib['v'].endswith("Hwy-1"):
                        tag.attrib['v'] = re.sub("Hwy-1$|Hwy$|HWY$","Highway",tag.attrib['v'])
                        cleaned.append(tag.attrib['v'])
                    elif tag.attrib['v'].endswith("Ln"):
                        tag.attrib['v'] = re.sub("Ln$","Lane",tag.attrib['v'])
                        cleaned.append(tag.attrib['v'])
                    elif tag.attrib['v'].endswith("Mnr"):
                        tag.attrib['v'] = re.sub("Mnr$","Manor",tag.attrib['v'])
                        cleaned.append(tag.attrib['v'])
                    elif tag.attrib['v'].endswith("Mnr"):
                        tag.attrib['v'] = re.sub("Mnr$","Manor",tag.attrib['v'])
                        cleaned.append(tag.attrib['v'])
                    elif tag.attrib['v'].endswith("Pkwy"):
                        tag.attrib['v'] = re.sub("Pkwy$","Parkway",tag.attrib['v'])
                        cleaned.append(tag.attrib['v'])
                    elif tag.attrib['v'].endswith("Pl"):
                        tag.attrib['v'] = re.sub("Pl$","Place",tag.attrib['v'])
                        cleaned.append(tag.attrib['v'])
                    elif tag.attrib['v'].endswith("Pt"):
                        tag.attrib['v'] = re.sub("Pt$","Point",tag.attrib['v'])
                        cleaned.append(tag.attrib['v'])
                    elif tag.attrib['v'].endswith("Rd") or tag.attrib['v'].endswith("RD") or tag.attrib['v'].endswith("Rd."):
                        tag.attrib['v'] = re.sub("Rd$|Rd.$|RD$","Road",tag.attrib['v'])
                        cleaned.append(tag.attrib['v'])
                    elif tag.attrib['v'].endswith("Sr"):
                        tag.attrib['v'] = re.sub("Sr$","State Road",tag.attrib['v'])
                        cleaned.append(tag.attrib['v'])
                    elif tag.attrib['v'].endswith("St") or tag.attrib['v'].endswith("ST") or tag.attrib['v'].endswith("St.") or tag.attrib['v'].endswith("st") or tag.attrib['v'].endswith("Ste") or tag.attrib['v'].endswith("street"):
                        tag.attrib['v'] = re.sub("St$|St.$|ST$|st$|street$|Ste$","Street",tag.attrib['v'])
                        cleaned.append(tag.attrib['v'])
                    elif tag.attrib['v'].endswith("Ter") or tag.attrib['v'].endswith("Terr") :
                        tag.attrib['v'] = re.sub("Ter$|Terr$","Terrace",tag.attrib['v'])
                        cleaned.append(tag.attrib['v'])
                    elif tag.attrib['v'].endswith("Trce"):
                        tag.attrib['v'] = re.sub("Trce$","Trace",tag.attrib['v']) 
                        cleaned.append(tag.attrib['v'])
                    elif tag.attrib['v'].endswith("Trl"):
                        tag.attrib['v'] = re.sub("Trl$","Trail",tag.attrib['v']) 
                        cleaned.append(tag.attrib['v'])
        elem.clear()               
    print cleaned
    
    
def test():
    clean_streettypes(OSMFILE)


if __name__ == '__main__':
    test()