def createSent(tokens, head, word):
	newsent = ''
	for i in range(0, head):
		newsent += tokens[i] + ' '
	newsent += word + ' '
	for i in range(head+1, len(tokens)):
		newsent += tokens[i] + ' '
	return newsent.strip()

f = open('/export/data/ghpaetzold/benchmarking/lexmturk/corpora/lexmturk_all.txt')
o = open('../../corpora/lexmturk_valid.txt', 'w')

for line in f:
	data = line.strip().split('\t')
	o.write(data[0].strip() + '\n')
	tokens = data[0].strip().split(' ')
	target = data[1].strip()
	head = int(data[2].strip())
	cands = data[3:]
	for cand in cands:
		candd = cand.strip().split(':')
		label = candd[0]
		word = candd[1]
		newsent = createSent(tokens, head, word)
		print(newsent)
		o.write(newsent + '\n')
f.close()
o.close()
