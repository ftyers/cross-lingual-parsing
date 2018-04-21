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

	def __str__(self):
		# when you print out the sentence, you first print out the comments, 
		# then you iterate through the tokens
		#    you get the id, if there is a span corresponding to that id, print the span
		#    print the token
		#    if there is an empty corresponding to the id, you print the empty
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

	def __init__(self, sentences):
		self.sentences = sentences
		self.merge_sents()
		# weights = {} # keyed on (id, head,deprel), e.g. weights[(3,0 ,'root')] = 0.445

	def merge_sents(self):
		self.merge_comments([s.comments for s in self.sentences])
		self.count_weights()

	def merge_comments(all_comm):
		# checking that all comments are equal
		if all_comm[1:] == all_comm[:-1]:
			self.comments = self.sentences[0].comments
		else:
			# if the comments are not equal, choose the longest ones
			self.comments = max(all_comm, key=len)

	def count_weights():
		pass


if __name__ == '__main__':
	for blokk in input().split('\n\n'):
		if blokk.strip() == '': continue
		sent = Sentence(blokk)
		print(sent)
