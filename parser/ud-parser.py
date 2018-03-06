import sys


# for example, python3 ud-parser.py fast_align_res.txt ud_results.txt de-ru.txt
align = open(sys.argv[-3], 'r').readlines()
ud = open(sys.argv[-2], 'r').readlines()
corpora = open(sys.argv[-1], 'r').readlines()


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


def zum_align(align, ud_indexes):
	d = {}
	point = ''
	before_zum = True
	for i in ud_indexes:
		if i in point:
			continue
		try:
			if before_zum == 0:
				# print(i)
				d[int(i)-1] = align[int(i)-2]
		except KeyError:
			continue
		if '-' in i:
			before_zum = False
			zum = i.split('-')	
			d[int(zum[0])-1] = align[int(zum[0])-1]
			d[int(zum[1])-1] = align[int(zum[0])-1]
			before_zum = 0
			point += i
		if before_zum is True:
			d[int(i)-1] = align[int(i)-1]
	return d


# this function go thru each word in sentence
def transfer_tree(i, align_sent, ud_sent, corpora_sent, file):
	for j in range(0, len(align_sent)):
		if '-' in ud_sent[j+1][0]:
			continue

		ud_sent[j+1][0] = str(align_sent[int(ud_sent[j+1][0])-1] + 1)
		if int(ud_sent[j+1][6]) != 0:
			ud_sent[j+1][6] = str(align_sent[int(ud_sent[j+1][6])-1] + 1)
		ud_sent[j+1][1] = corpora_sent[1][int(ud_sent[j+1][0])-1]
		if ud_sent[j+1][2] != '.':
			ud_sent[j+1][2] = '_'

		# discard XPOS and FEATS for now
		ud_sent[j+1][4] = '_' 
		ud_sent[j+1][5] = '_'
		file.write('\t'.join(ud_sent[j+1]) + '\n')
	file.write('\n') 


# this function go thru each sentence
def main(align, ud, corpora):
	# file = open('cross_lingual_results.txt','a')
	file = sys.stdout

	align_res = align_arr(align)
	ud_res = ud_parse(ud) 
	corpora_res = corpora_arr(corpora) 
	file.write('# newdoc\n')

	for i in range(0, len(align_res)):
		file.write('# newpar\n')	
		file.write('# sent_id = ' + str(i+1) + '\n')
		file.write('# text = ' + ' '.join(corpora_res[i][1]) + '\n')

		germ_indexes = [ud_res[i][j+1][0] for j in range(0, len(ud_res[i])-1)]

		if '-' in ''.join(germ_indexes):
			transfer_tree(i, zum_align(align_res[i], germ_indexes), ud_res[i], corpora_res[i], file)
		else:
			transfer_tree(i, align_res[i], ud_res[i], corpora_res[i], file)


main(align, ud, corpora)