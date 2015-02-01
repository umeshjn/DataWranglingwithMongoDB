#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import json


lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]
position = ['lat','lon']


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
                     address[tags.attrib['k'].split(':')[1]] = tags.attrib['v']
                elif problemchars.search(tags.attrib['k']) == None :
                     node[tags.attrib['k']] = tags.attrib['v']
        if address:             
            node['address'] = address
            
    return node  
    

def process_map(file_in, pretty = False):
    file_out = "miami_with_tiger.json".format(file_in)
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