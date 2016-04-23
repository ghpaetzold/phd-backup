import os

trainset = '../../../corpora/cwi_paetzold_training.txt'
testset = '../../../corpora/ls_dataset_benchmarking.txt'

#Features: 21
flabels = []
flabels.append('bestf1semeval')

for i in range(0, len(flabels)):
	os.system('mkdir ../../../labels/'+flabels[i])
	output = '../../../labels/'+flabels[i]+'/labels_'+flabels[i]+'.txt'
	comm = 'nohup python Run_Threshold.py '+testset+' '+trainset+' '+str(i)+' '+output+' &'
	os.system(comm)
