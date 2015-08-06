from lexenstein.morphadorner import *
from lexenstein.identifiers import *
from lexenstein.features import *
import sys

train_victor_corpus = sys.argv[1]
k = sys.argv[2].strip()
if k!='all':
        k = int(sys.argv[2].strip())
loss = sys.argv[3].strip()
penalty = sys.argv[4].strip()
alpha = float(sys.argv[5].strip())
l1_ratio = float(sys.argv[6].strip())
epsilon = float(sys.argv[7].strip())
test_victor_corpus = sys.argv[8].strip()
out_file = sys.argv[9].strip()

def getTaggedSents(corpus):
        result = []
        f = open(corpus)
        for line in f:
                tags = []
                tokens = line.strip().split(' ')
                for token in tokens:
                        tokendata = token.strip().split('|||')
                        tags.append((tokendata[0].strip(), tokendata[1].strip()))
                result.append(tags)
        return result

def getLabels(victor_corpus):
        result = []
        f = open(victor_corpus)
        for line in f:
                data = line.strip().split('\t')
                for item in data[3:len(data)]:
                        label = int(item.strip().split(':')[0].strip())
                        result.append(label)
        return result

def readFeatures(path):
	result = []
	f = open(path)
	for line in f:
		result.append([float(v) for v in line.strip().split('\t')])
	f.close()
	return result		

model = '/export/data/ghpaetzold/benchmarking/lexmturk/scripts/evaluators/stanford-postagger-full-2015-04-20/models/english-bidirectional-distsim.tagger'
tagger = '/export/data/ghpaetzold/benchmarking/lexmturk/scripts/evaluators/stanford-postagger-full-2015-04-20/stanford-postagger.jar'
java = '/usr/bin/java'
shelve_file_tb = '/export/data/ghpaetzold/generalpurpose/binaryfeatureslex/shelve/ngram_dict_wmt_simplewiki_1billion_webbase_treebank.bin'
shelve_file_pa = '/export/data/ghpaetzold/generalpurpose/binaryfeatureslex/shelve/ngram_dict_wmt_simplewiki_1billion_webbase_generalised.bin'

fe = FeatureEstimator(norm=False)
#fe.addCollocationalFeature('/export/data/ghpaetzold/subtitlesimdb/corpora/160715/subtleximdb.5gram.unk.bin.txt', 1, 1, 'Complexity')
#fe.addTargetPOSTagProbability('/export/data/ghpaetzold/LEXenstein/corpora/POS_condprob_model.bin', model, tagger, java, 'Simplicity')
fe.addTranslationProbabilityFeature('/export/data/ghpaetzold/LEXenstein/corpora/transprob_dict_lexmturk.bin', 'Simplicity')
w2vmodel = '/export/data/ghpaetzold/word2vecvectors/models/word_vectors_all_generalized_500_cbow.bin'
fe.addTaggedWordVectorSimilarityFeature(w2vmodel, model, tagger, java, 'paetzold', 'Simplicity')
#fe.addIsSynonymFeature('Simplicity')
#fe.addIsHypernymFeature('Simplicity')
#fe.addIsHyponymFeature('Simplicity')

print('For training...')
tagged_sents = getTaggedSents('/export/data/ghpaetzold/user_study_sgss/corpora/tagged_sents_grammaticality_meaning_victor_training.txt')
fe.temp_resources['tagged_sents'] = tagged_sents
Xtr = fe.calculateFeatures(train_victor_corpus)
#Xtr = readFeatures('/export/data/ghpaetzold/user_study_sgss/corpora/features_meaning_training.txt')
Ytr = getLabels(train_victor_corpus)

print('For testing...')
tagged_sents = getTaggedSents('/export/data/ghpaetzold/user_study_sgss/corpora/tagged_sents_grammaticality_meaning_victor_testing.txt')
fe.temp_resources['tagged_sents'] = tagged_sents
Xte = fe.calculateFeatures(test_victor_corpus)
#Xte = readFeatures('/export/data/ghpaetzold/user_study_sgss/corpora/features_meaning_testing.txt')

print('Training...')
mli = MachineLearningIdentifier(fe)
mli.Xtr = Xtr
mli.Ytr = Ytr
mli.Xte = Xte
mli.selectKBestFeatures(k=k)
mli.trainSGDClassifier(loss=loss, penalty=penalty, alpha=alpha, l1_ratio=l1_ratio, epsilon=epsilon, class_weight='auto')
labels = mli.identifyComplexWords()

o = open(out_file, 'w')
for label in labels:
	o.write(str(label) + '\n')
o.close()
