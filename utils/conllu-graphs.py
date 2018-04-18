import sys

def get_treebank():
	"""
	Reads the conllu files from command line arguments.
	Returns a list of lists with sctrings, where
	sentences are grouped by the id of the sentence. 
	"""
	treebank = []
	for fname in sys.argv[1:]:
		with open(fname) as f:
			sents = f.read().split('\n\n')
			treebank.append(sents) # at this point, treebank has n sub-lists for each file

	# re-structuring the treebank, so that the sub-lists contain n versions for each sentence
	treebank = [[li[i] for li in treebank] for i in range(len(treebank[0]))]
	return treebank



def analyse_sents():
	pass


def get_weights(sents):
	pass


def get_spanning_tree(G, W):
	MST = {} # This is the first MST subgraph
	
	print('G',G)
	print('W',W)
	for i in G:
		print(i, G[i])
		# the root node has no incoming arcs
		if i == 0:
			MST[0] = []
			continue
		if i not in MST:
			MST[i] = []
		# find incoming arcs
		incoming = [w for w in G.keys() if i in G[w]]
		max_j = -1
		if incoming != []:
			# max_j is the maximum incoming arc
			max_j = max(incoming, key=lambda j : W[j][i])
			if max_j not in MST:
				MST[max_j] = []
			MST[max_j].append(i)
	return MST


def dfs(graph, start, end):
	fringe = [(start, [])]
	while fringe:
		state, path = fringe.pop()
		if path and state == end:
			yield path
			continue
		for next_state in graph[state]:
			if next_state in path:
				continue
			fringe.append((next_state, path+[next_state]))


def enumerate_cycles(spanning_tree):
	return [[node]+path for node in spanning_tree for path in dfs(spanning_tree, node, node)]


def mst():
	pass


if __name__ == '__main__':
	if len(sys.argv) < 2:
		print('Usage:\npython3 conllu-graphs.py treebank1.conllu [treebank2.conllu, ...]')
		quit()
	treebank = get_treebank()
	for group in treebank:
		print(group)
	# analyse_sents(treebank[0])

	# for i, sent in enumerate(treebank):
	# 	treebank[i] = analyse_sents(sent)
	# with open('output.conllu') as f:
	# 	f.write('\n\n'.join(treebank))
