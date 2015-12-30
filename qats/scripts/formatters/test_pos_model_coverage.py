import pickle

condprob_model = '/export/data/ghpaetzold/LEXenstein/corpora/POS_condprob_model.bin'
m = pickle.load(open(condprob_model, 'rb'))

words = set([])
f = open('../../corpora/s1s.tok.txt')
for line in f:
	words.update(line.strip().split(' '))
f.close()
f = open('../../corpora/s2s.tok.txt')
for line in f:
	words.update(line.strip().split(' '))
f.close()

print(str(len(words)))

covered = set([])
for word in words:
	if word in m or word.lower() in m:
		covered.add(word)

print(str(len(covered)))

diff = words.difference(covered)
for d in diff:
	print(d)
