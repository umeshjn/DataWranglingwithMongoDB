#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This code will clean and structure the data so that 
it can be imported into MongoDB for further analysis.

In particular the following things will be done:
- process only 2 types of top level tags: "node" and "way"
- all attributes of "node" and "way" will be turned into regular key/value pairs, except:
    - attributes in the CREATED array will be added under a key "created"
    - attributes for latitude and longitude will be added to a "pos" array
- if second level tag "k" value contains problematic characters, it will be ignored
- if second level tag "k" value starts with "addr:", it will be added to a dictionary "address"
- if there is a second ":" that separates the type/direction of a street,
  the tag will be ignored, 
  
For example:

<tag k="addr:housenumber" v="5158"/>
<tag k="addr:street" v="North Lincoln Avenue"/>
<tag k="addr:street:name" v="Lincoln"/>
<tag k="addr:street:prefix" v="North"/>
<tag k="addr:street:type" v="Avenue"/>
<tag k="amenity" v="pharmacy"/>

will be turned into:

{...
"address": {
    "housenumber": 5158,
    "street": "North Lincoln Avenue"
}
"amenity": "pharmacy",
...
}

Here the problems with postcode, city, country, street type and state 
will be cleaned before loading the data into file.
"""
import xml.etree.cElementTree as ET
import re
import codecs
import json


lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]
position = ['lat','lon']


def is_street_type(elem):
    return (elem.attrib['k'] == "addr:street")


def clean_streettypes(tag):
        if tag.attrib['v'].endswith("Ave") or tag.attrib['v'].endswith("Ave.") or tag.attrib['v'].endswith("ave"):
            tag.attrib['v'] = re.sub("Ave.$|Ave$|ave$","Avenue",tag.attrib['v'])
        elif tag.attrib['v'].endswith("BLVD") or tag.attrib['v'].endswith("Blvd.") or tag.attrib['v'].endswith("Blvd"):
            tag.attrib['v'] = re.sub("Blvd.$|Blvd$|BLVD$","Boulevard",tag.attrib['v'])
        elif tag.attrib['v'].endswith("Bnd"):
            tag.attrib['v'] = re.sub("Bnd$","Bend",tag.attrib['v'])
        elif tag.attrib['v'].endswith("Cir") or tag.attrib['v'].endswith("Cirlce"):
            tag.attrib['v'] = re.sub("Cir$|Cirlce$","Circle",tag.attrib['v'])
        elif tag.attrib['v'].endswith("Ct"):
            tag.attrib['v'] = re.sub("Ct$","Court",tag.attrib['v'])
        elif tag.attrib['v'].endswith("Cres"):
            tag.attrib['v'] = re.sub("Cres$","Crescent",tag.attrib['v'])
        elif tag.attrib['v'].endswith("Dr"):
            tag.attrib['v'] = re.sub("Dr$","Drive",tag.attrib['v'])
        elif tag.attrib['v'].endswith("Hwy") or tag.attrib['v'].endswith("HWY") or tag.attrib['v'].endswith("Hwy-1"):
            tag.attrib['v'] = re.sub("Hwy-1$|Hwy$|HWY$","Highway",tag.attrib['v'])
        elif tag.attrib['v'].endswith("Ln"):
            tag.attrib['v'] = re.sub("Ln$","Lane",tag.attrib['v'])
        elif tag.attrib['v'].endswith("Mnr"):
            tag.attrib['v'] = re.sub("Mnr$","Manor",tag.attrib['v'])
        elif tag.attrib['v'].endswith("Mnr"):
            tag.attrib['v'] = re.sub("Mnr$","Manor",tag.attrib['v'])
        elif tag.attrib['v'].endswith("Pkwy"):
            tag.attrib['v'] = re.sub("Pkwy$","Parkway",tag.attrib['v'])
        elif tag.attrib['v'].endswith("Pl"):
            tag.attrib['v'] = re.sub("Pl$","Place",tag.attrib['v'])
        elif tag.attrib['v'].endswith("Pt"):
            tag.attrib['v'] = re.sub("Pt$","Point",tag.attrib['v'])
        elif tag.attrib['v'].endswith("Rd") or tag.attrib['v'].endswith("RD") or tag.attrib['v'].endswith("Rd."):
            tag.attrib['v'] = re.sub("Rd$|Rd.$|RD$","Road",tag.attrib['v'])
        elif tag.attrib['v'].endswith("Sr"):
            tag.attrib['v'] = re.sub("Sr$","State Road",tag.attrib['v'])
        elif tag.attrib['v'].endswith("St") or tag.attrib['v'].endswith("ST") or tag.attrib['v'].endswith("St.") or tag.attrib['v'].endswith("st") or tag.attrib['v'].endswith("Ste") or tag.attrib['v'].endswith("street"):
            tag.attrib['v'] = re.sub("St$|St.$|ST$|st$|street$|Ste$","Street",tag.attrib['v'])
        elif tag.attrib['v'].endswith("Ter") or tag.attrib['v'].endswith("Terr") :
            tag.attrib['v'] = re.sub("Ter$|Terr$","Terrace",tag.attrib['v'])
        elif tag.attrib['v'].endswith("Trce"):
            tag.attrib['v'] = re.sub("Trce$","Trace",tag.attrib['v']) 
        elif tag.attrib['v'].endswith("Trl"):
            tag.attrib['v'] = re.sub("Trl$","Trail",tag.attrib['v']) 
               
        return tag.attrib['v']
         
         

def is_state_name(elem):
    return (elem.attrib['k'] == "addr:state")
    
    
def clean_state_name(tag):
    if tag.attrib['v'] != "FL":
          tag.attrib['v'] = "FL"
    return tag.attrib['v'] 
    
    
def is_country_name(elem):
    return (elem.attrib['k'] == "addr:country")


def clean_country_name(tag):
      if tag.attrib['v'] != "USA":
         tag.attrib['v'] = "USA"
      return tag.attrib['v']

def is_postalcode(elem):
    return (elem.attrib['k'] == "addr:postcode")


def clean_postalcode(tag):
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
        
    return tag.attrib['v']


def is_city_name(elem):
    return (elem.attrib['k'] == "addr:city")


def clean_city_names(tag):
    if tag.attrib['v'] == "boca raton" or tag.attrib['v'].find("Boca Raton") !=-1:
        tag.attrib['v'] = "Boca Raton"        
    elif tag.attrib['v']== "delray beach":
        tag.attrib['v'] = "Delray Beach"
    elif tag.attrib['v'] == "Fort lauderdale" or tag.attrib['v'] == "Ft Lauderdale":
        tag.attrib['v'] = "Fort Lauderdale"
    elif tag.attrib['v'] == "miami" or tag.attrib['v'] == "Miami, FL" or tag.attrib['v'] == "Miami, Florida":
        tag.attrib['v'] = "Miami"
    elif tag.attrib['v'] == "miami beach":
        tag.attrib['v'] = "Miami Beach"
    elif tag.attrib['v'] == "miami Shores":
        tag.attrib['v'] = "Miami Shores"
    elif tag.attrib['v'] == "sunny Isles Beach":
        tag.attrib['v'] = "Sunny Isles Beach"
    elif tag.attrib['v'] == "sunrise":
        tag.attrib['v'] = "Sunrise"
   
    return tag.attrib['v']
    
    
    
def shape_element(element):
    node = {}
    refs = []
    created = {}
    address = {}
    pos = {}
    if element.tag == "node" or element.tag == "way" :
        for key in element.attrib.keys():
                if key in CREATED:          
                   created[key] = element.attrib[key]
                elif key in position:                
                   pos[key]=(float(element.attrib[key]))                    
                else:
                   node[key] = element.attrib[key]
        node['created'] = created
        node['type'] = element.tag
        if len(pos)==2:
            node['pos']=[pos['lat'],pos['lon']]

        for elem_nd in element.iter("nd"):
                refs.append(elem_nd.attrib['ref'])
        if(len(refs)>0):
            node['node_refs']=refs       
            
        for tags in element.iter("tag"):
                if tags.attrib['k'].find('addr') != -1 and tags.attrib['k'].find(':') != -1 and len(tags.attrib['k'].split(':')) == 2:
                    if is_street_type(tags):
                        address[tags.attrib['k'].split(':')[1]]  = clean_streettypes(tags)
                    elif is_state_name(tags):
                        address[tags.attrib['k'].split(':')[1]]  = clean_state_name(tags)
                    elif is_country_name(tags):
                        address[tags.attrib['k'].split(':')[1]]  = clean_country_name(tags)
                    elif is_postalcode(tags):
                        address[tags.attrib['k'].split(':')[1]]  = clean_postalcode(tags)
                    elif is_city_name(tags):
                        address[tags.attrib['k'].split(':')[1]]  = clean_city_names(tags)
                    else:
                        address[tags.attrib['k'].split(':')[1]] = tags.attrib['v']
                elif problemchars.search(tags.attrib['k']) == None and tags.attrib['k'].find('tiger') == -1:
                     node[tags.attrib['k']] = tags.attrib['v']
        if address:             
            node['address'] = address
            
    return node  
    

def process_map(file_in, pretty = False):
    file_out = "miami_florida.json".format(file_in)
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in,events=('start',)):
            el = shape_element(element)  
            element.clear()
            if el:
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")

def test():
    process_map('miami_florida.osm', False)    

if __name__ == "__main__":
    test()