"""
Takes a treebank as input.
Creates a directory 'validated' and puts there only those sentences of
the treebank which are valid.
"""
import sys
import os
from conllu_parser import Sentence

def validate(treebank):
	print('treebank: ' + str(len(treebank)))
	doubled = []
	missing = []
	valid = []
	for s in treebank:
		ids = [int(t[0]) for t in s.tokens]
		if len(set(ids)) != len(ids):
			doubled.append(s)
			# print('doubled:\n')
			# print(s)
		elif len(ids) < ids[-1]:
			# print('missing:\n')
			# print(s)
			missing.append(s)
		else:
			valid.append(s)
	print('doubled: ' + str(len(doubled)))
	print('missing: ' + str(len(missing)))
	print('valid: ' + str(len(valid)))
	return valid


def main():
	with open(sys.argv[1]) as f:
		sents = f.read().split('\n\n')
		treebank = [Sentence(s) for s in sents if s]
	treebank = validate(treebank)
	# print(treebank)
	if not os.path.exists('validated'):
		os.mkdir('validated')
	with open('validated/' + sys.argv[1].split('/')[-1], 'w') as f:
		f.write('\n\n'.join(str(s) for s in treebank))


if __name__ == '__main__':
	main()
