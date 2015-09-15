import os

#Max file: ranks_modified_huber_l1_0.1_0.05_0.0001.txt

#Parameters:
positive_ranges = ['1','2','3']
folds = ['5', '10']
#test_sizes = ['0.2', '0.25', '0.30', '0.5', '0.75']
test_sizes = ['0.5', '0.25']
ks = ['6', '8']

trainset = '../../corpora/ls_dataset_benchmarking_train.txt'
testset = '../../corpora/ls_dataset_benchmarking_test.txt'

os.system('mkdir ../../sr_rankings/boundary')
for r in positive_ranges:
	for f in folds:
		for t in test_sizes:
			for k in ks:
				output = '../../sr_rankings/boundary/ranks_'+r+'_'+f+'_'+t+'_'+k+'.txt'
				comm = 'nohup python Run_PaetzoldCV.py '+trainset+' '+r+' '+f+' '+t+' '+testset+' '+output+' '+k+' &'
				os.system(comm)
