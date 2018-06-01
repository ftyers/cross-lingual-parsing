import sys
from conllu_parser import *


class CurrentGraph:

	def __init__(self, full_graph):
		self.nodes = full_graph.nodes
		self.edges = []
		self.choose_edges()
		self.make_children()

	def choose_edges(self):
		# for each node, chosing the incoming edge eith the highest weight
		for node in self.nodes:
			best_edge = max(node.in_edges, key=lambda x: x.weight)
			self.edges.append(best_edge)

	def make_children(self): ## TODO wrong indices error handling
		for edge in self.edges:
			if edge.fr != 0:
				cur_token = self.nodes[edge.fr - 1]
				child_token = self.nodes[edge.to - 1]
				if cur_token.id != edge.fr or child_token.id != edge.to:
					raise ConllIndexError
				cur_token.children.append(child_token)

	def __repr__(self):
		res = ''
		for e in self.edges:
			res += str(e) + '\n'
		return res.strip()


def my_cycle_detection(graph):
	cycles = []
	white, gray, black = set(self.nodes), set(), set()
	while white:
		mapping = {}
		node = white.pop()
		gray.add(node)
		mapping[node] = None
		cycle, white, gray, black = my_dfs(node, white, gray, black)
	return cycles


def my_dfs(node, white, gray, black):
	for child in node.children:
		if child in black:
			continue
		if child in gray:
			print('cycle found')


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

			# at this point, treebank has n sub-lists for each file,
			# where n is a number of treebank versions
			treebank.append([Sentence(s) for s in sents])

	# re-structuring the treebank, froming a list of MultiSentence instances:
	# each multisentence is a compillation of n sentence versions
	multisentences = []
	diff_len = 0
	for i in range(len(treebank[0])):
		try:
			multisentences.append(MultiSentence([li[i] for li in treebank]))
		except DifferentLength:
			diff_len += 1
			print(treebank[0][i])
			print()
			print(treebank[1][i])
			quit()
	print('{} sentences out of {} were discarded because of the different size'.format(diff_len, len(treebank[0])))
	return multisentences


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
	print(treebank[0])
	for token in treebank[0].sentences[0].tokens:
		print(token)
	print()
	cur_g = CurrentGraph(treebank[0].graph)
	print(str(cur_g))

	# for i, sent in enumerate(treebank):
	# 	treebank[i] = analyse_sents(sent)
	# with open('output.conllu') as f:
	# 	f.write('\n\n'.join(treebank))
