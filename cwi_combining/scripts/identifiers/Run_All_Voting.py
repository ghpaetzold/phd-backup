import os

#Parameters:
ks = list(range(2, 20))
uses = ['True', 'False']

trainset = '../../corpora/cwi_paetzold_training.txt'
testset = '../../corpora/cwi_paetzold_testing.txt'
for k in ks:
	for use in uses:
		output = '../../labels/voting/labels_voting_'+str(k)+'_'+use+'.txt'
		comm = 'nohup python Run_Voting.py '+trainset+' '+str(k)+' '+' '+use+' '+testset+' '+output+' &'
		os.system(comm)
