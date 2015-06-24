import sys, os, nltk
from scipy.spatial.distance import cosine
import numpy as np

inpsubs = sys.argv[1]
outsubs = sys.argv[2]
temp = sys.argv[3]

def getCosine(vec1, vec2):
	all_keys = sorted(list(set(vec1.keys()).union(set(vec2.keys()))))
	v1 = []
	v2 = []
	for k in all_keys:
		if k in vec1:
			v1.append(vec1[k])
		else:
			v1.append(0.0)
		if k in vec2:
			v2.append(vec2[k])
		else:
			v2.append(0.0)
	return cosine(v1, v2)

def getCommonVec(target, candidate, model):
	if target not in model.keys() or candidate not in model.keys():
		return {}
	else:
		result = {}
		common_keys = set(model[target].keys()).intersection(set(model[candidate].keys()))
		for k in common_keys:
			if model[target][k]>model[candidate][k]:
				result[k] = model[candidate][k]
			else:
				result[k] = model[target][k]
		return result

def isNumeral(text):
        try:
                num = float(text.strip())
                return True
        except ValueError:
                return False

def getSentVec(sent, model, head):
	coocs = {}
 	tokens = sent.strip().split(' ')
	left = max(0, head-5)
	right = min(len(tokens), head+6)
	for j in range(left, right):
		if j!=head:
			cooc = tokens[j]
			if isNumeral(cooc):
				cooc = '#NUMERAL#'
			if cooc not in coocs.keys():
				coocs[cooc] = 1
			else:
				coocs[cooc] += 1
	return coocs

def getFinalCandidates(candidate_dists):
	proportion = 0.25
	result = sorted(list(candidate_dists.keys()), key=candidate_dists.__getitem__)
	return result[0:max(1, int(proportion*float(len(result))))]

def getVec(word, model):
	result = {}
	try:
		result = model[word]
	except KeyError:
		try:
			result = model[word.lower()]
		except KeyError:
			result = {}
	return result

def getCooccurrModel(path):
	result = {}
	numerals = set([0,1,2,3,4,5,6,7,8,9])
	f = open(path)
	for line in f:
		data = line.strip().split('\t')
		target = data[0].strip()
		coocs = data[1:len(data)]
		if target[0] not in numerals:
			result[target] = {}	
			for cooc in coocs:
				coocd = cooc.strip().split(':')
				word = coocd[0].strip()
				count = int(coocd[1].strip())
				result[target][word] = count
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
print('Getting model...')
model = getCooccurrModel('../../corpora/cooccur_vectors/vectors.clean.txt')
print('Model read!')

outf = open(outsubs, 'w')
lex = '../../corpora/lexmturk/lexmturk.txt'
lexf = open(lex)
c = 0
for line in lexf:
	c += 1
	print(str(c))
	data = line.strip().split('\t')
	sent = data[0].strip()
	target = data[1].strip()
	head = getHead(sent, target)
	
	target_vec = getSentVec(sent, model, head)

	candidates = []
	if target in substitutions.keys():
		candidates = substitutions[target]
	
	final_candidates = set([])
	for candidate in candidates:
		candidate_vec = getVec(candidate, model)
		candidate_dist = 1.0
		try:
			candidate_dist = getCosine(candidate_vec, target_vec)
		except ValueError:
			candidate_dist = 1.0

		common_vec = getCommonVec(target, candidate, model)
		common_dist = 0.0
		try:
                        common_dist = getCosine(common_vec, target_vec)
                except ValueError:
                        common_dist = 0.0
		#print('For candidate: ' + candidate)
		#print('\tCandidate dist: ' + str(candidate_dist))
		#print('\tCommon dist:' + str(common_dist))
		#print('')
		if common_dist>=0.01 and candidate_dist<=0.75:
			final_candidates.add(candidate)

	newline = target + '\t'	
	for candidate in final_candidates:
		newline += candidate + '|||'

	if newline.endswith('|||'):
		newline = newline[0:len(newline)-3]
	outf.write(newline.strip() + '\n')
lexf.close()
outf.close()
