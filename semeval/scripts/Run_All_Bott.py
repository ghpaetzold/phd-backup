import os

#Parameters:
alphas = ['-1', '0', '1']

trainset = '../corpora/semeval/semeval_train.txt'
testset = '../corpora/semeval/semeval_test.txt'
for a1 in alphas:
	for a2 in alphas:
		output = '../rankings/bott/ranks_'+a1+'_'+a2+'.txt'
		lm = '../../../machinelearningranking/corpora/lm/simplewiki.5gram.bin.txt'
		comm = 'nohup python Run_Bott.py '+trainset+' '+lm+' '+a1+' '+a2+' '+testset+' '+output+' &'
		os.system(comm)
		#print(comm)
