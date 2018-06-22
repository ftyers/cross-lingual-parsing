import random
from conllu_parser import *


TREEBANKS = [
'fao_wiki.apertium.nob-fao.udpipe.projected.conllu',
'fao_wiki.apertium.nno-fao.udpipe.projected.conllu',
'first_half.conllu',
'fao_wiki.apertium.dan-fao.udpipe.projected.conllu'
]


def treebanks_dict():
	whole = {}
	for fname in TREEBANKS:
		with open('validated/' + fname) as f:
			sents = f.read().split('\n\n')
			# at this point, treebank has n sub-lists for each file,
			# where n is a number of treebank versions

			whole = one_treebank_dict(sents, whole)
	print(len(whole))
	return whole


def one_treebank_dict(sents, whole):
	for sent in sents:
		s = Sentence(sent)
		for comline in s.comments:
			if comline.startswith('# sent_id = '):
				num = int(comline.split('=')[1].strip())
				if num not in whole:
					whole[num] = [s]
				else:
					whole[num].append(s)
				break
	return whole


def random_union(tbs):
	result = []
	for num in tbs:
		sent = random.choice(tbs[num])
		result.append(str(sent))
	return result


def unite_treebanks(tbs):
	pass


	# treebank.append([Sentence(s) for s in sents])


if __name__ == '__main__':
	tbs = treebanks_dict()
	res = random_union(tbs)
	with open('random_union.conllu', 'w') as f:
		f.write('\n\n'.join(res))