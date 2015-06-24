import os

#Parameters:
alphas = ['0', '1']

trainset = '../corpora/semeval/semeval_train.txt'
testset = '../corpora/semeval/semeval_test.txt'
for a1 in alphas:
	for a2 in alphas:
		for a3 in alphas:
			for a4 in alphas:
				for a5 in alphas:
					output = '../rankings/yamamoto/ranks_'+a1+'_'+a2+'_'+a3+'_'+a4+'_'+a5+'.txt'
					lm = '../../../machinelearningranking/corpora/lm/simplewiki.5gram.bin.txt'
					cooc = '../../lexmturk/corpora/vectors.clean.txt'
					comm = 'nohup python Run_Yamamoto.py '+trainset+' '+lm+' '+cooc+' '+a1+' '+a2+' '+a3+' '+a4+' '+a5+' '+testset+' '+output+' &'
					os.system(comm)
					#print(comm)
