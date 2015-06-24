import os

trainset = '../corpora/semeval/semeval_train.txt'
testset = '../corpora/semeval/semeval_test.txt'

#Features: 21
flabels = []
flabels.append('lexicon_basic')
flabels.append('lexicon_wikisimple')
flabels.append('length')
flabels.append('syllable')
flabels.append('freq_subtlex')
flabels.append('freq_subimdb')
flabels.append('freq_wiki')
flabels.append('freq_simplewiki')
flabels.append('freq_brown')
flabels.append('colloc00')
flabels.append('colloc01')
flabels.append('colloc02')
flabels.append('colloc10')
flabels.append('colloc11')
flabels.append('colloc12')
flabels.append('colloc20')
flabels.append('colloc21')
flabels.append('colloc22')
flabels.append('sent_prob')
flabels.append('senses')
flabels.append('synonyms')
flabels.append('hypernyms')
flabels.append('hyponyms')
flabels.append('mindepth')
flabels.append('maxdepth')

for i in range(0, len(flabels)):
	output = '../rankings/metrics/ranks_'+flabels[i]+'.txt'
	comm = 'nohup python Run_Metric.py '+testset+' '+str(i)+' '+output+' &'
	os.system(comm)
