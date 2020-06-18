import pandas as pd
import numpy as np
import pickle

telecom_data = pd.read_csv(open("data/May,2020.csv", "r"))

datetime_column = pd.to_datetime(telecom_data["Date Time"], format = "%Y-%m-%d %H:%M:%S")
telecom_data["tot_seconds"] = datetime_column.dt.hour * 3600 + datetime_column.dt.minute * 60 + datetime_column.dt.second
nodes = set(telecom_data["Node id"].tolist())
d = {i:{} for i in nodes}

for time_considered in (list(set(telecom_data["tot_seconds"].to_list()))):
	tmp = telecom_data[telecom_data["tot_seconds"] == time_considered]
	nodeids = tmp["Node id"].to_list()
	numpeople = tmp["Total Active Customer"].tolist()
	for i in range(len(nodeids)):
		if time_considered not in d[nodeids[i]]:
			d[nodeids[i]][time_considered] = []
		d[nodeids[i]][time_considered].append(numpeople[i])
for i in d:
	for j in d[i]:
		d[i][j] = (np.mean(d[i][j]), np.std(d[i][j]))
pickle.dump(d, open("dataset/1/real_data_means_and_std.pkl", "wb"))