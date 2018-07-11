import random
from conllu_parser import *


TREEBANKS = [
'fao_wiki.apertium.nob-fao.udpipe.projected.conllu',
'fao_wiki.apertium.nno-fao.udpipe.projected.conllu',
'fao_wiki.apertium.swe-fao.udpipe.projected.conllu',
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
	print('uniuon: ' + str(len(whole)))
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


def fast_write_3_4(whole):
	three_sents = [[], [], []]
	four_sents = [[], [], [], []]
	for num in whole:
		sents = whole[num]
		if len(sents) == 3:
			three_sents[0].append(str(sents[0]))
			three_sents[1].append(str(sents[1]))
			three_sents[2].append(str(sents[2]))
		elif len(sents) == 4:
			four_sents[0].append(str(sents[0]))
			four_sents[1].append(str(sents[1]))
			four_sents[2].append(str(sents[2]))
			four_sents[3].append(str(sents[3]))
	print('three_sents: ' + str(len(three_sents[0])))
	print('four_sents: ' + str(len(four_sents[0])))
	with open('tmp/three_1st.conllu', 'w') as f:
		f.write('\n\n'.join(three_sents[0]))
	with open('tmp/three_2nd.conllu', 'w') as f:
		f.write('\n\n'.join(three_sents[1]))
	with open('tmp/three_3rd.conllu', 'w') as f:
		f.write('\n\n'.join(three_sents[2]))
	with open('tmp/four_1st.conllu', 'w') as f:
		f.write('\n\n'.join(four_sents[0]))
	with open('tmp/four_2nd.conllu', 'w') as f:
		f.write('\n\n'.join(four_sents[1]))
	with open('tmp/four_3rd.conllu', 'w') as f:
		f.write('\n\n'.join(four_sents[2]))
	with open('tmp/four_4th.conllu', 'w') as f:
		f.write('\n\n'.join(four_sents[3]))


if __name__ == '__main__':
	union = treebanks_dict()
	fast_write_3_4(union)

	# tbs = treebanks_dict()
	# res = random_union(tbs)
	# with open('random_union.conllu', 'w') as f:
	# 	f.write('\n\n'.join(res))
