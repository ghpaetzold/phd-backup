import os

trainset = '../../corpora/cwi_paetzold_training.txt'
testset = '../../corpora/ls_dataset_benchmarking.txt'

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
	os.system('mkdir ../../labels/'+flabels[i])
	output = '../../labels/'+flabels[i]+'/labels_'+flabels[i]+'.txt'
	comm = 'nohup python Run_Threshold.py '+testset+' '+trainset+' '+str(i)+' '+output+' &'
	os.system(comm)
