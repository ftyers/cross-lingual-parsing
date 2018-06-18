fao = open('fao_wiki.txt', 'r').readlines()
xxx = open('fao_wiki.apertium.nob-swe.txt', 'r').readlines()


new_align = open('fao_wiki.apertium.swe-fao.input.txt','a')

for x, f in zip(xxx, fao):
	x.replace('\n', '')
	print(x + ' ||| ' + f)
	new_align.write(x.replace('\n', '') + ' ||| ' + f)