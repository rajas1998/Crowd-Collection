# import networkx as nx
# import matplotlib.pyplot as plt
# import pickle
# from newsim import *
# fig, ax = plt.subplots()
# G, nodes = make_graph()
# a,b,c = pickle.load(open("dataset/1/abnormal_go_0.01_600_4972481337_7927.datapoint", "rb"))
# # print (b,c) #394 816
# # 4972482832
# epicenter=4972481337
# l = []
# for i in range(206, len(a)):
# 	l.append(a[i][epicenter])
# # plt.plot(l,color = "red")
# d = nx.single_source_shortest_path_length(G, epicenter, cutoff = 5)
# onehop = []
# twohop = []
# threehop = []
# fourhop = []
# fivehop = []
# for i in d:
# 	if d[i] == 1:
# 		onehop.append(i)
# 	elif d[i] == 2:
# 		twohop.append(i)
# 	elif d[i] == 3:
# 		threehop.append(i)
# 	elif d[i] == 4:
# 		fourhop.append(i)
# 	elif d[i] == 5:
# 		fivehop.append(i)
# # l = []
# # for i in range(206, len(a)):
# # 	people_mean = 0
# # 	for j in onehop:
# # 		people_mean += a[i][j]
# # 	people_mean /= len(onehop)
# # 	l.append(people_mean)
# # plt.plot(l,color = "blue", label="Mean at one hop")
# # l = []
# # for i in range(206, len(a)):
# # 	people_mean = 0
# # 	for j in twohop:
# # 		people_mean += a[i][j]
# # 	people_mean /= len(twohop)
# # 	l.append(people_mean)
# # print (len(onehop), len(twohop))
# # plt.plot(l,color = "green", label="Mean at two hop")
# l = []
# for i in range(206, len(a)):
# 	people_mean = 0
# 	for j in twohop:
# 		people_mean = max(people_mean, a[i][j])
# 	# people_mean /= len(twohop)
# 	l.append(people_mean)
# print (len(onehop), len(twohop))
# plt.plot(l,color = "orange", label="Max at two hop")
# l = []
# for i in range(206, len(a)):
# 	people_mean = 0
# 	for j in threehop:
# 		people_mean = max(people_mean, a[i][j])
# 	# people_mean /= len(threehop)
# 	l.append(people_mean)
# print (len(onehop), len(threehop))
# plt.plot(l,color = "red", label="Max at three hop")
# l = []
# for i in range(206, len(a)):
# 	people_mean = 0
# 	for j in fourhop:
# 		people_mean = max(people_mean, a[i][j])
# 	# people_mean /= len(fourhop)
# 	l.append(people_mean)
# print (len(onehop), len(fourhop))
# plt.plot(l,color = "violet", label="Max at four hop")
# l = []
# for i in range(206, len(a)):
# 	people_mean = 0
# 	for j in fivehop:
# 		people_mean = max(people_mean, a[i][j])
# 		print (a[i][j], j)
# 	# people_mean /= len(fivehop)
# 	l.append(people_mean)
# print (len(onehop), len(fivehop))
# plt.plot(l,color = "green", label="Max at five hop")
# plt.xlabel("Time from collect message")
# plt.ylabel("Number of people")
# plt.title("People with distance from epicenter")
# ax.legend()
# plt.show()
# from tqdm import tqdm
# import pickle
# data = []
# for i in range(1,9):
# 	data.append(pickle.load(open("dataset/1/normal_" + str(i) + ".datapoint", "rb")))
# s1 = 0
# e1 = 1440
# s2 = 0
# e2 = 1440
# for i in data:
# 	s1 = max(s1,i[2])
# 	e1 = min(e1,i[3])
# 	s2 = max(s2,i[4])
# 	e2 = min(e2,i[5])
# from newsim import make_graph
# G, nodes = make_graph()
# # print (s1,e1,s2,e2) # 401 816 880 1298
# means1 = [{j:[] for j in nodes} for i in range(s1,e1+1)]
# for time in tqdm(range(s1,e1)):
# 	for i in data:
# 		for j in nodes:
# 			try:
# 				means1[time-s1][j].append(i[0][time-i[2]][j])
# 			except KeyError:
# 				means1[time-s1][j].append(0)
# 			except:
# 				import pdb; pdb.set_trace()
####################################################
# Saving mean and standard deviation
# import os
# files = os.listdir("dataset/1/normal")
# from tqdm import tqdm
# import pickle
# from newsim import make_graph
# import numpy as np
# G, nodes = make_graph()
# d = {i:{} for i in nodes}
# for file in tqdm(files):
# 	location_people,_,s1,e1,_,_ = pickle.load(open("dataset/1/normal/" + file,"rb"))
# 	for time in range(s1,e1):	
# 		# for i in location_people[time-s1]:
# 		for i in nodes:
# 			if time not in d[i]:
# 				d[i][time] = []
# 			if i in location_people[time-s1]:
# 				d[i][time].append(location_people[time-s1][i])
# 			else:
# 				d[i][time].append(0)
# for i in d:
# 	for j in d[i]:
# 		d[i][j] = (np.mean(d[i][j]), np.std(d[i][j]))
# pickle.dump(d, open("dataset/1/normal_means_and_std.pkl", "wb"))
#######################################################
# Finding abnormal nodes
# import os
# from tqdm import tqdm
# import pickle
# from newsim import make_graph
# import numpy as np
# G, nodes = make_graph()
# CONFIDENCE = 2
# d = pickle.load(open("dataset/1/normal_means_and_std.pkl"))
# for folder in ["normal", "abnormal"]:
# 	x = {}
# 	files = os.listdir("dataset/1/" + folder)
# 	for file in tqdm(files):
# 		location_people,_,s1,e1,_,_ = pickle.load(open("dataset/1/" + folder + "/" + file,"rb"))
# 		abnormal_nodes = []
# 		for time in range(s1,e1):
# 			for i in nodes:
# 				people_here = location_people[time-s1][i] if i in location_people[time-s1] else 0
# 				if (people_here - d[i][time][0] > CONFIDENCE*d[i][time][1]):
# 					abnormal_nodes.append(i)
# 		x[file] = abnormal_nodes
# 		print (len(abnormal_nodes))
# 	pickle.dump(abnormal_nodes, open("dataset/1/predicted_abnormal_for_"+folder, "wb"))
############################################################################
#Betweenness centrality calculation
# import networkx as nx
# from newsim import *
# G, nodes = make_graph()
# N = len(nodes)
# bet_centrality = nx.betweenness_centrality(G, normalized = False, endpoints = False)
############################################################################
import pickle
import numpy as np
import os
import matplotlib.pyplot as plt
import pandas as pd
from newsim import *
from geopy.distance import geodesic

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
		# plt.plot(ranks)
		# plt.title("Rank of the cluster containing the epicenter")
		# plt.savefig("viz_new/"+str(epicenter)+"_"+str(time_collect) + "/ranks_" + str(CUTOFF_PATH_LENGTH) + ".png")
		# plt.close()
		# plt.plot(dist_of_pred)
		# plt.title("Distance of prediction")
		# plt.savefig("viz_new/"+str(epicenter)+"_"+str(time_collect) + "/dist_from_pred_" + str(CUTOFF_PATH_LENGTH) + ".png")
		# plt.close()
		# plt.plot(dist_of_cluster)
		# plt.title("Distance of cluster mean")
		# plt.savefig("viz_new/"+str(epicenter)+"_"+str(time_collect) + "/dist_from_cluster_" + str(CUTOFF_PATH_LENGTH) + ".png")
		# plt.close()
				##### If you want to plot the points on a map
				# lats = []
				# longs = []
				# for i in abnormal_nodes:
				# 	lats.append(nodes[i][0])
				# 	longs.append(nodes[i][1])
				# plt.scatter(lats,longs, c = "red")
				# plt.scatter([nodes[epicenter][0]], [nodes[epicenter][1]], c = "green")
				# plt.title(str(time_collect))
				# plt.savefig("viz_new/"+str(epicenter)+"_"+str(time_collect) + "/" + str(time_after) + ".png")
				# plt.close()

