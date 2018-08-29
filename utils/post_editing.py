import sys


ud = open(sys.argv[1], 'r').readlines()
# ud = open('cross_lingual_results.txt', 'r').readlines()

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



def get_ids(sent):
	sent_arr_first = []
	sent_arr_second = []
	for i in range(1, len(sent)):
		sent_arr_first.append(sent[i][0])
		sent_arr_second.append(int(sent[i][6]))
	# print(sent_arr_first)
	# print(sent_arr_second)
	return(sent_arr_first, sent_arr_second)


def change_ids(sent):
	d_1 = {}
	d_2 = {}
	sent_1, sent_2 = get_ids(sent)
	for i in range(1, len(sent_1)+1):
		d_1[sent_1[i-1]] = i

	if max(sent_2) > len(sent_1):
		# print(max(sent_2), min(sent_2))
		difrnc = max(sent_2) - len(sent_1)
		for n in sent_2:
			new_n = n - difrnc
			if new_n <= 0:
				d_2[str(n)] = n
				# print('LOL')
			else:
				d_2[str(n)] = new_n
				# print('thats niice')
	# print(d_1)
	# print(d_2)
	# print(len(d_2), len(sent_2))
	return(d_1, d_2)


def main(ud):
	file = sys.stdout
	file.write('# newdoc\n')
	file.write('# newpar\n')
	j = 1
	for sent in ud_parse(ud):
		
		file.write('# sent_id = ' + str(j) + '\n')
		file.write(sent[0][0] + '\n')
		j += 1
		d_ids, d_2 = change_ids(sent)
		for i in range(1, len(sent)):
			sent[i][0] = str(i)
			try:
				sent[i][6] = str(d_ids[sent[i][6]])
			except KeyError:
				pass

			try:
				sent[i][6] = str(d_2[sent[i][6]])
			except KeyError:
				pass

			file.write('\t'.join(sent[i]) + '\n')
		file.write('\n')


main(ud)