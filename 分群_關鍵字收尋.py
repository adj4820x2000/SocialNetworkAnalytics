import community as community_louvain
import networkx as nx
import csv
import argparse
import matplotlib.pyplot as plt
from jieba.analyse import *
import ujson

parser = argparse.ArgumentParser()
parser.add_argument('-A', type=str, help='an string of A', dest='A', default='default')
parser.add_argument('-B', type=str, help='an string of B', dest='B', default='default')
args = parser.parse_args()

G = nx.Graph()

with open('C:/Users/T2-503/Desktop/HW/社群媒體資料分析實務/Final_Project/ptt_node_with_edge.csv', encoding='utf-8') as csv_file:
	csv_reader = csv.reader(csv_file)
	line_count = 0
	for row in csv_reader:
		if line_count == 0:
			line_count += 1
			continue

		G.add_edge(row[1], row[2])

		line_count += 1
	print('Edges =', G.number_of_edges())
	print('Nodes =', G.number_of_nodes())

partition = community_louvain.best_partition(G)

print('Community :', max(partition.values()))

count = 0
A=0
for com in set(partition.values()):
    list_nodes = [nodes for nodes in partition.keys() if partition[nodes]== com]
    if len(list_nodes) > 1000 :
        content = ''
        count = count + 1
        print('Group key words', count ,':')
        with open('C:/Users/T2-503/Desktop/HW/社群媒體資料分析實務/Final_Project/WomenTalk-0-500.json', encoding='utf-8') as json_file:
            data = ujson.load(json_file)
            for p in data['articles']:
                for author in list_nodes:
                    try:
                        if  p['author'].split(' (')[0] == author :
                            content = content + p['article_title'];
                    except:
                        A=1
        for keyword, weight in extract_tags(content, withWeight=True):
            print('%s %s' % (keyword, weight))

       

if(args.A != 'default' and args.B != 'default'):
	preds = nx.jaccard_coefficient(G, [(args.A, args.B)])

	if(partition[args.A] == partition[args.B]):
		print('In same community')

	for u, v, p in preds:
		print(u, v, p)		


# draw the graph
#pos = nx.spring_layout(G)
# color the nodes according to their partition
#cmap = cm.get_cmap('viridis', max(partition.values()) + 1)
#nx.draw_networkx_nodes(G, pos, partition.keys(), cmap=cmap, node_color=list(partition.values()))
#nx.draw_networkx_edges(G, pos, alpha=0.5)
#plt.show()