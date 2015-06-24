import sys, os, nltk
import gensim
from scipy.spatial.distance import cosine
import numpy as np

inpsubs = sys.argv[1]
outsubs = sys.argv[2]
temp = sys.argv[3]

def getFinalCandidates(candidate_dists):
	proportion = 0.25
	result = sorted(list(candidate_dists.keys()), key=candidate_dists.__getitem__)
	return result[0:max(1, int(proportion*float(len(result))))]

def getVec(sentence, model):
	tokens = sentence.split(' ')
	result = []
	for token in tokens:
		if len(result)==0:
			try:
				result = model[token]
			except KeyError:
				try:
					result = model[token.lower()]
				except KeyError:
					result = []
		else:
			try:
				result = np.multiply(result, model[token])
			except KeyError:
				try:
					result = np.multiply(result, model[token.lower()])
				except KeyError:
					result = result
	return result

def getCandidateSentence(sentence, candidate, head):
	tokens = sentence.strip().split(' ')
	result = ''
	for i in range(0, head):
		result += tokens[i] + ' '
	result += candidate + ' '
	for i in range(head+1, len(tokens)):
		result += tokens[i] + ' '
	return result.strip()

def getHead(sent, target):
        tokens = sent.strip().lower().split(' ')
        head = -1
        for i in range(0, len(tokens)):
                if target == tokens[i]:
                        head = i
        return head

substitutions = {}
inpf = open(inpsubs)
for line in inpf:
	data = line.strip().split('\t')
	target = data[0].strip()
	subs = sorted(data[1].strip().split('|||'))
	substitutions[target] = subs
inpf.close()

#Load word vector model:
model = gensim.models.word2vec.Word2Vec.load_word2vec_format('../../corpora/word_vectors/word_vectors_all.bin', binary=True)

outf = open(outsubs, 'w')
lex = '../../corpora/lexmturk/lexmturk.txt'
lexf = open(lex)
for line in lexf:
	data = line.strip().split('\t')
	sent = data[0].strip()
	target = data[1].strip()
	head = getHead(sent, target)
	
	target_vec = getVec(sent, model)

	candidates = []
	if target in substitutions.keys():
		candidates = substitutions[target]
	
	candidate_dists = {}
	for candidate in candidates:
		candidate_vec = getVec(candidate, model)
		try:
			candidate_dists[candidate] = cosine(candidate_vec, target_vec)
		except ValueError:
			candidate_dists = candidate_dists

	final_candidates = getFinalCandidates(candidate_dists)

	newline = target + '\t'	
	for candidate in final_candidates:
		newline += candidate + '|||'

	if newline.endswith('|||'):
		newline = newline[0:len(newline)-3]
	outf.write(newline.strip() + '\n')
lexf.close()
outf.close()
