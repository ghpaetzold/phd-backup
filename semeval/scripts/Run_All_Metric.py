import os

trainset = '../corpora/semeval/semeval_train.txt'
testset = '../corpora/semeval/semeval_test.txt'

flabels = []
flabels.append('length')
flabels.append('syllable')
flabels.append('subimdb00')
flabels.append('subtlex00')
flabels.append('simplewiki00')
flabels.append('wiki00')
flabels.append('brown00')
flabels.append('senses')
flabels.append('synonyms')
flabels.append('hypernyms')
flabels.append('hyponyms')
flabels.append('mindepth')
flabels.append('maxdepth')

for i in range(0, len(flabels)):
	os.system('mkdir ../rankings/'+flabels[i])
	output = '../rankings/'+flabels[i]+'/ranks.txt'
	comm = 'nohup python Run_Metric.py '+testset+' '+str(i)+' '+output+' &'
	os.system(comm)
