import os

trainset = '../../corpora/ls_dataset_benchmarking_train.txt'
testset = '../../corpora/ls_dataset_benchmarking_test.txt'

flabels = []
flabels.append('devlin')

for i in range(0, len(flabels)):
	os.system('mkdir ../../sr_rankings/'+flabels[i])
	output = '../../sr_rankings/'+flabels[i]+'/ranks.txt'
	comm = 'nohup python Run_Metric.py '+testset+' '+str(i)+' '+output+' &'
	os.system(comm)
