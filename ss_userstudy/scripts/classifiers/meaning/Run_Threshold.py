from lexenstein.identifiers import *
from lexenstein.features import *
from lexenstein.morphadorner import *
import sys

train_victor_corpus = sys.argv[1].strip()
test_victor_corpus = sys.argv[2].strip()
index = int(sys.argv[3].strip())
output_path = sys.argv[4].strip()

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

fe = FeatureEstimator(norm=False)
fe.addCollocationalFeature('/export/data/ghpaetzold/subtitlesimdb/corpora/160715/subtleximdb.5gram.unk.bin.txt', 1, 1, 'Simplicity')
fe.addTargetPOSTagProbability('/export/data/ghpaetzold/LEXenstein/corpora/POS_condprob_model.bin', model, tagger, java, 'Simplicity')
fe.addTranslationProbabilityFeature('/export/data/ghpaetzold/LEXenstein/corpora/transprob_dict_lexmturk.bin', 'Simplicity')
w2vmodel = '/export/data/ghpaetzold/word2vecvectors/models/word_vectors_all_generalized_500_cbow.bin'
fe.addTaggedWordVectorSimilarityFeature(w2vmodel, model, tagger, java, 'paetzold', 'Simplicity')
fe.addIsSynonymFeature('Simplicity')
fe.addIsHypernymFeature('Simplicity')
fe.addIsHyponymFeature('Simplicity')

ti = ThresholdIdentifier(fe)

Xtr = readFeatures('/export/data/ghpaetzold/user_study_sgss/corpora/features_meaning_training.txt')
Ytr = getLabels(train_victor_corpus)
Xte = readFeatures('/export/data/ghpaetzold/user_study_sgss/corpora/features_meaning_testing.txt')

ti.Xtr = Xtr
ti.Ytr = Ytr
ti.Xte = Xte
ti.trainIdentifierBruteForce(index)
labels = ti.identifyComplexWords()

o = open(output_path, 'w')
for label in labels:
	o.write(str(label) + '\n')
o.close()
