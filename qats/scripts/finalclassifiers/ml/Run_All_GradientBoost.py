import os

#Parameters:
types = ['G', 'S', 'M', 'O']

for type in types:
	trainset = '../../../corpora/'+type+'_all.txt'
        testset = '../../../corpora/testset/'+type+'_all.txt'
        os.system('mkdir ../../../finallabels/'+type+'/gradientboost')
	output = '../../../finallabels/'+type+'/gradientboost/labels.txt'
	comm = 'nohup python Run_GradientBoost.py '+trainset+' '+testset+' '+output+' &'
	os.system(comm)
