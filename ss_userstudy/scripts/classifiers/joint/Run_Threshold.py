from lexenstein.identifiers import *
from lexenstein.features import *
from lexenstein.morphadorner import *
import sys

train_victor_corpus = sys.argv[1].strip()
test_victor_corpus = sys.argv[2].strip()
index = int(sys.argv[3].strip())
out_file = sys.argv[4].strip()

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

fe = FeatureEstimator(norm=False)
fe.addCollocationalFeature('/export/data/ghpaetzold/subtitlesimdb/corpora/160715/subtleximdb.5gram.unk.bin.txt', 1, 1, 'Complexity')
fe.addTaggedFrequencyCollocationalFeature(shelve_file_tb, 1, 1, model, tagger, java, 'treebank', 'Simplicity')
fe.addTaggedFrequencyCollocationalFeature(shelve_file_pa, 1, 1, model, tagger, java, 'paetzold', 'Simplicity')
fe.addTargetPOSTagProbability('/export/data/ghpaetzold/LEXenstein/corpora/POS_condprob_model.bin', model, tagger, java, 'Simplicity')

ti = ThresholdIdentifier(fe)

print('For training...')
tagged_sents = getTaggedSents('/export/data/ghpaetzold/benchmarking/ss_userstudy/corpora/tagged_sents_grammaticality_meaning_training.txt')
fe.temp_resources['tagged_sents'] = tagged_sents
Xtr = fe.calculateFeatures(train_victor_corpus)
Ytr = getLabels(train_victor_corpus)

print('For testing...')
tagged_sents = getTaggedSents('/export/data/ghpaetzold/benchmarking/ss_userstudy/corpora/tagged_sents_lexmturk_all.txt')
fe.temp_resources['tagged_sents'] = tagged_sents
Xte = fe.calculateFeatures(test_victor_corpus)

print('Training...')
ti.Xtr = Xtr
ti.Ytr = Ytr
ti.Xte = Xte
ti.trainIdentifierBruteForce(index)
labels = ti.identifyComplexWords()

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
