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
	print(len(whole))
	trnum = 0
	tnum = 0
	for num in whole:
		if len(whole[num]) == 3:
			trnum += 1
		elif len(whole[num]) == 2:
			tnum += 1
	print(trnum)
	print(tnum)


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


def unite_treebanks(tbs):
	pass


	# treebank.append([Sentence(s) for s in sents])


if __name__ == '__main__':
	treebanks_dict()