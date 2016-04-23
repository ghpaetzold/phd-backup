import os, sys

def getRankings(valid):
	result = []
	f = open('../../../rankings/rnnlm/ranks_allvocab_void_'+valid+'.txt')
	for line in f:
		words = line.strip().split('\t')
		result.append(words[0:100])
	f.close()
	return result

valid = sys.argv[1]

rankings = getRankings(valid)

f = open('../../../corpora/paetzold_nns_dataset.txt')
o = open('../../../substitutions/allvocab/substitutions_rnnlm_'+valid+'.txt', 'w')
for rank in rankings:
	data = f.readline().strip().split('\t')
	newline = data[0] + '\t' + data[1] + '\t' + data[2] + '\t'
	for word in rank:
		newline += '0:'+word + '\t'
	o.write(newline.strip() + '\n')
f.close()
o.close()

