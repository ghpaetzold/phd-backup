import os

#Parameters:
types = ['G', 'S', 'M', 'O']

for type in types:
	trainset = '../../../corpora/'+type+'_all.txt'
        testset = '../../../corpora/testset/'+type+'_all.txt'
        os.system('mkdir ../../../finallabels/'+type+'/randomforest')
	output = '../../../finallabels/'+type+'/randomforest/labels_RandomForests.txt'
	comm = 'nohup python Run_RandomForests.py '+trainset+' '+testset+' '+output+' &'
	os.system(comm)
