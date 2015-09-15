from lexenstein.selectors import *
import sys

generator = sys.argv[1]
victor_corpus = sys.argv[2]
proportion = float(sys.argv[3])
stop_words_file = sys.argv[4]
if stop_words_file=='None':
	stop_words_file = None
window = int(sys.argv[5].strip())
onlyInformative = False
if sys.argv[6].strip()=='True':
	onlyInformative = True
keepTarget = False
if sys.argv[7].strip()=='True':
	keepTarget = True
onePerWord = False
if sys.argv[8].strip()=='True':
	onePerWord = True
out = sys.argv[9].strip()

def getSubs(generator):
	result = {}
	f = open('../../substitutions/' + generator + '/substitutions.txt')
	for line in f:
		data = line.strip().split('\t')
		target = data[0].strip()
		candidates = data[1].strip().split('|||')
		result[target] = candidates
	f.close()
	return result

subs = getSubs(generator)

pos_model = '/export/data/ghpaetzold/benchmarking/lexmturk/scripts/evaluators/stanford-postagger-full-2015-04-20/models/english-bidirectional-distsim.tagger'
stanford_tagger = '/export/data/ghpaetzold/benchmarking/lexmturk/scripts/evaluators/stanford-postagger-full-2015-04-20/stanford-postagger.jar'
java_path = '/usr/bin/java'
vector_model = '/export/data/ghpaetzold/word2vecvectors/models/word_vectors_all_generalized_1100_cbow.bin'

wvs = WordVectorSelector(vector_model, pos_model, stanford_tagger, java_path, pos_type='paetzold')
selected = wvs.selectCandidates(subs, victor_corpus, proportion=proportion, proportion_type='percentage', stop_words_file=stop_words_file, window=window, onlyInformative=onlyInformative, keepTarget=keepTarget, onePerWord=onePerWord)

outf = open(out, 'w')
vicf = open(victor_corpus)
for cands in selected:
	data = vicf.readline().strip().split('\t')
	newline = data[0] + '\t' + data[1] + '\t' + data[2] + '\t'
	for cand in cands:
		newline += '0:'+cand + '\t'
	outf.write(newline.strip() + '\n')
outf.close()
vicf.close()
