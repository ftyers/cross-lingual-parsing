import sys
from collections import Counter
from conllu_parser import *

RECURSION_DEPTH = 50

class CurrentGraph:

	def __init__(self, nodes):
		self.nodes = nodes
		self.choose_edges()
		self.make_children()

	def choose_edges(self):
		# for each node, chosing the incoming edge eith the highest weight
		self.edges = []
		for node in self.nodes:
			best_edge = max(node.in_edges, key=lambda x: x.weight)
			self.edges.append(best_edge)

	def build_sentence(self):
		tokens = []
		for edge in self.edges:
			for node in self.nodes:
				if node.id == edge.to:
					# coosing the most common deprel
					if edge.fr == 0:
						deprel = 'root'
					else:
						if 'root' in node.deprels:
							node.deprels.remove('root')
						deprel = max(set(node.deprels), key=node.deprels.count)

					# rewriting head and deprel
					features = list(node.features)
					features[6] = str(edge.fr)
					features[7] = deprel
					tokens.append('\t'.join(features))
					break
		return '\n'.join(tokens)


	def make_children(self): ## TODO wrong indices error handling

		# crearing _clean_ children attribute for each node
		for node in self.nodes:
			node.children = []

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
	nob = []
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

			
			lens = Counter([len(li[i]) for li in treebank])
			if 3 in lens.values(): # если есть хотя бы три предложения одинаковой длины
				multisentences.append(MultiSentence(fix_for_diff_len(treebank, lens, i)))
			else:
				nob.append(treebank[0][i])
			# raise DifferentLength
	print('{} sentences out of {} were discarded because of the different size'.format(diff_len, len(treebank[0])))
	return multisentences, nob


def fix_for_diff_len(treebank, lens, i): # TODO: fix
	for key in lens: # получаем эту длину
		if lens[key] == 3:
			thelen = key
	# предложения с одинаковой длиной
	return [li[i] for li in treebank if len(li[i]) == thelen]


def mst(cur_g, ms, depth=0):

	if depth == RECURSION_DEPTH: # stop the recursion if the dpepth limit is exeeded
		print('cyclic sent: ')
		print(cur_g)
		quit()
		return str(ms.sentences[0]), False

	cycles = cycle_detection(cur_g)
	if cycles:
		# fixing cycles
		changed_nodes = []
		for cycle in cycles:
			changed_nodes += resolve_cycle(cycle)

		# rebuilding the graph
		for node in changed_nodes:
			cur_g.nodes[node.id - 1] = node
		cur_g.choose_edges()
		cur_g.make_children()
		return mst(cur_g, ms, depth=(depth+1))
	else:
		return serialize_valid_mst(cur_g, ms), True



def get_combined(treebank):
	combined = []
	nok, cyclic = 0, 0
	for i, ms in enumerate(treebank):
		try:
			cur_g = CurrentGraph(ms.graph.nodes)
			tree, sucess = mst(cur_g, ms)
			combined.append(tree)
			if sucess:
				nok += 1
			else:
				cyclic += 1
		except (ConllIndexError, IndexError) as e:
			print('Sentence {}: a problem with ids.'.format(i))
	print('Number of sentences in combined model: ' + str(nok))
	print('cyclic: ' + str(cyclic))
	print('treebank len: '  + str(len(combined)))
	return combined


def serialize_valid_mst(cur_g, ms):
	sent = cur_g.build_sentence()
	comments = ''.join(ms.sentences[0].comments)
	return comments + sent

def resolve_cycle(cycle):

	max_incoming = find_max_incoming(cycle)
	# print('max_incoming: ' + str(max_incoming))

	# leaving only the node with maximum incoming edge for the node in question
	node_id = max_incoming.to
	for node in cycle:
		if node.id == node_id:
			node.in_edges = [max_incoming]

	# print(cycle)
	# print(cycle[0].in_edges)
	# print(cycle[1].in_edges)
	return cycle


def find_max_incoming(cycle):
	"""
	looking for maximum incoming edge
	"""
	indices = [node.id for node in cycle]
	max_incoming = None
	for node in cycle:
		inc_edges = [e for e in node.in_edges if e.fr not in indices]
		try:
			cur_max = max(inc_edges, key=lambda x: x.weight)
		except ValueError:
			cur_max = None

		# the first case
		if max_incoming is None:
			max_incoming = cur_max
			continue
		
		if cur_max and cur_max.weight > max_incoming.weight:
			max_incoming = cur_max

	if max_incoming is None: # kinda giving up for now. TODO: work out why it happens
		max_incoming = cycle[0].in_edges[0]
	return max_incoming


if __name__ == '__main__':
	if len(sys.argv) < 2:
		print('Usage:\npython3 conllu-graphs.py treebank1.conllu [treebank2.conllu, ...]')
		quit()
	treebank, difflen_nob = get_treebank()
	print('difflen_nob: ' + str(len(difflen_nob)))
	combined = get_combined(treebank)
	with open('tmp/combined_four.conllu', 'w') as f:
		f.write('\n\n'.join(combined))
	with open('tmp/combined_difflen_four.conllu', 'w') as f:
		f.write('\n\n'.join(str(s) for s in difflen_nob))