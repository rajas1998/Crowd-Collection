import os

save_location =  "./" + "map.xml"

# lat_min, long_min, lat_max, long_max

# Ahmedabad bbox
# http://bboxfinder.com/#22.882650,72.3980260,23.300175,72.72085

# Delhi Bbox
# http://bboxfinder.com/#28.4564,76.992,28.7516,77.523

# Banglore Bbox
# http://bboxfinder.com/#12.803850,77.32806,13.125741,77.788101
blr_bbox = "12.803850,77.32806,13.125741,77.788101"
del_bbox = "28.4564,76.992,28.7516,77.523"
ahm_bbox = "22.882650,72.3980260,23.300175,72.72085"

query = "http://overpass-api.de/api/interpreter?data=[out:xml][timeout:86400][maxsize:1073741824];(node(" + del_bbox + ");<;);out meta;"

cmd_query = "wget -O " + save_location + " \"" + query + "\""

print(cmd_query)

# SG bbox - 1.213212,103.603821,1.472692,104.039154
# New york bbox - -74.25909008,40.47739894,-73.70018092,40.91617849
# Bengaluru bbox - 12.803850,77.32806,13.125741,77.788101
