import re
import os

align_sents = open('fast_align_res.txt', 'r')
align = align_sents.readlines()

ud_pipe = open('ud_results.txt', 'r')
ud = ud_pipe.readlines()

parpall_corpora = open('de-ru.txt', 'r')
corpora = parpall_corpora.readlines()

sents = re.findall('sent_id.*newpar?', 'ud')



def corpora_arr(corpora):
	arr = []
	for line in corpora:
		de_ru = [l.split() for l in line.replace('\n', '').split('|||')]
		arr.append(de_ru)
	return arr


def align_arr(align):
	arr = []
	for line in align:
		d = {}
		for pattern in ([word.split('-') for word in line.replace('\n', '').split()]):
			d[int(pattern[0])] = int(pattern[1])
		arr.append(d)
	return arr


def ud_parse(ud):
	doc = []
	sentense = []
	new_sent = False
	for line in ud:
		if line == '\n':
			new_sent = False
			doc.append(sentense)
			sentense = []
		if new_sent == True:
			sentense.append(line.replace('\n', '').split('	'))
		if 'sent_id' in line:
			new_sent = True
	return(doc)


def main():
	file = open('cross_lingual_results.txt','a')

	align_res = align_arr(align)
	ud_res = ud_parse(ud)
	corpora_res = corpora_arr(corpora)

	file.write('# newdoc\n')

	for i in range(0, len(align_res)):

		file.write('# newpar\n')	
		file.write('# sent_id = ' + str(i+1) + '\n')
		file.write('# text = ' + ' '.join(corpora_res[i][1]) + '\n')

		for j in range(0, len(align_res[i])):
			ud_res[i][j+1][0] = str(align_res[i][int(ud_res[i][j+1][0])-1] + 1)
			if int(ud_res[i][j+1][6]) != 0:
				ud_res[i][j+1][6] = str(align_res[i][int(ud_res[i][j+1][6])-1] + 1)
			ud_res[i][j+1][1] = corpora_res[i][1][int(ud_res[i][j+1][0])-1]
			if ud_res[i][j+1][2] != '.':
				ud_res[i][j+1][2] = '_'

			file.write('	'.join(ud_res[i][j+1]) + '\n')

	file.close() 



main()






