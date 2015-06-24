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

def getKauchak(data, scores):
	testdata = {}
	index = 0
	firsts = {}
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
		if rank=='1':
			firsts[id] = word

	totalc = 0
	total = 0
	precise = 0
	for id in testdata.keys():
		candidates = testdata[id].keys()
		candidates = sorted(candidates, key=testdata[id].__getitem__, reverse=False)
		first = candidates[0].split(':')[1].strip()

		total += 1
		if first!=firsts[id]:
			totalc += 1
			precise += 1

	if totalc == 0:
		totalc = 1
	return float(precise)/float(totalc), float(precise)/float(total), float(totalc)/float(total)


f = open('./features/train/training_features.txt')
data = []
for line in f:
	data.append(line.strip().split(' '))
f.close()

max = -1
maxvalues = None
bestmodel = ''
rankings = os.listdir('./rankings/train/')
for ranking in rankings:
	print('At file ' + ranking)
	f = open('./rankings/train/' + ranking)
	scores = []
	for line in f:
		scores.append(float(line.strip()))
	f.close()
	trank1, trank2, trank3 = getKauchak(data, scores)
	if trank2>max:
		max = trank2
		maxvalues = (trank1, trank2, trank3)
		bestmodel = ranking

print('Max values:')
print('\tPrecision: ' + str(maxvalues[0]))
print('\tAccuracy: ' + str(maxvalues[1]))
print('\tChanged: ' + str(maxvalues[2]))
print('Best: ' + bestmodel)
