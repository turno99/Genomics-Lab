#sequences = ["A C G C G T T G G G C G A T G G C A A C",
#             "A C G C G T T G G G C G A C G G T A A T",
#             "A C G C A T T G A A T G A T G A T A A T",
#             "A C G C A T T G A A T G A T G A T A A T",
#             "A C A C A T T G A G T G A T A A T A A T"]
sequences = ["GTGCTGCACGGCTCAGTATAGCATTTACCCTTCCATCTTCAGATCCTGAA",
"ACGCTGCACGGCTCAGTGCGGTGCTTACCCTCCCATCTTCAGATCCTGAA",
"GTGCTGCACGGCTCGGCGCAGCATTTACCCTCCCATCTTCAGATCCTATC",
"GTATCACACGACTCAGCGCAGCATTTGCCCTCCCGTCTTCAGATCCTAAA",
"GTATCACATAGCTCAGCGCAGCATTTGCCCTCCCGTCTTCAGATCTAAAA"]


def hamming(s1, s2):
    return sum(c1!=c2 for c1,c2 in zip(s1,s2))

def strFormat(i, j):
    return "(" + str(i) + " " + str(j) + ")"

modules_available = False
try:
    import matplotlib.pyplot as plt
    import networkx as nx
    modules_available = True
except ImportError:
    modules_available = False

n = len(sequences)

dist_matrix = [[hamming(sequences[i],sequences[j]) for i in range(n)] for j in range(n)]

sequence_names = []
for i in range(n):
    seq_name = str(i+1)
    sequence_names.append(seq_name)

distance = {row: {col: None for col in sequence_names} for row in sequence_names}


if modules_available:
    G = nx.Graph()
else:
    G = None    

if modules_available:
    G.add_nodes_from(sequence_names)

joins = 0

for i in range(n):
    for j in range(n):
        distance[str(i+1)][str(j+1)] = hamming(sequences[i],sequences[j])

while(joins<n-1):
    min_dist = 100000
    key1 = ""
    key2 = ""
    for row in distance.keys():
        for col in distance[row]:
            if (distance[row][col]) is not None and (distance[row][col] < min_dist) and(row!=col):
                key1 = row
                key2 = col
                min_dist = distance[row][col]
    print(f'joining {key1} and {key2}')
    new_key = strFormat(key1,key2)
    print(new_key)
    if(modules_available):
        G.add_node(new_key)
        G.add_edge(key1,new_key)
        G.add_edge(key2,new_key)
    distance[new_key] = {}
    for row in distance.keys():
        val1 = 0
        val2 = 0
        if row != key1 and row!=key2 and row!=new_key:
            if(row in distance[key1]):
                val1 = distance[key1][row]
            else:
                val1 = distance[row][key1]
            if(row in distance[key2]):
                val2 = distance[key2][row]
            else:
                val2 = distance[row][key2]
            distance[new_key][row] = 0.5*(val1+val2)
            distance[row][new_key] = 0.5*(val1+val2)
    
    del distance[key1]
    del distance[key2]
    for row_data in distance.values():
        if key1 in row_data:
            del row_data[key1]
        if key2 in row_data:
            del row_data[key2]
    joins = joins + 1
    print(distance)

if modules_available:    
    plt.figure(figsize=(8, 6))
    plt.clf()
    plt.title('Phylogenetic Tree')
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, font_weight='bold', node_color='skyblue', node_size=2500) 
    plt.show()