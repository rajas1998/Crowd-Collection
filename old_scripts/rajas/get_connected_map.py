import pandas as pd
import networkx as nx

import warnings
warnings.filterwarnings("ignore")
############################################### Change This Only ###########################################
base_dir = "/media/root/data/swiggy/"
data_dir = base_dir + "data_DEL/"

map_dir = data_dir + "map/"

############################################################################################################

DG = nx.DiGraph()

# add nodes
nodes = pd.read_csv(map_dir + "nodes_mod.csv")
nodes = nodes.drop('al', axis = 1)
nodes = nodes.set_index('id')
nodes = nodes.to_dict('index')
nodes = list(nodes.items())

DG.add_nodes_from(nodes)

# add edges
edges = pd.read_csv(map_dir + "segments_mod.csv")
edges = edges.drop(['list', 'int', 'pid', 'oneway'], axis = 1)
rows = list(edges.itertuples(index=False, name=None))
rows = [list(i) for i in rows]
rows = [(i[0], i[1]) for i in rows]

DG.add_edges_from(rows)

max_comp = max(nx.strongly_connected_component_subgraphs(DG), key=len)

print("Percent Nodes in Maximum Strongly Connected Component = %f"%(len(max_comp.nodes)/len(nodes)))

nodes = pd.read_csv(map_dir + "nodes_mod.csv")
nodes = nodes[nodes.id.isin(list(max_comp.nodes))]
nodes.to_csv(map_dir + "nodes_mod_connected.csv", index=False, float_format='%.7f')

print((len(nodes)))
print(len(max_comp.nodes))
print("These must be equal\n If not equal, implies segments contain edges between garbage nodes")

edges = pd.read_csv(map_dir + "segments_mod.csv")
edges = edges[edges.u.isin(nodes.id) & edges.v.isin(nodes.id)]
edges = edges.drop_duplicates(['u', 'v'])

print(len(edges))
print(len(max_comp.edges))
print("These must be equal\n If not equal, implies segments contain edges between garbage nodes")

edges.to_csv(map_dir + "segments_mod_connected.csv", index=False)