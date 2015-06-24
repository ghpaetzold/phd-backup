

lex = open('../../../corpora/lexmturk/lexmturk.txt')

targets = set([])
for line in lex:
	data = line.strip().split('\t')
	target = data[1].strip()
	targets.add(target)
lex.close()

f = open('../../../corpora/substitutions/kauchak/all/final_substitutions.txt')
o = open('../../../corpora/substitutions/kauchak/substitutions.txt', 'w')
for line in f:
	data = line.strip().split('\t')
	if data[0].strip() in targets:
		o.write(line.strip() + '\n')
f.close()
o.close()
