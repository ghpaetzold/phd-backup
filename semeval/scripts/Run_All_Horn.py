import os

#Parameters:
Cs = ['0.0005', '0.0007', '0.001', '0.01', '0.1']
epsilons = ['0.0001', '0.0005', '0.0007', '0.001']
kernels = ['0', '1', '2', '3', '4']

trainset = '../corpora/semeval/semeval_train.txt'
testset = '../corpora/semeval/semeval_test.txt'
counter = -1
for C in Cs:
	for e in epsilons:
		for k in kernels:
			counter += 1
			output = '../rankings/horn/ranks_'+C+'_'+e+'_'+k+'.txt'
			trfile = './temp/train_feature_file_'+str(counter)+'.txt'
			mfile = './temp/model_'+str(counter)+'.txt'
			tefile = './temp/test_feature_file_'+str(counter)+'.txt'
			sfile = './temp/scores_'+str(counter)+'.txt'
			comm = 'nohup python Run_Horn.py '+trainset+' '+trfile+' '+C+' '+e+' '+k+' '+mfile+' '+tefile+' '+sfile+' '+testset+' '+output+' &'
			os.system(comm)
			#print(comm)
