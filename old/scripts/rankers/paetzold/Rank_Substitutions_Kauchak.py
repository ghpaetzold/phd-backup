from nltk.stem.porter import *
from tabulate import tabulate
import os
from nltk.corpus import wordnet as wn
import subprocess
import kenlm
from sklearn import linear_model

def getPrefixes():
        files = os.listdir('../../../corpora/substitutions/biran/')
        result = set([])
        for file in files:
                if file.startswith('substitutions'):
                        if len(file.split('.'))>2:
                                prefix = file.split('.')[1].strip()
                                result.add(prefix)
        return result

def calculateAlignmentProbabilities(data):
        stemmer = PorterStemmer()
        result = []
        f = open('../../../corpora/alignment_probabilities/alignment_probabilities_lexmturk.txt')
        probs = {}
        for line in f:
                datal = line.strip().split('\t')
                target = datal[0].strip()
                cand = datal[1].strip()
                prob = float(datal[2].strip())
                if target not in probs.keys():
                        probs[target] = {}
                probs[target][cand] = prob
        f.close()
        for line in data:
                target = stemmer.stem(line[1])
                for substu in line[3:len(line)]:
                        prob = 0.0
                        word = substu.split(':')[1].strip()
			subst = word
                        try:
				subst = stemmer.stem(word)
			except UnicodeDecodeError:
				subst = word
                        if target in probs.keys():
                                if subst in probs[target].keys():
                                        prob = probs[target][subst]
                        result.append(prob)
        #print('Len alignment probabilities: ' + str(len(result)))
        return result

def getSentenceProbability(data, lm):
    result = []
    model = kenlm.LanguageModel(lm)
    for line in data:
        sent = line[0]
        target = line[1]
        head = int(line[2])
        for subst in line[3:len(line)]:
            word = subst.split(':')[1].strip()
            ngram, bosv, eosv = getNgram(word, sent, head, 9999, 9999)
            aux = -1.0*model.score(ngram, bos=bosv, eos=eosv)
            result.append(aux)
    #print 'Len sent: ' + str(len(result))
    return result

