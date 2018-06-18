import re

# corpora = open('fao_wiki.apertium.swe-fao.input.txt', 'r').readlines()
corpora = open('fao_wiki.apertium.nob-fao.input.txt', 'r').readlines()
result = open('fao_wiki.apertium.nob-fao.input-1.txt', 'a')

punct = [',', '!', '"', "'", ':', ';']

for line in corpora:
	# print(line)

	line = re.sub('(\w\w+)\. ', '\\1 . ', line)
	line = re.sub('\.$', ' .', line)
	line = re.sub('\?', ' ?', line)
	# line = re.sub('!', ' !', line)
	for p in punct:
		p1 = ' ' + p
		line = re.sub(p, p1, line)
	result.write(line)