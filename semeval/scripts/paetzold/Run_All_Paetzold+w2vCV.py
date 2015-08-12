import os

#Max file: ranks_modified_huber_l1_0.1_0.05_0.0001.txt

#Parameters:
positive_ranges = ['1','2','3']
folds = ['5', '10', '15', '20']
folds = ['10']
test_sizes = ['0.2', '0.25', '0.30', '0.5', '0.75']
#test_sizes = ['0.10', '0.05', '0.25']

trainset = '../../corpora/semeval/semeval_train_clean.txt'
testset = '../../corpora/semeval/semeval_test_clean.txt'
for r in positive_ranges:
	for f in folds:
		for t in test_sizes:
			output = '../../rankings/paetzold+w2vCV/ranks_'+r+'_'+f+'_'+t+'.txt'
			comm = 'nohup python Run_Paetzold+w2vCV.py '+trainset+' '+r+' '+f+' '+t+' '+testset+' '+output+' &'
			os.system(comm)
