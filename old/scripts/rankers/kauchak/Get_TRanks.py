import os

def getTranks(data, scores):
	testdata = {}
	index = 0
	for line in data:
		rank = line[0].strip()
		id = line[1].strip().split(':')[1].strip()
		word = line[len(line)-1]
		score = scores[index]
		index += 1
		if id in testdata.keys():
			testdata[id][rank+':'+word] = score
		else:
			testdata[id] = {rank+':'+word:score}

	total1 = 0
	total2 = 0
	total3 = 0
	corrects1 = 0
	corrects2 = 0
	corrects3 = 0
	for id in testdata.keys():
		candidates = testdata[id].keys()
		candidates = sorted(candidates, key=testdata[id].__getitem__, reverse=False)
		first = int(candidates[0].split(':')[0].strip())
		if first==1:
			corrects1 += 1
		total1 += 1
		if len(candidates)>2:
			if first<=2:
				corrects2 += 1
			total2 += 1
		if len(candidates)>3:
			if first<=3:
				corrects3 += 1
			total3 += 1
	return float(corrects1)/float(total1), float(corrects2)/float(total2), float(corrects3)/float(total3)

f = open('../corpora/features/features_semeval_test.txt')
data = []
for line in f:
	data.append(line.strip().split(' '))
f.close()

max = -1
maxvalues = None
rankings = os.listdir('../corpora/rankings/')
for ranking in rankings:
	print('At file ' + ranking)
	f = open('../corpora/rankings/' + ranking)
	scores = []
	for line in f:
		scores.append(float(line.strip()))
	f.close()
	trank1, trank2, trank3 = getTranks(data, scores)
	if trank1>max:
		max = trank1
		maxvalues = (trank1, trank2, trank3)

print('Max values:')
print('\tTrank1: ' + str(maxvalues[0]))
print('\tTrank2: ' + str(maxvalues[1]))
print('\tTrank3: ' + str(maxvalues[2]))
