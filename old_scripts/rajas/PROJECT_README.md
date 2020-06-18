# Environment 

Preprocessing scripts are written in Python3(Tested on Python 3.6.9)
Algorithm/Simulation codebase is in C++11 (Tested on GCC 7.4.0)

Create environment venv :
	conda env create -f environment.yml

# Data Preparation


## Getting Map
Use scripts/get_osm_map.py to download a OSM using a given bounding box. It creates a commandline query to dowload the map.
The bounding box can be found by experimenting with zones and orders. Use scripts/get_bounding_box.ipynb and http://bboxfinder.com/ for the same
Current Location : data_BLR/map/map.xml

## Generating nodes and segments
Use scripts/map_extract/finalParseBound.jl to extract nodes and edges from the OSM XML format map. It creates two files - nodes and segments

Current Location : data_BLR/map/nodes.csv data_BLR/map/segments.csv

It requires installation of Julia 0.3 with OpenStreetMap.jl extension - https://github.com/tedsteiner/OpenStreetMap.jl
A new version package is available for Julia 1.0 at https://github.com/pszufe/OpenStreetMapX.jl it may be used.

## Modifying nodes and segments file
The format of above generated files is modified using simple find/replace as :

nodes.csv :
1522655984,LLA(12.9674517,77.5624332,0.0)
1588453609,LLA(12.8820959,77.4928339,0.0)
2450408122,LLA(13.0411969,77.5809113,0.0)
.
.

nodes_mod.csv :
id,lat,lon,al
1522655984,12.9674517,77.5624332,0.0
1588453609,12.8820959,77.4928339,0.0
2450408122,13.0411969,77.5809113,0.0
.
.

segments.csv :
Segment(419638272,599212733,[419638272,599212733],70.86635228852029,6,46951459,true)
Segment(599212733,419638272,[599212733,419638272],70.86635228852029,6,46951459,true)
Segment(599212733,599212731,[599212733,599212731],53.45547791675319,6,46951459,true)
.
.

segments_mod.csv :
u,v,list,dist,int,pid,oneway
419638272,599212733,"[419638272,599212733]",70.86635228852029,6,46951459,true
599212733,419638272,"[599212733,419638272]",70.86635228852029,6,46951459,true
599212733,599212731,"[599212733,599212731]",53.45547791675319,6,46951459,true
.
.

Current Location : data_BLR/map/nodes_mod.csv data_BLR/map/segments_mod.csv

## Modifying Map
The julia script extracts roads compatible for vehicles and marks intersection of these roads as nodes of a map.
We need to modify our map according to these nodes and edges for further applications.
Use scripts/modify_map.py for the purpose.

Current Location : data_BLR/map/map_mod.xml

## Map Connectivity
The OSM map obtained may not be strongly connected. 
scripts/get_connected_map.py extracts the largest strongly connected component of the graph
Use the connected version if required.

Current Location : data_BLR/map/nodes_mod_connected.csv data_BLR/map/segments_mod_connected.csv
