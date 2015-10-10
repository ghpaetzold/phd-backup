import os

#Max file: ranks_modified_huber_l1_0.1_0.05_0.0001.txt

#Parameters:
positive_ranges = ['1','2','3']
folds = ['5', '10']
#test_sizes = ['0.2', '0.25', '0.30', '0.5', '0.75']
test_sizes = ['0.75', '0.5', '0.25']

trainset = '../../corpora/NNSimpLex_train.txt'
testset = '../../corpora/NNSimpLex_test.txt'
os.system('mkdir ../../rankings/paetzold/')

for r in positive_ranges:
	for f in folds:
		for t in test_sizes:
			output = '../../rankings/paetzold/ranks_'+r+'_'+f+'_'+t+'.txt'
			comm = 'nohup python Run_PaetzoldCV.py '+trainset+' '+r+' '+f+' '+t+' '+testset+' '+output+' &'
			os.system(comm)
