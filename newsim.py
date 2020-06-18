import argparse
import math
import numpy as np
import pandas as pd
import networkx as nx
from networkx.algorithms.shortest_paths.generic import shortest_path
from networkx.algorithms.shortest_paths.unweighted import all_pairs_shortest_path
import random
import time
from tqdm import tqdm
import pickle
from copy import deepcopy

# Preprocessed Road Network Files
NODES = "data/nodes_1_8.csv"
SEGMENTS = "data/segments_1_8.csv"

START_TIME = 9*60 # 9 o clock in the morning
END_TIME = 17*60  # 5 o clock in the evening
STD_DEV = 30	  # People start with a normal distribution from Start time with this standard deviation
COLLECT_TIME_GO = 600 # This is taken as argparse input. It is the time when all people are given the message to collect.
RANDOM_PERCENT = 0.2  # Random percentage of people that do not go to home or to office
COLLECT_PERCENT = 0.01 # This is the percentage of people that collect when given the message to collect.
task = "simulate_normal" # "simulate_normal" means there is no collection of people
						 # "generate" generates the home and office of each simulated person
						 # "collect_together_while_going" implements the collection of people

def parse_args():
	parser = argparse.ArgumentParser('')
	parser.add_argument('--collect_percent',
                            type=float,
                            required=False,
                            default=COLLECT_PERCENT,
                            help='Percentage of people which collect at specified node.')
	parser.add_argument('--collect_time_go',
                            type=int,
                            required=False,
                            default=COLLECT_TIME_GO,
                            help='Time at which people get the message to collect.')
	parser.add_argument('--task',
							type=str,
							required =False,
							default = task,
							help = "Task for simulation.")
	return parser.parse_args()

# nodes = pd.read_csv(NODES, index_col = False)["ID"].tolist()
segments = pd.read_csv(SEGMENTS, index_col = False)

def make_graph():
	edges = list(zip(segments["u"].tolist(), segments["v"].tolist()))
	G = nx.Graph()
	G.add_edges_from(edges)
	nodes = list(set(segments["u"].tolist() + segments["v"].tolist()))
	return G, nodes

def generate_home_and_office_data(filename):
	G, nodes = make_graph()
	NUM_PEOPLE = len(nodes) * 100
	homes_and_offices = []
	hno_paths = []
	for i in tqdm(range(NUM_PEOPLE)):
		s = random.choice(nodes)
		t = random.choice(nodes)
		while True:
			try:
				x = shortest_path(G,s,t)
			except nx.exception.NetworkXNoPath:
				s = random.choice(nodes)
				t = random.choice(nodes)
				continue
			hno_paths.append(x)
			homes_and_offices.append((s,t))
			break
	pickle.dump((homes_and_offices,hno_paths), open(filename,'wb'))
	return G

def load_home_and_office_data(filename):
	return pickle.load(open(filename, "rb"))

def simulate_to_office_or_back(abs_start, abs_end, nodes, start_times, hno_paths, people_locations, 
		random_percentage, random_followed, collect, collect_time = -1, collect_percent = -1, collect_node = -1):
	if collect == True:
		assert collect_time != -1 and collect_node != -1 and collect_percent != -1
		collect_dict = {}
		collect_errors = 0
		total_collect_length = 0
	num_people = len(hno_paths)
	ret_people_locations = []
	people_queues = [[] for i in range(num_people)]
	random_followed_out = {}
	last_people_locations = None
	for time_now in tqdm(range(abs_start, abs_end)):
		for person_num in range(num_people):
			if collect == True and time_now == collect_time:
				if (random.uniform(0,1) < collect_percent):
					try:
						x = shortest_path(G,people_locations[person_num],collect_node)
						people_queues[person_num] = list(x)
						collect_dict[person_num] = True
						total_collect_length += len(x)
						continue
					except nx.exception.NetworkXNoPath:
						collect_errors += 1
			if len(people_queues[person_num]) > 0:
				location = people_queues[person_num].pop(0)
				people_locations[person_num] = location
			if start_times[person_num] == time_now:
				if collect == True and person_num in collect_dict:
					continue
				if (random.uniform(0,1) > random_percentage):
					if (random_followed is not None) and (person_num in random_followed):
						people_queues[person_num] = list(random_followed[person_num])
						people_queues[person_num].reverse()
					else:
						people_queues[person_num] = list(hno_paths[person_num])
				else:
					t = random.choice(nodes)
					while True:
						try:
							x = shortest_path(G,people_locations[person_num],t)
						except nx.exception.NetworkXNoPath:
							t = random.choice(nodes)
							continue
						people_queues[person_num] = list(x)
						random_followed_out[person_num] = list(x)
						break

		if collect == True and time_now == collect_time:
			print ("Average Collection length: ", (total_collect_length/len(collect_dict)))
			print ("Collection errors: ", (collect_errors/ (collect_errors + len(collect_dict))))

		ret_people_locations.append(convert_to_dict(list(people_locations)))
		last_people_locations = list(people_locations)

	return ret_people_locations, random_followed_out, last_people_locations

