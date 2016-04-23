from lexenstein.morphadorner import *
from lexenstein.identifiers import *
from lexenstein.features import *
import sys
import numpy as np

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
task = sys.argv[9].strip()


def transformVector(X, task, file):
	values = [line.strip() for line in open('../../corpora/'+task+'_tasks.txt')]
	Xr = []
	filedata = getFileData(file)
	void = [0.0]*len(X[0])
	for i in range(0, len(X)):
		baseX = list(X[i])
		void = [0.0]*len(baseX)
		vec = list(baseX)
		map = filedata[i]
		included = map[task]
		for value in values:
			if value in included:
				vec += baseX
			else:
				vec += void
#		print('Vec size: ' + str(len(vec)))
		Xr.append(vec)
#		print('Xr size: ' + str(len(Xr)))
#		print('Xr last size: ' + str(len(Xr[len(Xr)-1])))
#	Xr = np.array(Xr)
#	print(str(Xr.shape))
	print('Len: ' + str(len(Xr)))
	print('Xr first: ' + str(len(Xr[0])))
	for line in Xr:
		if len(line)!=len(Xr[0]):
			print('Problem at: ' + str(len(line)))
	return Xr


def getFileData(file):
	result = []
	f = open(file)
	for line in f:
		data = line.strip().split('\t')
	        anns = data[4:]
		map = {'age':set([]), 'language':set([]), 'education':set([]), 'proficiency':set([])}
	        for ann in anns:
	                annd = ann[1:len(ann)-1].split(', ')
			age = formatAge(int(annd[0]))
			language = annd[1]
			education = annd[2]
			proficiency = annd[3]
			map['age'].add(age)
			map['language'].add(language)
			map['education'].add(education)
			map['proficiency'].add(proficiency)
		result.append(map)
	return result

def formatAge(age):
	result = 0
	if age<=20:
		result = 20
	elif age<=30:
		result = 30
	elif age<=40:
		result = 40
	elif age<=50:
		result = 50
	else:
		result = 60	
	return str(result)


m = MorphAdornerToolkit('/export/data/ghpaetzold/LEXenstein/morph/')

fe = FeatureEstimator(norm=False)
fe.addLexiconFeature('/export/data/ghpaetzold/benchmarking/semeval/corpora/basic/basic_words.txt', 'Simplicity')
fe.addLexiconFeature('/export/data/ghpaetzold/benchmarking/semeval/corpora/vocabularies/wikisimple.vocab.txt', 'Simplicity')
fe.addLengthFeature('Complexity')
fe.addSyllableFeature(m, 'Complexity')
fe.addCollocationalFeature('../../../../benchmarking/semeval/corpora/lm/simplewiki/simplewiki.5gram.bin.txt', 2, 2, 'Complexity')
fe.addSentenceProbabilityFeature('../../../../benchmarking/semeval/corpora/lm/simplewiki/simplewiki.5gram.bin.txt', 'Complexity')
fe.addCollocationalFeature('../../../lexmturk/corpora/subtleximdb.5gram.bin.unk.txt', 2, 2, 'Complexity')
fe.addSentenceProbabilityFeature('../../../lexmturk/corpora/subtleximdb.5gram.bin.unk.txt', 'Complexity')
fe.addSenseCountFeature('Simplicity')
fe.addSynonymCountFeature('Simplicity')
fe.addHypernymCountFeature('Simplicity')
fe.addHyponymCountFeature('Simplicity')
fe.addMinDepthFeature('Complexity')
fe.addMaxDepthFeature('Complexity')
#fe.addWordVectorValues('/export/data/ghpaetzold/LEXenstein/corpora/word_vectors_all.bin', 300, 'Complexity')

mli = MachineLearningIdentifier(fe)
mli.calculateTrainingFeatures(train_victor_corpus)
mli.calculateTestingFeatures(test_victor_corpus)
mli.selectKBestFeatures(k=k)

mli.Xtr = transformVector(mli.Xtr, task, train_victor_corpus)
mli.Xte = transformVector(mli.Xte, task, test_victor_corpus)

mli.trainDecisionTreeClassifier(criterion=criterion, splitter=splitter, max_features=max_features, max_depth=max_depth)
labels = mli.identifyComplexWords()

o = open(out_file, 'w')
for label in labels:
	o.write(str(label) + '\n')
o.close()
