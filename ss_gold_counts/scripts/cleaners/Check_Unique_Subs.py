f = open('../../corpora/lexmturk_gold_test.txt')
cs = open('../../corpora/lexmturk_gold_counts_test.txt')
for line in f:
	data = line.strip().split('\t')
	cands = data[3:len(data)]
	candsc = [c.split(':')[1].strip() for c in cands]

	gcounts = int(cs.readline().strip())

	if len(cands)!=gcounts:
		print('problem')
	if len(candsc)!=gcounts:
		print('treta')
	
	myset = set([])
	for i in range(0, len(cands)):
		if candsc[i] in myset:
			print('Problem at: ' + cands[i])
			print('Sentence: ' + line.strip())
		else:
			myset.add(candsc[i])

	scands = set(candsc)
	if len(candsc)!=len(scands):
		print('Problem is found forever')
f.close()
