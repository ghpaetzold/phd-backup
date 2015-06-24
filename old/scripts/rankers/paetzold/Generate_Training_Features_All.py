from nltk.stem.porter import *
from nltk.corpus import wordnet as wn
import subprocess
import kenlm

def calculateFeatures(data):
    X = []
    alignprobs = calculateAlignmentProbabilities(data)
    lengths = calculateLenghts(data)
    syllables = calculateSyllables(data)
    senses, synonyms, hypernyms, hyponyms, mindepths, maxdepths = calculateSenseSynonymCounts(data)
    basic = calculateBasics(data)
    lmSubtlex = '../../../../machinelearningranking/corpora/lm/subtlex.5gram.bin.txt'
    lmSubimdb = '../../../../machinelearningranking/corpora/lm/subtleximdb.5gram.unk.bin.txt'
    lmSWikipedia = '/export/data/ghpaetzold/wordnetlmranking/corpora/corpus/simplewiki/lm/corpus.clean.3.bin.txt'
    lmWikipedia = '/export/data/ghpaetzold/wordnetlmranking/corpora/corpus/wiki/lm/corpus.clean.3.bin.txt'
    sentWikipedia = getSentenceProbability(data, lmWikipedia)
    sentSWikipedia = getSentenceProbability(data, lmSWikipedia)
    colocSubtlex = getCollocationalFeatures(data, lmSubtlex, 2, 2)
    colocSubimdb = getCollocationalFeatures(data, lmSubimdb, 2, 2)
    colocSWikipedia = getCollocationalFeatures(data, lmSWikipedia, 2, 2)
    lmdcWikipedia = '../../../../machinelearningranking/corpora/lm/oneperdoc.wiki.2.bin.txt'
    lmdcSimpleWikipedia = '../../../../machinelearningranking/corpora/lm/oneperdoc.simplewiki.2.bin.txt'
    lmdcSubimdb = '../../../../machinelearningranking/corpora/lm/oneperdoc.subimdb.2.bin.txt'
    docCountsWikipedia = getCollocationalFeatures(data, lmdcWikipedia, 0, 0)
    docCountsSimpleWikipedia = getCollocationalFeatures(data, lmdcSimpleWikipedia, 0, 0)
    docCountsSubimdb = getCollocationalFeatures(data, lmdcSubimdb, 0, 0)
    
    feature_vector = [alignprobs, lengths, syllables, senses, synonyms, hypernyms, hyponyms, mindepths, maxdepths]
    feature_vector.extend([basic, colocSubtlex, colocSubimdb, colocSWikipedia, sentWikipedia, sentSWikipedia])
    feature_vector.extend([docCountsWikipedia, docCountsSimpleWikipedia, docCountsSubimdb])

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
			subst = stemmer.stem(word) 
			if target in probs.keys():
				if subst in probs[target].keys():
					prob = probs[target][subst]
			result.append(prob)
	print('Len alignment probabilities: ' + str(len(result)))
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
    print 'Len sent: ' + str(len(result))
    return result


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
                    if span1==0 and span2==0:
                        aux = -1.0*model.score(ngram, bos=False, eos=False)
                        aux += -1.0*model.score(ngram, bos=False, eos=True)
                        aux += -1.0*model.score(ngram, bos=True, eos=False)
                        aux += -1.0*model.score(ngram, bos=True, eos=True)
                        values.append(aux)
                    else:
                        aux = -1.0*model.score(ngram, bos=bosv, eos=eosv)
                        values.append(aux)
            result.append(values)
    print 'Len collocational: ' + str(len(result))
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
    print 'Len basics: ' + str(len(result))
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
    print 'Len senses: ' + str(len(resultse))
    print 'Len synonyms: ' + str(len(resultsy))
    print 'Len hypernyms: ' + str(len(resulthe))
    print 'Len hyponyms: ' + str(len(resultho))
    print 'Len min depth: ' + str(len(resultmi))
    print 'Len max depth: ' + str(len(resultma))
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
    print 'Len syllables: ' + str(len(result))
    return result


def calculateLenghts(data):
    result = []
    for line in data:
        for subst in line[3:len(line)]:
            word = subst.strip().split(':')[1].strip()
            result.append(len(word))
    print 'Len lengths: ' + str(len(result))
    return result

































#Training input and output files:
ftrainin = open('../../../corpora/lexmturk/lexmturk_all.txt', 'r')
ftrainout = open('./features/training_features_all.txt', 'w')

#Testing input and output files:
#ftestin = open('../../corpora/semeval/semeval_test_gold_formatted.txt', 'r')
#ftestout = open('../../corpora/features/features_semeval_test_subtleximdb.txt', 'w')

#Read each line of training dataset:
raw_training_features = []
for line in ftrainin:
    raw_training_features.append(line.strip().split('\t'))
ftrainin.close()

#Read each line of testing dataset:
#raw_testing_features = []
#for line in ftestin:
#    raw_testing_features.append(line.strip().split('\t'))
#ftestin.close()

#Calculate training feature values:
features_train = calculateFeatures(raw_training_features)

#Calculate testing feature values:
#features_test = calculateFeatures(raw_testing_features)

#Save training feature file:
for line in features_train:
	values = ''
	for v in line:
		values += str(v) + '\t'
	ftrainout.write(str(values.strip()) + '\n')
ftrainout.close()

#Save testing feature file:
#for line in features_test:
#        values = ''
#        for v in line:
#                values += str(v) + '\t'
#        ftestout.write(str(values.strip()) + '\n')
#ftestout.close()
