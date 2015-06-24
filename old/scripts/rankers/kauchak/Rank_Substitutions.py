from tabulate import tabulate
import os

def getTranks(data, scores):
        testdata = {}
        index = 0
        for line in data:
                rank = line[0].strip()
                id = int(line[1].strip().split(':')[1].strip())
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

def getKauchak(training_subs, data_test, scores):
	testdata = {}
	index = 0
	firsts = {}
	for line in data_test:
		rank = line[0].strip()
		id = int(line[1].strip().split(':')[1].strip())
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
	for id in sorted(testdata.keys()):
		instance_data = training_subs[id-1]
		candidates = testdata[id].keys()
		candidates = sorted(candidates, key=testdata[id].__getitem__, reverse=False)
		first = candidates[0].split(':')[1].strip()

		total += 1
		if first!=instance_data[0]:
			totalc += 1
			if first in instance_data[1]:
				precise += 1

	if totalc == 0:
		totalc = 1
	return float(precise)/float(totalc), float(precise)/float(total), float(totalc)/float(total)

def getSubs(data):
        result = []
        for line in data:
                target = line[1].strip()
                vec = set([])
                for sub in line[3:len(data)]:
                        cand = sub.strip().split(':')[1].strip()
                        vec.add(cand)
                result.append((target, vec))
        return result

def getPrefixes():
        files = os.listdir('../../../corpora/substitutions/biran/')
        result = set([])
        for file in files:
                if file.startswith('substitutions'):
                        if len(file.split('.'))>2:
                                prefix = file.split('.')[1].strip()
                                result.add(prefix)
        return result

#Training input and output files:
ftrainin = open('../../../corpora/lexmturk/lexmturk_all.txt', 'r')

#Read each line of training dataset:
raw_training_features = []
for line in ftrainin:
	raw_training_features.append(line.strip().split('\t'))
ftrainin.close()

#Get training subs:
training_subs = getSubs(raw_training_features)

methods = ['all', 'biran', 'kauchak', 'merriam', 'wordnet', 'yamamoto']
prefixes = getPrefixes()

max = -1
maxvalues = None
for method in methods:
        print('For method ' + method + ':')
	table = [['Sel. Method', 'Precision', 'Accuracy', 'Changed']]
        for prefix in prefixes:
		f = open('./features/test/features.'+method+'.'+prefix+'.txt')
		data_test = []
		for line in f:
			data_test.append(line.strip().split(' '))
		f.close()

		f = open('./rankings/test/rankings.' + method + '.' + prefix + '.txt')
		scores = []
		for line in f:
			scores.append(float(line.strip()))
		f.close()
		precision, accuracy, changed = getKauchak(training_subs, data_test, scores)
		table.append([prefix, precision, accuracy, changed])
        print(tabulate(table))
        print('')

