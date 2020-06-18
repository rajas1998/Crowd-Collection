import os
from tqdm import tqdm
import pickle
from newsim import make_graph
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from newsim import *
from geopy.distance import geodesic

def save_mean_and_std():
	# Saving mean and standard deviation
	files = os.listdir("dataset/1/normal")
	G, nodes = make_graph()
	d = {i:{} for i in nodes}
	for file in tqdm(files):
		location_people,_,s1,e1,_,_ = pickle.load(open("dataset/1/normal/" + file,"rb"))
		for time in range(s1,e1):	
			for i in nodes:
				if time not in d[i]:
					d[i][time] = []
				if i in location_people[time-s1]:
					d[i][time].append(location_people[time-s1][i])
				else:
					d[i][time].append(0)
	for i in d:
		for j in d[i]:
			d[i][j] = (np.mean(d[i][j]), np.std(d[i][j]))
	pickle.dump(d, open("dataset/1/normal_means_and_std.pkl", "wb"))

def predict_abnormal_nodes():
	# Finding abnormal nodes
	G, nodes = make_graph()
	CONFIDENCE = 2
	d = pickle.load(open("dataset/1/normal_means_and_std.pkl"))
	for folder in ["normal", "abnormal"]:
		x = {}
		files = os.listdir("dataset/1/" + folder)
		for file in tqdm(files):
			location_people,_,s1,e1,_,_ = pickle.load(open("dataset/1/" + folder + "/" + file,"rb"))
			abnormal_nodes = []
			for time in range(s1,e1):
				for i in nodes:
					people_here = location_people[time-s1][i] if i in location_people[time-s1] else 0
					if (people_here - d[i][time][0] > CONFIDENCE*d[i][time][1]):
						abnormal_nodes.append(i)
			x[file] = abnormal_nodes
			print (len(abnormal_nodes))
		pickle.dump(abnormal_nodes, open("dataset/1/predicted_abnormal_for_"+folder, "wb"))

def cluster(l, cutoff_path_length):
	# Cluster the abnormal nodes according to how close they are
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

def predict_epicenter():
	# Predicting the location of the epicenter
	# This is done by first clustering the abnormal nodes according to their edge distance
	# Then the cluster with highest number of abnormal nodes is selected
	# The predicted epicenter is the average latitude and longitude value of the abnormal nodes in this cluster
	G, _ = make_graph()
	d = pickle.load(open("dataset/1/predicted_abnormal_for_abnormal_3_20", "rb"))
	nodes = {}
	for index,row in pd.read_csv("data/nodes_1_8.csv").iterrows():
		nodes[int(row["ID"])] = (row["Lat"], row["Long"])
	TIME_AFTER = 75
	CUTOFF_PATH_LENGTH = 3
	x = {}
	for file in d:
		if '0.01' in file:
			location_people,s1,e1 = pickle.load(open("dataset/1/abnormal/" + file, "rb"))
			time_collect = int(file.split("_")[3])
			epicenter = int(file.split("_")[-2])
			abnormal_nodes_list = d[file]
			# if time_collect == 540:
			# 	continue
			print ("Time collect is", time_collect)
			ranks = []
			dist_of_pred = []
			dist_of_cluster = []
			time_27 = -1
			time_30 = -1
			for time_after in range(0,TIME_AFTER):
				abnormal_nodes = list(abnormal_nodes_list[time_collect - s1 - 1 + time_after])
				if (len(abnormal_nodes) > 0):
					if (time_27 == -1 and len(abnormal_nodes) > 27):
						time_27 = time_after
					if (time_30 == -1 and len(abnormal_nodes) > 30):
						time_30 = time_after
					if (not os.path.exists("viz_new/"+str(epicenter)+"_"+str(time_collect) + "/")):
						os.makedirs("viz_new/"+str(epicenter)+"_"+str(time_collect) + "/")

			# 		### If you want to cluster the nodes
					components = cluster(abnormal_nodes,CUTOFF_PATH_LENGTH)
					c_len = -1
					for i in components:
						if epicenter in i:
							c_len = len(i)
							break
					comp_lens = sorted([len(i) for i in components], reverse=True)
					comp_rank = comp_lens.index(c_len) + 1 if c_len != -1 else len(comp_lens)
					ranks.append(comp_rank)
					lats = longs = 0
					components.sort(key = len, reverse = True)
					for i in components[0]:
						lats += nodes[i][0]
						longs += nodes[i][1]
					lats /= len(components[0])
					longs /= len(components[0])
					temp_d1 = geodesic((lats,longs), nodes[epicenter]).m
					dist_of_pred.append(temp_d1)
					lats = longs = 0
					ind = 0
					for i in range(len(components)):
						if epicenter in components[i]:
							ind = i
							break
					for i in components[ind]:
						lats += nodes[i][0]
						longs += nodes[i][1]
					lats /= len(components[ind])
					longs /= len(components[ind])
					temp_d2 = geodesic((lats,longs), nodes[epicenter]).m
					dist_of_cluster.append(temp_d2)
					print (comp_lens[:5], c_len, sum(comp_lens), comp_rank, temp_d1, temp_d2)
			x[file] = (dist_of_pred,ranks,time_27, time_30)

	pickle.dump(x, open("dists.pkl", "wb"))