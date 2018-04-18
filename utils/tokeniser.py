import sys, re

abbrs_in = [i.strip() for i in open(sys.argv[1]).readlines()]
abbr_i = 0
abbrs_to = {}
abbrs_from = {}
for i in abbrs_in:
	abbrs_to[i] = '@_' + str(abbr_i) + '_@'
	abbrs_from['@_' + str(abbr_i) + '_@'] = i
	abbr_i += 1

def tokenise(line, abbrs_to, abbrs_from):
	out = line
	for abbr in abbrs_to:
		out = out.replace(abbr, ' ' + abbrs_to[abbr] + ' ')

	for p in '!:,?;.()"“”':
		out = out.replace(p, ' ' + p + ' ')

	out = re.sub(r'([0-9]+) ([\.,:]) ([0-9]+) ([\.,:]) ([0-9]+)', r'\1\2\3\4\5', out)
	out = re.sub(r'([0-9]+) ([\.x,:]) ([0-9]+)', r'\1\2\3', out)
	out = re.sub(r'([0-9]+) \.', r'\1.', out)

	for abbr in abbrs_from:
		out = out.replace(abbr, abbrs_from[abbr])

	out = out.strip()

	out = re.sub('  *', ' ', out)

	return out	

for line in sys.stdin.readlines():
	line = tokenise(line, abbrs_to, abbrs_from)
	print(line.strip('\n'))
