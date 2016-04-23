import os

trainset = '../../corpora/cwi_paetzold_training_conservative.txt'
testset = '../../corpora/cwi_paetzold_testing.txt'

#Features: 21
flabels = []
flabels.append('length')
flabels.append('syllable')
flabels.append('freqSubtlex')
flabels.append('freqSubimdb')
flabels.append('freqWiki')
flabels.append('freqSimplewiki')
flabels.append('freqSubimdblex')
flabels.append('senses')
flabels.append('synonyms')
flabels.append('hypernyms')
flabels.append('hyponyms')
flabels.append('mindepth')
flabels.append('maxdepth')

for i in range(0, len(flabels)):
	os.system('mkdir ../../labels_majority/'+flabels[i])
	output = '../../labels_majority/'+flabels[i]+'/labels_'+flabels[i]+'.txt'
	comm = 'nohup python Run_Threshold.py '+testset+' '+trainset+' '+str(i)+' '+output+' &'
	os.system(comm)