def simulate(nodes, num_people, hno_paths, people_locations, random_followed, 
					collect, collect_time = -1, collect_percent = -1, collect_node = -1):
	start_times = np.random.normal(START_TIME if random_followed is None else END_TIME, STD_DEV, num_people)
	start_times = [math.ceil(i) for i in start_times]
	abs_start = min(start_times)
	abs_end = max([len(hno_paths[i]) + start_times[i] for i in range(num_people)])
	print ("Start and end time: ",abs_start, abs_end)
	people_locations, random_followed, last_people_locations = simulate_to_office_or_back(abs_start, abs_end, nodes, 
											start_times, hno_paths, people_locations, RANDOM_PERCENT, random_followed,
											collect, collect_time, collect_percent, collect_node)
	return people_locations, random_followed, abs_start, abs_end, last_people_locations

def convert_to_dict(l):
	d = {}
	for j in l:
		if j in d:
			d[j] += 1
		else:
			d[j] = 1
	return d
def convert_to_dicts(input_list):
	ret_l = []
	for l in tqdm(input_list):
		d = {}
		for j in l:
			if j in d:
				d[j] += 1
			else:
				d[j] = 1
		ret_l.append(d)
	return ret_l

if __name__ == "__main__":
	args = parse_args()
	if args.task == "simulate_normal":
		G, nodes = make_graph()
		homes_and_offices, hno_paths = load_home_and_office_data("dataset/1/home_n_office_paths.pickle")
		num_people = len(homes_and_offices)
		people_locations = [s for (s,t) in homes_and_offices]
		total_people_locations_go, random_followed, s1, e1, last_people_locations = simulate(nodes, num_people, hno_paths, people_locations, None, False)
		people_locations = last_people_locations
		hno_paths_copy = (hno_paths)
		for i in (hno_paths_copy):
			i.reverse()
		total_people_locations_come, random_followed, s2, e2, last_people_locations = simulate(nodes, num_people, hno_paths_copy, people_locations, random_followed, False)
		pickle.dump((total_people_locations_go, total_people_locations_come, s1, e1, s2, e2), open("dataset/1/normal/normal_"+ str(random.randint(1,10000))+ ".datapoint", "wb"))
	elif args.task == "generate":
		generate_home_and_office_data("dataset/2/home_n_office_paths.pickle")
	elif args.task == "collect_together_while_going":
		G, nodes = make_graph()
		homes_and_offices, hno_paths = load_home_and_office_data("dataset/1/home_n_office_paths.pickle")
		num_people = len(homes_and_offices)
		people_locations = [s for (s,t) in homes_and_offices]
		collect_node = random.choice(nodes)
		total_people_locations_go, random_followed, s1, e1, last_people_locations = simulate(nodes, num_people, hno_paths, people_locations, None, True, args.collect_time_go, args.collect_percent, collect_node)
		pickle.dump((total_people_locations_go, s1, e1), open("dataset/1/abnormal/abnormal_go_" + str(args.collect_percent) + "_" + str(args.collect_time_go) + "_" + str(collect_node) + "_" + str(random.randint(1,10000))+ ".datapoint", "wb"))
