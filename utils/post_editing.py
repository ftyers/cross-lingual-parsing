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
	sent_arr = []
	for i in range(1, len(sent)):
		sent_arr.append(sent[i][0])
	return(sent_arr)


def change_ids(sent):
	d = {}
	sent = get_ids(sent)
	for i in range(1, len(sent)+1):
		d[sent[i-1]] = i
	return(d)


def main(ud):
	file = sys.stdout
	file.write('# newdoc\n')
	file.write('# newpar\n')
	j = 1
	for sent in ud_parse(ud):
		
		file.write('# sent_id = ' + str(j) + '\n')
		file.write(sent[0][0] + '\n')
		j += 1
		d_ids = change_ids(sent)
		for i in range(1, len(sent)):
			sent[i][0] = str(i)
			try:
				sent[i][6] = str(d_ids[sent[i][6]])
			except KeyError:
				pass
			file.write('\t'.join(sent[i]) + '\n')
		file.write('\n')


main(ud)