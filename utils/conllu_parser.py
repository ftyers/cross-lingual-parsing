import sys

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
			row = line.split('\t')
			if row[0].count('.') > 0:
				id = int(row[0].split('.')[0])
				self.empties[id] = row		
				continue
			if row[0].count('-') > 0:
				id = int(row[0].split('-')[0])
				self.spans[id] = row		
				continue
			self.tokens.append(row)

	# when you print out the sentence, you first print out the comments, 
	# then you iterate through the tokens
	#    you get the id, if there is a span corresponding to that id, print the span
	#    print the token
	#    if there is an empty corresponding to the id, you print the empty

	def __str__(self):
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


#class MultiSentence:
#	weights = {} # keyed on (id, head,deprel), e.g. weights[(3,0 ,'root')] = 0.445


for blokk in sys.stdin.read().split('\n\n'):
	if blokk.strip() == '': continue
	sent = Sentence(blokk)
	print(sent)


