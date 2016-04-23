from lexenstein.rankers import *
from lexenstein.features import *
import sys

victor_corpus = sys.argv[1]
train_feature_file = sys.argv[2]
c = float(sys.argv[3].strip())
epsilon = float(sys.argv[4].strip())
kernel = int(sys.argv[5].strip())
model_file = sys.argv[6].strip()
test_feature_file = sys.argv[7].strip()
scores_file = sys.argv[8].strip()
test_victor_corpus = sys.argv[9].strip()
output_path = sys.argv[10].strip()

#Add target to test corpus:
data = test_victor_corpus.strip().split(r'/')
gen = data[len(data)-2]
rest = data[len(data)-1]
rest = rest[0:len(rest)-4]
temp_victor = './temp/'+gen+'_'+rest+'.temp'

f = open(test_victor_corpus)
o = open(temp_victor, 'w')
for line in f:
        data = line.strip().split('\t')
        o.write(line.strip() + '\t0:' + data[1].strip() + '\n')
f.close()
o.close()

fe = FeatureEstimator()
fe.addCollocationalFeature('../../../semeval/corpora/lm/subtleximdb/subtleximdb.5gram.unk.bin.txt', 2, 2, 'Complexity')

br = SVMRanker(fe, '/export/tools/svm-rank/')
br.getFeaturesFile(victor_corpus, train_feature_file)
br.getTrainingModel(train_feature_file, c, epsilon, kernel, model_file)
br.getFeaturesFile(test_victor_corpus, test_feature_file)
br.getScoresFile(test_feature_file, model_file, scores_file)

ranks = br.getRankings(temp_victor, test_feature_file, scores_file)

o = open(output_path, 'w')
for rank in ranks:
	newline = ''
	for r in rank:
		newline += r + '\t'
	o.write(newline.strip() + '\n')
o.close()
