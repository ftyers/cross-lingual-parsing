import sys


# for example, python3 ud-parser.py fast_align_res.txt ud_results.txt de-ru.txt
# align = open(sys.argv[-3], 'r').readlines()
# ud = open(sys.argv[-2], 'r').readlines()
# corpora = open(sys.argv[-1], 'r').readlines()


align = open('align_res.txt', 'r').readlines()
ud = open('ud_res.txt', 'r').readlines()
corpora = open('yiddish_german_google_cleared_01.txt', 'r').readlines()


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
	# print(align)
	for i in ud_indexes:
		# print(i)
		# print(d)
		if i in point:
			continue
		try:
			if before_zum == 0:
				# print(i)
				d[int(i)-1] = align[int(i)-2]
		
			if '-' in i:
				before_zum = False
				zum = i.split('-')
				for j in range(int(zum[0]), int(zum[1])+1):					
					d[j-1] = align[j-1]	
				before_zum = 0
				point += i

			if before_zum is True:
				d[int(i)-1] = align[int(i)-1]
		except KeyError:
			continue
	# print('ALIGN RESULT ZUM', d)
	return d


# this function go thru each word in sentence
def transfer_tree(i, source_indexes, align_sent, ud_sent, corpora_sent, file):
	for j in range(0, len(source_indexes)):

		if '-' in ud_sent[j+1][0]:
			continue

		try:
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
		except KeyError:
			continue

	file.write('\n') 


def test(i, source_indexes, align_sent, ud_sent, corpora_sent, file):
	print(align_sent)
	for j in range(0, len(source_indexes)):
		if '-' in ud_sent[j+1][0]:
			continue
		
		try:
			print(int(ud_sent[j+1][0])-1, align_sent[int(ud_sent[j+1][0])-1])
		except KeyError:
			continue

		


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

		source_indexes = [ud_res[i][j+1][0] for j in range(0, len(ud_res[i])-1)]
		# print(source_indexes)

		if '-' in ''.join(source_indexes):
			# print('ALIGN RESULT', align_res[i])
			transfer_tree(i, source_indexes, zum_align(align_res[i], source_indexes), ud_res[i], corpora_res[i], file)
		else:
			# print('ALIGN RESULT', align_res[i])
			transfer_tree(i, source_indexes, align_res[i], ud_res[i], corpora_res[i], file)


main(align, ud, corpora)