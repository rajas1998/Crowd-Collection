import math
import numpy as np
import random
import pandas as pd
import pickle
from geopy.distance import geodesic
from tqdm import tqdm

def indices_in_between(l, minvalue, maxvalue):
	#returns the indices according to the list l
	minindex = len(l)
	for i in range(len(l)):
		if (l[i][0] >= minvalue):
			minindex = i
			break
	maxindex = len(l)
	for i in range(minindex, len(l)):
		if (l[i][0] > maxvalue):
			maxindex = i - 1
			break
	return (minindex, maxindex)

def return_indices(l, minindex, maxindex, maxsamples):
	#returns the original tower numbers which are going to be marked abnormal
	indices = random.sample(range(minindex, maxindex+1), min(maxsamples, maxindex - minindex + 1))
	return [l[i][1] for i in indices]

dists = pickle.load(open("data/dists", "r"))
telecom_data = pd.read_csv(open("data/augmented_telecom_data.csv", "r"))
means = telecom_data["mean"].tolist()
n = len(means)
std_devs = [max(means[i]/10.0,0.1) for i in range(n)]
given_abnormal_indices = []
# epicenter = 1117
# epicenter = 853
epicenter = random.randint(0,n-1)
epicenter_lat = telecom_data["lat"][epicenter]
epicenter_long = telecom_data["long"][epicenter]

def create_data():
	dist_from_epicenter = list(dists[epicenter])
	dist_from_epicenter = [(dist_from_epicenter[i]/1000,i) for i in range(n)]
	dist_from_epicenter.sort()
	data = []
	repeat_timesteps = 1
	start_dist = 10
	for dist in range(10,-1,-1):
		for timestep in range(repeat_timesteps):
			mindist = 0.5*dist
			maxdist = 0.5*(dist+1)
			minind, maxind = indices_in_between(dist_from_epicenter, mindist, maxdist)
			# print (minind, maxind)
			abnormal_indices = return_indices(dist_from_epicenter, minind, maxind, 20)
			given_abnormal_indices.append(abnormal_indices)
			# print (len(abnormal_indices))
			sample_people = np.random.normal(means, std_devs, n)
			sample_people = [int(i) for i in sample_people]
			for i in abnormal_indices:
				sample_people[i] = int(math.ceil(means[i] + 3*std_devs[i]))
			data.append(sample_people)
	return data

data = np.array(create_data())
std_devs = np.array(std_devs)
means = np.array(means)
scores = []
detected_abnormal_indices = []
lats,longs = [],[]

# Create the scores
for i,datapoint in (enumerate(data)):
	abnormal_indices = np.nonzero(datapoint - means >= 3 * std_devs)[0]
	# For now remove the ones that came due to randomness
	abnormal_indices = list(given_abnormal_indices[i])
	detected_abnormal_indices.append(abnormal_indices)
	score = []
	lat_mean = 0.0
	long_mean = 0.0
	for i in abnormal_indices:
		lat_mean += telecom_data["lat"][i]
		long_mean += telecom_data["long"][i]
	lat_mean /= len(abnormal_indices)
	long_mean /= len(abnormal_indices)
	lats.append(lat_mean)
	longs.append(long_mean)
	# print ("Distance of mean from epicenter is", geodesic((lat_mean, long_mean), (epicenter_lat, epicenter_long)).m)
	for i in range(n):
		sum_dist = 0.0
		for j in abnormal_indices:
			sum_dist += dists[i][j]
		score.append(sum_dist/len(abnormal_indices))
	scores.append(score)

# Print the score statistics
print ("Addition of distance")
for score_list in scores:
	val = score_list[epicenter]
	tmp = list(score_list)
	tmp.sort()
	print (tmp.index(val), val, dists[epicenter][score_list.index(min(score_list))])
	# ind = score_list.index(min(score_list))
	# print (dists[epicenter][ind])

# Print who is closest to the mean
print ("Mean estimate --")
for i in range(len(lats)):
	dist_from_mean = []
	for j in range(n):
		dist_from_mean.append((geodesic((lats[i], longs[i]), (telecom_data["lat"][j], telecom_data["long"][j])).m, j))
	dist_from_mean.sort()
	for ind in range(n):
		if dist_from_mean[ind][1] == epicenter:
			print ("The rank and distance from mean of the epicenter is ", ind, dist_from_mean[ind][0])
			break
	print ("Distance of predicted from epicenter is ", dists[epicenter][dist_from_mean[0][1]])

# Rate of the decrease in score
print ("Rate of decrease")
for i in range(1,len(scores)):
	newscores = [scores[i][j] - scores[i-1][j] for j in range(n)]
	val = newscores[epicenter]
	tmp = list(newscores)
	tmp.sort()
	print (tmp.index(val), dists[epicenter][newscores.index(min(newscores))])

# Sanity check
# print (len(detected_abnormal_indices))
for i,l in enumerate(detected_abnormal_indices):
	for j in given_abnormal_indices[i]:
		if j not in l:
			print "Not possible!"


