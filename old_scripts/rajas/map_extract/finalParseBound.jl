using OpenStreetMap

############################################### Change This Only ###########################################
#output file for storing nodes
outfile1 = open("nodes.csv", "w")
#output file for storing segments
outfile2 = open("segments.csv", "w")

#Pass osm file
nodesLLA, highways, buildings, features = getOSMData("map.xml")

#Bounding box - lat/lon 
#boundsLLA = Bounds(1.2,1.5,103.6,104.04)
# boundsLLA = Bounds(12.803850,13.1257,77.32806,77.788101)
boundsLLA = Bounds(26.0705,91.5363,26.2099,91.8426)
###########################################################################################################

println("Number of nodes: $(length(nodesLLA))")
println("Number of highways: $(length(highways))")
#boundsLLA = getBounds(parseMapXML("/local/nandini/nandini/taxi_project/map/NY.osm"))
println(boundsLLA)

# Convert to ENU coordinates
lla_reference = center(boundsLLA) # Manual reference point for coordinate transform (optional)
nodes = ENU( nodesLLA, lla_reference )
bounds = ENU( boundsLLA, lla_reference )


# Crop map to bounds
cropMap!(nodes, bounds, highways=highways, buildings=buildings, features=features, delete_nodes=false)


# Extract highway classes (note that OpenStreetMap calls all paths “highways”
roads = roadways(highways)
intersections = findIntersections(highways)
nodeids=keys(intersections)


for j in nodeids
	if(j in keys(nodesLLA))
  		write(outfile1, join((j,nodesLLA[j]), ","), "\n") 
 	end
end
close(outfile1)






#println(nodes)

# Segment only specific levels of roadways
# (e.g., freeways through residential streets, levels 1-6)
segments = segmentHighways(nodes, highways, intersections, roads, Set(1:6))
println("Number of segments: $(length(segments))")
for i = 1:length(segments)
	show(outfile2,segments[i])
	print(outfile2,"\n")
end
close(outfile2)
println("yahoo")


