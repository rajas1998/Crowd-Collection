f = open("map_data/segments_1_8.csv", "r")
o = open("data/segments_1_8.csv", "w")
data = []
for i in f.readlines():
	l = i.split(",")
	u = int(l[0][8:])
	v = int(l[1])
	dist = float(l[-4])
	data.append((u,v,dist))
for i in data:
	o.write(",".join(map(str,list(i))) + "\n")
o.close()