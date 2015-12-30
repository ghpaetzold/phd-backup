f = open('../../corpora/cwi_paetzold_testing.txt')
answers = {}
words = []
for line in f:
	data = line.strip().split('\t')
	word = data[1].strip()
	words.append(word)
	label = data[3].strip()
	if word not in answers:
		answers[word] = set([])
	answers[word].add(label)
f.close()

labels = {}
f = open('../../labels/voting/labels_voting_8_True.txt')
c = -1
for line in f:
	c += 1
	label = line.strip()
        word = words[c]
	if word not in labels:
		labels[word] = set([])
	labels[word].add(label)
f.close()

for word in answers:
	ans = answers[word]
	lab = labels[word]
	if len(ans)==1:
		diff = lab.difference(ans)
		if len(diff)>0:
			print('\nProblem with: ' + word)
			print('Answers: ' + str(ans))
			print('Labels: ' + str(lab))
