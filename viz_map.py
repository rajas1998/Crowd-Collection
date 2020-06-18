import pickle
import numpy as np
import os
import matplotlib.pyplot as plt
import pandas as pd
from newsim import *
from geopy.distance import geodesic
from tqdm import tqdm

# This file generates all the csv file which is fed to tableau to generate the necessary plots
# It takes in the predicted abnormal nodes, clusters them and then shows the abnormal nodes in the highest cluster
# The csv file has the columns ["Lat", "Long", "Time", "Epicenter", "This_time", "Confidence"]
# The lat and long are those of the abormal node
# There is one datapoint for each time step
# The epicenter cilumn is 1 if the corresponding node is the epicenter and 0 otherwise
# The confidence is the confidence score related to the node being the epicenter
# This file assumes that we know where the epicenter is (It has been saved in the file name)

G, _ = make_graph()
d = pickle.load(open("dataset/1/predicted_abnormal_for_abnormal_new_3", "rb"))
nodes = {}
for index,row in pd.read_csv("data/nodes_1_8.csv").iterrows():
	nodes[int(row["ID"])] = (row["Lat"], row["Long"])

def cluster(l, cutoff_path_length):
	n = len(l)
	e = {i:[] for i in l}
	for i in range(n):
		for j in range(i+1,n):
			path = shortest_path(G,l[i],l[j])
			if (len(path) - 1 <= cutoff_path_length):
				e[l[i]].append(l[j])
				e[l[j]].append(l[i])
	vis = {i: False for i in l}
	components = []
	for vert in l:
		if (not vis[vert]):
			component = []
			q = [vert]
			vis[vert] = True
			while len(q) > 0:
				u = q.pop(0)
				assert u not in component
				component.append(u)
				for v in e[u]:
					if (not vis[v]):
						vis[v] = True
						q.append(v)
			components.append(component)
	return components

TIME_AFTER = 75
CUTOFF_PATH_LENGTH = 3
x = {}
for file in d:
	if '0.01' in file:
		location_people,s1,e1 = pickle.load(open("dataset/1/abnormal_new/" + file, "rb"))
		time_collect = int(file.split("_")[3])
		epicenter = int(file.split("_")[-2])
		abnormal_nodes_list = d[file]
		if time_collect != 510:
			continue
		print ("Time collect is", time_collect)
		l = []
		all_nodes = {}
		for time_after in tqdm(range(0,TIME_AFTER)):
			abnormal_nodes = list(abnormal_nodes_list[time_collect - s1 - 1 + time_after])
			# for i in abnormal_nodes:
			# 	if i == epicenter:
			# 		continue
			# 	l.append((nodes[i][0], nodes[i][1], time_after, 0))
			components = cluster(abnormal_nodes,CUTOFF_PATH_LENGTH)
			components.sort(key = len, reverse = True)
			# lats = longs = 0
			for i in components[0]:
				if i in all_nodes:
					all_nodes[i] += 6
				else:
					all_nodes[i] = 6
			for i in all_nodes:
				all_nodes[i] -= 1
			all_nodes = {k:v for (k,v) in all_nodes.items() if v > 0}
			tot_sum = sum(all_nodes.values())
			for i in components[0]:
				# lats += nodes[i][0]
				# longs += nodes[i][1]
				if i == epicenter:
					continue
				l.append((nodes[i][0], nodes[i][1], time_after, 0, 1, float(all_nodes[i])/tot_sum))
			for i in all_nodes:
				if i not in components[0]:
					l.append((nodes[i][0], nodes[i][1], time_after,0,0,float(all_nodes[i])/tot_sum))
			# lats /= len(components[0]); longs /= len(components[0])
			# l.append((lats, longs, time_after, 1))
			l.append((nodes[epicenter][0], nodes[epicenter][1], time_after, 1,1,1))
		df = pd.DataFrame(l, columns=["Lat", "Long", "Time", "Epicenter", "This_time", "Confidence"])
		df.to_csv("confidence_plots/" + file[:-10] + ".csv", index=False)
		# df.to_csv("test.csv", index=False)

