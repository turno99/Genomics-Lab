import networkx as nx
import matplotlib.pyplot as plt
import copy

sequence = "GACTTACGTACT"
k = 3

def generate_kmers(sequence, k):
    kmers = []
    for i in range(len(sequence) - k + 1):
        kmer = sequence[i:i + k]
        kmers.append(kmer)
    return kmers

def generate_de_bruijn_graph(kmers):
    de_bruijn_graph = {}
    in_degrees = {}
    out_degrees = {}

    for kmer in kmers:
        prefix = kmer[:-1]
        suffix = kmer[1:]
        if prefix not in out_degrees:
            out_degrees[prefix] = 0
        
        if prefix not in in_degrees:
            in_degrees[prefix] = 0
        
        if suffix not in out_degrees:
            out_degrees[suffix] = 0

        if suffix not in in_degrees:
            in_degrees[suffix] = 0            
        if prefix not in de_bruijn_graph:
            de_bruijn_graph[prefix] = []
             
        if suffix not in de_bruijn_graph:
            de_bruijn_graph[suffix] = []
        de_bruijn_graph[prefix].append(suffix)

        out_degrees[prefix] = out_degrees.get(prefix, 0) + 1
        in_degrees[suffix] = in_degrees.get(suffix, 0) + 1

    return de_bruijn_graph, in_degrees, out_degrees

def find_starting_node(in_degrees, out_degrees):
    starting_node = []
    for node in in_degrees.keys():
        if in_degrees[node] < out_degrees[node]:
            if node not in starting_node: 
                starting_node.append(node)
    return starting_node

def valid_euler_walk(path) -> bool:
    graph_2 = copy.deepcopy(db_graph_2)
    path2 = copy.deepcopy(path)
    n = len(path2)
    for i in range (n - 1):
        if path2[i+1] not in graph_2[path2[i]]:
            return False
        else:
            graph_2[path2[i]].remove(path2[i+1])
    
    return True


all_euler_walks = []

def dfs(path, graph, node, level = 0):
    l = len(path)
    if l == len(sequence) - k + 2:
        if valid_euler_walk(path):
            all_euler_walks.append(path)
            return
    if node not in graph: return
    sz = len(graph[node])  
    for i in range(sz):
        to = graph[node][0]
        new_path = path + [to]
        graph[node].remove(to)
        dfs(new_path,graph,to, level+1)
        graph[node] = graph[node] + [to]
 
def visualize_graph(graph):
    pos = nx.spring_layout(graph, seed=42)
    plt.figure(figsize=(10, 8))
    nx.draw(graph, pos, with_labels=True, node_size=3000, node_color='skyblue', font_size=10, font_weight='bold', arrowsize=20)
    plt.title("De Bruijn Graph Visualization")
    plt.show()

def print_all_walks():
    walk_set = set()
    for walk in all_euler_walks:
        path = " -> ".join(walk)
        walk_set.add(path)
    print(f"Number of distinct Eulerian walk(s): {len(walk_set)}")
    print("The walks are:")
    for walk in walk_set:
        print(walk)

kmers = generate_kmers(sequence,k)

db_graph, in_degrees, out_degrees = generate_de_bruijn_graph(kmers)

db_graph_2 = copy.deepcopy(db_graph)
db_graph_3 = copy.deepcopy(db_graph)
for node in kmers:
    start_node = node[:-1]
    dfs([start_node],db_graph,start_node)
    
print_all_walks()

G = nx.MultiDiGraph(db_graph_3)  
visualize_graph(G)

