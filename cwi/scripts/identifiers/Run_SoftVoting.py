from lexenstein.morphadorner import *
from lexenstein.identifiers import *
from lexenstein.features import *
import sys
from sklearn import svm
from sklearn.linear_model import *
from sklearn.tree import *
from sklearn.ensemble import *
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import f_classif
from sklearn.preprocessing import normalize

train_victor_corpus = sys.argv[1]
test_victor_corpus = sys.argv[2].strip()
out_file = sys.argv[3].strip()

m = MorphAdornerToolkit('/export/data/ghpaetzold/LEXenstein/morph/')

fe = FeatureEstimator(norm=False)
fe.addLexiconFeature('../../../semeval/corpora/basic/basic_words.txt', 'Simplicity')
fe.addLexiconFeature('../../../semeval/corpora/vocabularies/wikisimple.vocab.txt', 'Simplicity')
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

clf1 = svm.SVC(probability=True)
clf2 = PassiveAggressiveClassifier()
clf3 = SGDClassifier()
clf4 = DecisionTreeClassifier()
clf5 = AdaBoostClassifier()
clf6 = GradientBoostingClassifier()
clf7 = RandomForestClassifier()

estimators = [('clf1', clf1), ('clf4', clf4), ('clf5', clf5), ('clf6', clf6), ('clf7', clf7)]
eclf1 = VotingClassifier(estimators=estimators, voting='soft')

mli = MachineLearningIdentifier(fe)
mli.calculateTrainingFeatures(train_victor_corpus)
mli.calculateTestingFeatures(test_victor_corpus)

Xtr = mli.Xtr
Ytr = mli.Ytr
Xte = mli.Xte

print('Fitting...')
eclf1 = eclf1.fit(Xtr, Ytr)
print('Fit!')

labels = eclf1.predict(Xte)

o = open(out_file, 'w')
for label in labels:
	o.write(str(label) + '\n')
o.close()
