from lexenstein.morphadorner import *
from lexenstein.identifiers import *
from lexenstein.features import *
import sys

train_victor_corpus = sys.argv[1]
k = sys.argv[2].strip()
if k!='all':
	k = int(sys.argv[2].strip())
criterion = sys.argv[3].strip()
splitter = sys.argv[4].strip()
max_features = None
try:
	max_features = float(sys.argv[5].strip())
except ValueError:
	max_features = sys.argv[5].strip()
max_depth = None
try:
	max_depth = float(sys.argv[6].strip())
except ValueError:
	max_depth = None
test_victor_corpus = sys.argv[7].strip()
out_file = sys.argv[8].strip()

def getParsedSents(corpus):
        result = []
        f = open(corpus)
        for line in f:
                data = line.strip().split('\t')
                inst = []
                for parse in data:
                        parsed = parse.strip().split('|||')
                        inst.append((parsed[0], parsed[1], parsed[2], parsed[3], parsed[4]))
                result.append(inst)
        f.close()
        return result

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

model = '/export/data/ghpaetzold/benchmarking/lexmturk/scripts/evaluators/stanford-postagger-full-2015-04-20/models/english-bidirectional-distsim.tagger'
tagger = '/export/data/ghpaetzold/benchmarking/lexmturk/scripts/evaluators/stanford-postagger-full-2015-04-20/stanford-postagger.jar'
java = '/usr/bin/java'
shelve_file_tb = '/export/data/ghpaetzold/generalpurpose/binaryfeatureslex/shelve/ngram_dict_wmt_simplewiki_1billion_webbase_treebank.bin'
shelve_file_pa = '/export/data/ghpaetzold/generalpurpose/binaryfeatureslex/shelve/ngram_dict_wmt_simplewiki_1billion_webbase_generalised.bin'
lm = '/export/data/ghpaetzold/LEXenstein/corpora/dep_parse_lm_1billion.bin'
counts = '/export/data/ghpaetzold/LEXenstein/corpora/dep_parse_counts_1billion.bin'
stanford_parser = '/export/data/ghpaetzold/generalpurpose/binaryfeatureslex/stanford/stanford-parser/stanford-parser.jar'
dependency_models = '/export/data/ghpaetzold/generalpurpose/binaryfeatureslex/stanford/stanford-parser/stanford-parser-3.4.1-models.jar'
java_path = '/usr/bin/java'
w2vmodel = '/export/data/ghpaetzold/word2vecvectors/models/word_vectors_all_1300_cbow_retrofitted.bin'

fe = FeatureEstimator(norm=False)
fe.addCollocationalFeature('/export/data/ghpaetzold/subtitlesimdb/corpora/160715/subtleximdb.5gram.unk.bin.txt', 1, 1, 'Complexity')
fe.addTaggedFrequencyCollocationalFeature(shelve_file_tb, 1, 1, model, tagger, java, 'treebank', 'Simplicity')
fe.addTaggedFrequencyCollocationalFeature(shelve_file_pa, 1, 1, model, tagger, java, 'paetzold', 'Simplicity')
fe.addTargetPOSTagProbability('/export/data/ghpaetzold/LEXenstein/corpora/POS_condprob_model.bin', model, tagger, java, 'Simplicity')
fe.addTaggedWordVectorSimilarityFeature(w2vmodel, model, tagger, java, 'paetzold', 'Simplicity')

print('For training...')
tagged_sents = getTaggedSents('/export/data/ghpaetzold/user_study_sgss/datasets/tagged_sents_grammaticality_meaning_all.txt')
fe.temp_resources['tagged_sents'] = tagged_sents
Xtr = fe.calculateFeatures(train_victor_corpus)
Ytr = getLabels(train_victor_corpus)

print('For testing...')
tagged_sents = getTaggedSents('/export/data/ghpaetzold/benchmarking/paetzold_nns/corpora/tagged_sents_paetzold_nns_dataset.txt')
fe.temp_resources['tagged_sents'] = tagged_sents
Xte = fe.calculateFeatures(test_victor_corpus)

print('Training...')
mli = MachineLearningIdentifier(fe)
mli.Xtr = Xtr
mli.Ytr = Ytr
mli.Xte = Xte
mli.selectKBestFeatures(k=k)
mli.trainDecisionTreeClassifier(criterion=criterion, splitter=splitter, max_features=max_features, max_depth=max_depth)
labels = mli.identifyComplexWords()

o = open(out_file, 'w')
f = open(test_victor_corpus)
c = -1
for line in f:
        data = line.strip().split('\t')
        newline = data[0] + '\t' + data[1] + '\t' + data[2] + '\t'
        cands = data[3:len(data)]
        for cand in cands:
                c += 1
                label = labels[c]
                if str(label)=='1':
                        newline += cand + '\t'
        o.write(newline.strip() + '\n')
o.close()
f.close()
