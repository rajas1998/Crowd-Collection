#!/usr/bin/env python
# coding: utf-8

#Imports
import numpy as np
import pandas as pd
from tqdm.auto import tqdm

import xml.etree.ElementTree as ET

import warnings
warnings.filterwarnings("ignore")
############################################### Change This Only ###########################################
# Miscellaneous
base_dir = "/media/root/data/swiggy/"
data_dir = base_dir + "data_DEL/"

map_dir = data_dir + "map/"
## Input Map
map_file = data_dir + "map/map.xml"
## Output Map
mod_map_file = data_dir + "map/map_mod.xml"

# Read Data
blr_nodes = pd.read_csv(map_dir + "nodes_mod.csv") 
blr_edges = pd.read_csv(map_dir + "segments_mod.csv") 

##########################################################################################################

print("Invalid u Nodes in Edges = %d" %np.sum(~blr_edges.v.isin(blr_nodes.id)))
print("Invalid v Nodes in Edges = %d" %np.sum(~blr_edges.u.isin(blr_nodes.id)))

# Read Original Map
tree = ET.parse(map_file) 

# Modify Map
root = tree.getroot() 
ways = root.findall('way')

new_root = ET.Element(root.tag, root.attrib)
new_root.extend(root.findall('note'))
new_root.extend(root.findall('meta'))

all_node_elems=[]
for row in tqdm(blr_nodes.itertuples(), total=len(blr_nodes)):
    elem = ET.Element('node', {'id':str(row.id), 'lat':str(row.lat), 'lon':str(row.lon)})
    elem.tail='\n  '
    all_node_elems.append(elem)

new_root.extend(all_node_elems)

######### Note the oneway tag is true for all segments, therefore it was not required to handle it. 
all_way_elems=[]
for row in tqdm(blr_edges.itertuples(), total=len(blr_edges)): 
    way_elem = ET.Element("way", {'id':str(row.Index)})
    
    u_elem = ET.Element("nd", {'ref': str(row.u)})
    u_elem.tail = '\n    '
    v_elem = ET.Element("nd", {'ref': str(row.v)})
    v_elem.tail = '\n    '
    
    nd_elems = [u_elem, v_elem]
    
    t1_elem = ET.Element("tag", {'k': 'highway', 'v':'primary'})
    t1_elem.tail = '\n    '
    t2_elem = ET.Element("tag", {'k': 'oneway', 'v':'yes'})
    t2_elem.tail = '\n  '
    
    nd_elems.extend([t1_elem, t2_elem])
    
    way_elem.extend(nd_elems)
    way_elem.text = '\n    '
    way_elem.tail = '\n  '
    
    all_way_elems.append(way_elem)

new_root.extend(all_way_elems)
new_tree = ET.ElementTree(new_root)

# Save File
new_tree.write(mod_map_file, encoding="UTF-8")

with open(mod_map_file, 'r') as myf:
    data = myf.read()

data = '<?xml version="1.0" encoding="UTF-8"?>\n' + data 

with open(mod_map_file, 'w') as myf:
    myf.write(data)

print("Map Modified")
