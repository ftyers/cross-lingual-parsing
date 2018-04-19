import sys

out = ''
for line in sys.stdin.readlines():

	if line.strip() == '': 
		print(out.strip())
		out = ''
		continue
	if line[0] == '#': continue
	row = line.split('\t')
	if row[0].count('.') > 0: continue
	
	# probably do something with spans
	if row[0].count('-') > 0: continue

	out += row[1] + ' '
