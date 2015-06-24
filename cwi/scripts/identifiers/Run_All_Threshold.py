import os

trainset = '../../corpora/cwi_paetzold_training.txt'
testset = '../../corpora/cwi_paetzold_testing.txt'

#Features: 21
flabels = []
flabels.append('length')
flabels.append('syllable')
flabels.append('colloc00subtlex')
flabels.append('colloc00imdb')
flabels.append('colloc00wiki')
flabels.append('colloc00simplewiki')
flabels.append('colloc00imdblex')
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
	output = '../../labels/threshold/labels_'+flabels[i]+'.txt'
	comm = 'nohup python Run_Threshold.py '+testset+' '+trainset+' '+str(i)+' '+output+' &'
	os.system(comm)