def calculateKauchak(datate, X, clf, subs):
    total = 0
    totalc = 0
    precise = 0

    distances = clf.decision_function(X)
    index = 0
    for i in range(0, len(datate)):
	line = datate[i]
        tuples = []
        for subst in line[3:len(line)]:
            word = subst.strip().split(':')[1].strip()
            tuples.append((subst, distances[index]))
            index += 1
        tuples = sorted(tuples, reverse=True)
        tuples = sorted(tuples, key=lambda item: item[1], reverse=True)
        first = tuples[0][0].strip().split(':')[1].strip()

        total += 1
        if first!=subs[i][0]:
            totalc += 1
            if first in subs[i][1]:
                precise += 1

    if totalc == 0:
        totalc = 1
    if total == 0:
        print('PROBLEM!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        total = 1
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

def generateLabels(data, positive_range):
    Y = []

    for line in data:
        max_range = min(int(line[len(line)-1].split(':')[0].strip()), positive_range)
        for i in range(3, len(line)):
            rank_index = int(line[i].split(':')[0].strip())
            if rank_index<3+max_range:
                Y.append(1)
            else:
                Y.append(0)
    return Y

def getTestDataset(path, data):
	result = []
	f = open(path)
	for line in data:
		vec = [line[0], line[1], line[2], '1:'+line[1]]
		data = f.readline().strip().split('\t')
		subs = []
		if len(data)>1:
			subs = data[1].strip().split('|||')
			for sub in subs:
				if sub.strip()!=line[1].strip():
					vec.append('1:'+sub)
		result.append(vec)
	f.close()
	return result

def readFeatures(file):
    result = []
    f = open(file)
    for line in f:
        values = [float(v.strip()) for v in line.strip().split('\t')]
        result.append(values)
    f.close()
    return result

def calculateFeatures(data):
    X = []
    alignprobs = calculateAlignmentProbabilities(data)
    #lengths = calculateLenghts(data)
    #syllables = calculateSyllables(data)
    #senses, synonyms, hypernyms, hyponyms, mindepths, maxdepths = calculateSenseSynonymCounts(data)
    #basic = calculateBasics(data)
    #lmSubtlex = '../../../../machinelearningranking/corpora/lm/subtlex.5gram.bin.txt'
    lmSubimdb = '../../../../machinelearningranking/corpora/lm/subtleximdb.5gram.unk.bin.txt'
    lmSWikipedia = '/export/data/ghpaetzold/wordnetlmranking/corpora/corpus/simplewiki/lm/corpus.clean.3.bin.txt'
    lmWikipedia = '/export/data/ghpaetzold/wordnetlmranking/corpora/corpus/wiki/lm/corpus.clean.3.bin.txt'
    #colocSubtlex = getCollocationalFeatures(data, lmSubtlex, 4, 4)
    sentWikipedia = getSentenceProbability(data, lmWikipedia)
    sentSWikipedia = getSentenceProbability(data, lmSWikipedia)
    colocSubimdb = getCollocationalFeatures(data, lmSubimdb, 2, 2)
    colocSWikipedia = getCollocationalFeatures(data, lmSWikipedia, 0, 0)
    #lmdcWikipedia = '../../../../machinelearningranking/corpora/lm/oneperdoc.wiki.2.bin.txt'
    #lmdcSimpleWikipedia = '../../../../machinelearningranking/corpora/lm/oneperdoc.simplewiki.2.bin.txt'
    #lmdcSubimdb = '../../../../machinelearningranking/corpora/lm/oneperdoc.subimdb.2.bin.txt'
    #docCountsWikipedia = getCollocationalFeatures(data, lmdcWikipedia, 0, 0)
    #docCountsSimpleWikipedia = getCollocationalFeatures(data, lmdcSimpleWikipedia, 0, 0)
    #docCountsSubimdb = getCollocationalFeatures(data, lmdcSubimdb, 0, 0)

    feature_vector = [alignprobs, colocSubimdb, sentWikipedia, sentSWikipedia, colocSWikipedia]

    index = 0
    for line in data:
        for i in range(3, len(line)):
            rank_index = int(line[i].split(':')[0].strip())
            vector = generateVector(feature_vector, index)
            X.append(vector)
            index += 1
    return X

def generateVector(feature_vector, index):
    result = []
    for feature in feature_vector:
	if not isinstance(feature[index], list):
        	result.append(feature[index])
        else:
                result.extend(feature[index])
    return result

def getNgram(cand, sent, head, configl, configr):
    if configl==0 and configr==0:
        return cand, False, False
    else:
        result = ''
        tokens = sent.strip().split(' ')
        bosv = False
        if max(0, head-configl)==0:
            bosv = True
        eosv = False
        if min(len(tokens), head+configr+1)==len(tokens):
            eosv = True
        for i in range(max(0, head-configl), head):
            result += tokens[i] + ' '
        result += cand + ' '
        for i in range(head+1, min(len(tokens), head+configr+1)):
            result += tokens[i] + ' '
#        print 'Original sent: ' + sent
#        print 'Generated ngram: ' + result.strip() + ', ' + str(bosv) + ', ' + str(eosv)
        return result.strip(), bosv, eosv

def getCollocationalFeatures(data, lm, spanl, spanr):
    result = []
    model = kenlm.LanguageModel(lm)
    for line in data:
        sent = line[0]
        target = line[1]
        head = int(line[2])
        spanlv = range(0, spanl+1)
        spanrv = range(0, spanr+1)
        for subst in line[3:len(line)]:
            word = subst.split(':')[1].strip()
            values = []
            for span1 in spanlv:
                for span2 in spanrv:
                    ngram, bosv, eosv = getNgram(word, sent, head, span1, span2)
                    aux = -1.0*model.score(ngram, bos=bosv, eos=eosv)
                    values.append(aux)
            result.append(values)
    #print 'Len collocational: ' + str(len(result))
    return result

def calculateBasics(data):
    result = []
    basics = [w.strip() for w in open('../../../corpora/basic_words/basic_words.txt')]
    for line in data:
        for subst in line[3:len(line)]:
            words = subst.strip().split(':')[1].strip()
            basicCount = 0
            for word in words.split(' '):
                if word.strip() in basics:
                    basicCount += 1
            if basicCount==len(words.split(' ')):
                result.append(1.0)
            else:
                result.append(0.0)
    #print 'Len basics: ' + str(len(result))
    return result

def calculateSenseSynonymCounts(data):
    resultse = []
    resultsy = []
    resulthe = []
    resultho = []
    resultmi = []
    resultma = []
    for line in data:
        for subst in line[3:len(line)]:
            words = subst.strip().split(':')[1].strip()
            sensec = 0
            syncount = 0
            hypernyms = set([])
            hyponyms = set([])
            mindepth = 9999999
            maxdepth = -1
            for word in words.split(' '):
                senses = wn.synsets(word)
                sensec += len(senses)
                for sense in senses:
                    auxmin = sense.min_depth()
                    auxmax = sense.max_depth()
                    if auxmin<mindepth:
                        mindepth = auxmin
                    if auxmax>maxdepth:
                        maxdepth = auxmax
                    syncount += len(sense.lemmas())
                    hypernyms.update(sense.hypernyms())
                    hyponyms.update(sense.hyponyms())
            resultse.append(sensec)
            resultsy.append(syncount)
            resulthe.append(len(hypernyms))
            resultho.append(len(hyponyms))
            resultmi.append(mindepth)
            resultma.append(maxdepth)
    #print 'Len senses: ' + str(len(resultse))
    #print 'Len synonyms: ' + str(len(resultsy))
    #print 'Len hypernyms: ' + str(len(resulthe))
    #print 'Len hyponyms: ' + str(len(resultho))
    #print 'Len min depth: ' + str(len(resultmi))
    #print 'Len max depth: ' + str(len(resultma))
    return resultse, resultsy, resulthe, resultho, resultmi, resultma

def calculateSyllables(data):
    #Create the input for the Java application:
    input = ''
    counter = 0
    for line in data:
        for subst in line[3:len(line)]:
            counter += 1
            word = subst.strip().split(':')[1].strip()
            input += word + '\n'
    input += '\n'

    #Run the syllable splitter:
    java = 'java'
    path = '/export/tools/adorner-tools/SyllableSplitter.jar'
    p = subprocess.Popen([java, '-jar', path, input], stdout=subprocess.PIPE)
    out, err = p.communicate()

    #Decode output:
    out = out.decode("latin1")
    out = out.replace(' ', '-').split('\n')

    #Calculate number of syllables
    result = []
    for instance in out:
        if len(instance.strip())>0:
            result.append(len(instance.split('-')))
    #print 'Len syllables: ' + str(len(result))
    return result


def calculateLenghts(data):
    result = []
    for line in data:
        for subst in line[3:len(line)]:
            word = subst.strip().split(':')[1].strip()
            result.append(len(word))
    #print 'Len lengths: ' + str(len(result))
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

#Set positive range:
positive_range = 1

#Calculate training feature values:
Xtr = readFeatures('training_features_kauchak.txt')
Ytr = generateLabels(raw_training_features, positive_range)





methods = ['all', 'biran', 'kauchak', 'merriam', 'wordnet', 'yamamoto']
prefixes = getPrefixes()

for method in methods:
	print('For method ' + method + ':')
	table = [['Sel. Method', 'Precision', 'Accuracy', 'Changed']]
	for prefix in prefixes:

		#Get formatted target dataset:
		path = '../../../corpora/substitutions/'+method+'/substitutions.'+prefix+'.txt'
		raw_testing_features = getTestDataset(path, raw_training_features)
		
		#Calculate testing feature values:
		Xte = calculateFeatures(raw_testing_features)
		Yte = generateLabels(raw_testing_features, positive_range)

		#print('--------------------------------------------------------------------------------------------------------------')
		
		#print('\nFor the linear classifier:')
		#SGD parameters:
		losses = ['hinge', 'log', 'modified_huber', 'squared_hinge', 'perceptron']
		#losses = ['modified_huber']
		penalties = ['l2', 'l1', 'elasticnet']
		#alphas = [0.0005, 0.0007, 0.001, 0.01, 0.1]
		alphas = [0.001, 0.01, 0.1]
		#l1ratios = [0.001, 0.01, 0.05, 0.10, 0.15]
		l1ratios = [0.001, 0.10, 0.15]
		#epsilons = [0.00001, 0.0001, 0.0005, 0.0007, 0.001]
		epsilons = [0.00001, 0.0001, 0.001]
		#Maximum variables:
		maxv = -1
		maxvalues = None
		maxloss = None
		maxpenalty = None
		maxalpha = None
		maxl1 = None
		maxepsilon = None
		for l in losses:
			for p in penalties:
				for a in alphas:
					for r in l1ratios:
						for e in epsilons:
							#Train the SGD classifier:
							clf = linear_model.SGDClassifier(loss=l, penalty=p, alpha=a, l1_ratio=r, epsilon=e)
							try:
								clf.fit(Xtr, Ytr)
								#Score the classifier:
								precision, accuracy, change = calculateKauchak(raw_testing_features, Xte, clf, training_subs)
								if precision>maxv:
									maxv = precision
									maxvalues = [precision, accuracy, change]
							except ValueError:
								aux = 0
		
		table.append([prefix, maxvalues[0], maxvalues[1], maxvalues[2]])
	print(tabulate(table))
	print('')
