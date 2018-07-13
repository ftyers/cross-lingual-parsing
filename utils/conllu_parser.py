class Sentence:

	def __init__(self, blokk):
		self.spans = {} # keyed on the first token in the span
		self.empties = {} # keyed on the token in the span
		self.tokens = [] # only legit tokens ... 11-tuple or list
		self.comments = [] # list of comments

		for line in blokk.split('\n'):
			if line == '': continue
			if line[0] == '#':
				self.comments.append(line+'\n')
				continue
			row = tuple(line.split('\t'))
			if row[0].count('.') > 0:
				id = int(row[0].split('.')[0])
				self.empties[id] = row		
				continue
			if row[0].count('-') > 0:
				id = int(row[0].split('-')[0])
				self.spans[id] = row
				continue
			self.tokens.append(row)

	def __len__(self):
		return len(self.tokens)

	def __str__(self):
		"""
		when you print out the sentence, you first print out the comments,
		then you iterate through the tokens
		   you get the id, if there is a span corresponding to that id, print the span
		   print the token
		   if there is an empty corresponding to the id, you print the empty
		"""
		out = ''
		for line in self.comments:
			out += line
		if 0 in self.empties:
			out += '\t'.join(self.empties[0]) + '\n'
		for token in self.tokens:
			idx = int(token[0])
			if idx in self.spans:
				out += '\t'.join(self.spans[idx]) + '\n'
			out += '\t'.join(token) + '\n'
			if idx in self.empties:
				out += '\t'.join(self.empties[idx]) + '\n'

		return out


class MultiSentence:
	"""
	self.sentences -- a list of Sentence objects
	self.comments -- the longest comments of the three sentences
	self.graph -- an object of FullGraph class
	"""

	def __init__(self, sentences):
		self.sentences = sentences
		self.merge_comments([s.comments for s in self.sentences if s.comments])
		self.graph = FullGraph([s.tokens for s in self.sentences])

	def merge_comments(self, all_comm):
		if not all_comm:
			self.comments = []
		else: # if the comments are not equal, choose the longest ones
			self.comments = max(all_comm, key=len)

	def __repr__(self):
		graph = ''
		for edge in self.graph.edges:
			graph += str(self.graph.edges[edge]) + '\n'
		return graph.strip()


class DifferentLength(Exception):
	def __repr__(self):
		return "The lenghts of the sentecnes are not equal."		


class ZeroLength(Exception):
	def __repr__(self):
		return "There is no sentences."


class ConllIndexError(Exception):
	def __repr__(self):
		return "There expected index doesn't match the resulting index."


class FullGraph:
	"""a graph representation for merged sentences"""
	def __init__(self, sentences):

		if len(sentences) == 0: # if there're no sentences, throw an exception
			raise ZeroLength

		shortest = min(sentences, key=lambda x: len(x))
		longest = max(sentences, key=lambda x: len(x))
		if len(shortest) != len(longest): # if there's a different number of tokens, throw an exception
			raise DifferentLength
		self.sentences = sentences
		self.build_graph()

	def build_graph(self):
		"""
		Takes the nodes from the first sentence.
		Then builds the edges by iterating each sentence.  
		"""
		self.nodes = [] # a list of tokens
		self.edges = {} # a dict of edges keyed on (id, head,deprel),
		for token in self.sentences[0]:
			self.nodes.append(Node(token))
		for sent in self.sentences:
			for token in sent:
				fr, to, deprel = int(token[6]), int(token[0]), token[7]
				cur_edge = self.edges.get((fr, to), Edge(fr, to, deprel))
				cur_edge.weight += 1
				self.edges[(fr, to)] = cur_edge

		# fill the in_edges lists for each node
		for node in self.nodes:
			for fr, to in self.edges:
				if to == node.id:
					edge = self.edges[(fr, to)]
					node.in_edges.append(edge)
					node.deprels.append(edge.deprel)


class Node:
	"""
	A node class which represents a token in the FullGraph.
	features -- a tuple formed from a connlu line
	id -- the number of the token
	in_edges -- a list of incoming edges
	"""
	def __init__(self, features):
		self.features = features
		self.id = int(features[0])
		self.in_edges = []
		self.deprels = []

	def __repr__(self):
		return '\t'.join(self.features)


class Edge:
	"""
	Represents a weighted edge of the graph.
	deprels -- a list of all of the deprels with this source and destination
	weight -- the number of times an edge occured in the data
	"""
	def __init__(self, source, destination, deprel):
		self.fr = source
		self.to = destination
		self.weight = 0
		self.deprel = deprel

	def __repr__(self):
		return 'from ' + str(self.fr) + ', to ' + str(self.to) + ', weight '\
		       + str(self.weight) + ', labels ' + str(self.deprel)


if __name__ == '__main__':
	for blokk in input().split('\n\n'):
		if blokk.strip() == '': continue
		sent = Sentence(blokk)
		print(sent)
