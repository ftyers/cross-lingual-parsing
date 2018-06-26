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

	def build_sentence(self):
		tokens = []
		for edge in self.edges:
			for node in self.nodes:
				if node.id == edge.to:
					# coosing the most common deprel
					deprel = max(set(node.deprels), key=node.deprels.count)

					# rewriting head and deprel
					features = list(node.features)
					features[6] = str(edge.fr)
					features[7] = deprel
					tokens.append('\t'.join(features))
					break
		return '\n'.join(tokens)


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


def cycle_detection(graph):
	"""
	Takes an instance of CurrentGraph. Returns a list with cycles,
	if there are any.
	"""
	cycles = []
	white, gray, black = set(graph.nodes), set(), set()
	while white:
		mapping = {}
		node = list(white)[0]
		gray.add(node)
		isCyclic, cyclic_node = dfs(node, None, white, gray, black, mapping)
		if isCyclic:
			cycle = get_the_cycle(mapping, cyclic_node)
			cycles.append(cycle)
	return cycles


def get_the_cycle(mapping, cyclic_node):
	"""
	Takes the nodes child/parent and the node which is guaranteed
	to be a part of cycle. Returns a list with all the nodes in cycle.
	"""
	cycle = [cyclic_node]
	cur = mapping[cyclic_node]
	i = 0
	while cur != cycle[0]:
		cycle.append(cur)
		cur = mapping[cur]

		# just in case something breaks and goes wrong, to avoid eternal loops 
		i += 1
		if i == 50:
			print('WAS NOT ABLE TO RETRIEVE A CYCLE')
			break

	return cycle


def dfs(node, parent, white, gray, black, mapping):
	move_vertex(node, white, gray)
	mapping[node] = parent
	for child in node.children:
		if child in black:
			continue
		if child in gray:
			mapping[child] = node
			return True, child
		isCyclic, cyclic_node = dfs(child, node, white, gray, black, mapping)
		if isCyclic:
			return True, cyclic_node
	move_vertex(node, gray, black)
	return False, None


def move_vertex(vertex, source_set, destination_set):
    source_set.remove(vertex)
    destination_set.add(vertex)


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
			# print(treebank[0][i])
			# print()
			# print(treebank[1][i])
			# raise DifferentLength
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


def get_combined(treebank):
	combined = []
	nok, cyclic = 0, 0
	for i, ms in enumerate(treebank):
		try:
			cur_g = CurrentGraph(ms.graph)
			# print(cur_g)
			# print('---')
			if cycle_detection(cur_g):
				# print('cyclic:')
				# print(cur_g.build_sentence())
				# quit()
				combined.append(str(ms.sentences[0]))
				cyclic += 1
			else:
				sent = cur_g.build_sentence()
				comments = ''.join(ms.sentences[0].comments)
				combined.append(comments + sent)
				nok += 1
		except (ConllIndexError, IndexError) as e:
			print('Sentence {}: a problem with ids.'.format(i))
	print('Number of sentences in combined model: ' + str(nok))
	print('cyclic: ' + str(cyclic))
	print('treebank len: '  + str(len(combined)))
	return combined



if __name__ == '__main__':
	if len(sys.argv) < 2:
		print('Usage:\npython3 conllu-graphs.py treebank1.conllu [treebank2.conllu, ...]')
		quit()
	treebank = get_treebank()
	# print(treebank[0].sentences[0])
	# cur_g = CurrentGraph(treebank[0].graph)
	# print(cur_g)
	# if not cycle_detection(cur_g):
	# 	sent = cur_g.build_sentence()
	# 	comments = ''.join(treebank[0].sentences[0].comments)
	# 	print(comments + sent)
	combined = get_combined(treebank)
	with open('tmp/combined_three.conllu', 'w') as f:
		f.write('\n\n'.join(combined))