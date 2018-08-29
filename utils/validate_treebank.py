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
	wrong_order = []
	wrong_start = []
	too_large_head = []
	for s in treebank:
		ids = [int(t[0]) for t in s.tokens]
		heads = [int(t[6]) for t in s.tokens]
		if len(set(ids)) != len(ids):
			doubled.append(s)
			# print('doubled:\n')
			# print(s)
		elif ids[0] != 1:
			wrong_start.append(s)
		elif len(ids) < ids[-1]:
			# print('missing:\n')
			# print(s)
			missing.append(s)
		elif ids != list(sorted(ids)):
			wrong_order.append(s)
		elif max(heads) > max(ids):
			too_large_head.append(s)
		else:
			valid.append(s)
	print('doubled: ' + str(len(doubled)))
	print('missing: ' + str(len(missing)))
	print('wrong_order: ' + str(len(wrong_order)))
	print('wrong_start: ' + str(len(wrong_start)))
	print('too_large_head: ' + str(len(too_large_head)))
	# for item in too_large_head:
	# 	print(item)
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
	with open('validated/' + sys.argv[1].split('/')[-1], 'w', encoding='utf-8') as f:
		f.write('\n\n'.join(str(s) for s in treebank))


if __name__ == '__main__':
	main()
