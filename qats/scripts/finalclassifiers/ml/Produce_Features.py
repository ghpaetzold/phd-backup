import kenlm

def getFeatures(s1, s2, lms):
	result = ''
	#Calculate sentence probabilities:
	for lm in lms:
		result += str(lm.score(s1, bos=True, eos=True))+' '
		result += str(lm.score(s2, bos=True, eos=True))+' '
	#Calculate lengths:
	result += str(len(s1))+' '
	result += str(len(s2))+' '
	result += str(len(s1.split(' ')))+' '
	result += str(len(s2.split(' ')))+' '
	result += str(len(set(s1.split(' '))))+' '
	result += str(len(set(s2.split(' '))))+' '
	return result.strip()
	

#Language models:
lmsp = []
lmsp.append('/export/data/ghpaetzold/wordnetlmranking/corpora/corpus/subtlex/lm/corpus.clean.5.bin.txt')
lmsp.append('/export/data/ghpaetzold/subtitlesimdb/corpora/160715/subimdb.5gram.unk.bin.txt')
lmsp.append('/export/data/ghpaetzold/wordnetlmranking/corpora/corpus/wiki/lm/corpus.clean.5.bin.txt')
lmsp.append('/export/data/ghpaetzold/benchmarking/semeval/corpora/lm/simplewiki/simplewiki.5gram.bin.txt')
lms = []
for lm in lmsp:
	lms.append(kenlm.LanguageModel(lm))

#Calculate training features:
f = open('../../../corpora/G_all.txt')
o = open('features_training.txt', 'w')
for line in f:
	data = line.strip().split('\t')
	s1 = data[0].strip()
	s2 = data[1].strip()
	features = getFeatures(s1, s2, lms)
	o.write(features + '\n')
f.close()
o.close()

f = open('../../../corpora/testset/G_all.txt')
o = open('features_testing.txt', 'w')
for line in f:
        data = line.strip().split('\t')
        s1 = data[0].strip()
        s2 = data[1].strip()
        features = getFeatures(s1, s2, lms)
        o.write(features + '\n')
f.close()
o.close()
