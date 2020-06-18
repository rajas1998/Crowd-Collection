# Crowd-Collection

This repository simulates the movement of people and predicts the collection of people using telecom data. The details of the method can be found [here](https://www.overleaf.com/read/qpgybdhbhvqn).

### Creating Simulation Data

The road network data for the city under consideration is present in `data/`.

```bash
	python3 newsim.py --task generate
	python3 newsim.py --task simulate_normal
	python3 newsim.py --task collect_together_while_going
```
These commands runs the simulation according to the default parameters. The first command generates homes and offices for all the simulated people and stores them as a pickle file. 

"simulate_normal" then simulates people going randomly at normally distributed start time from their home to the office during morning. A parameterized fraction of people do not go to their home and instead go to a random node. At night, a similar process occurs with people going back to their homes from their offices.

"collect_together_while_going" makes the abnormal data, i.e data where people start collecting together. A parameterized fraction of people (specified by --collect_percent) are given a message at a specified time (specified by --collect_time_go) to collect at a specified node, called the epicenter. The simulation data here is stored in `dataset/1/`. The saving format is such that if a 0.01, fraction of people do not go their offices when others are, people get the message to collect at 8 o clock, the epicenter is at road node "400", the datapoint will be stored as abnormal_go_0.01_480_400.datapoint.

### Predicting the Epicenter at real time

The epicenter is predicted using the method described in the [document](https://www.overleaf.com/read/qpgybdhbhvqn).

```bash
	python3 make_prediction.py save_mean_and_std
	python3 make_prediction.py predict_abnormal_nodes
	python3 make_prediction.py predict_epicenter
```

"save_mean_and_std" saves the mean and standard deviations of the people present at different nodes in the road network, using the normal data, i.e when people are not collecting. "predict_abnormal_nodes" then uses these values to predict the abnormal nodes present in the road network at any given time. "predict_epicenter" then predicts the epicenter at which the people may be thought to be collecting, with the prediction and its distance from the actual epicenter being printed to the screen.

### Using Real Data

Currently we did not have the complete real data to test our model. Using skeleton of the real data present in `data/May,2020.csv`,this real data has been converted to the mean and standard deviation pickle file which is used for the other files. However, it has been assumed that the towers have been mapped to the road network data, and the "Node id" field in the csv is thus filled appropriately. So, the command required to run on real data would be,

```bash
	python3 convert_real_data.py PATH_TO_REAL_DATA.csv
	python3 make_prediction.py predict_abnormal_nodes
	python3 make_prediction.py predict_epicenter
```
