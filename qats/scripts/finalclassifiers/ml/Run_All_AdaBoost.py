import os

#Parameters:
types = ['G', 'S', 'M', 'O']

for type in types:
        trainset = '../../../corpora/'+type+'_all.txt'
        testset = '../../../corpora/testset/'+type+'_all.txt'
        os.system('mkdir ../../../finallabels/'+type+'/adaboost')
	output = '../../../finallabels/'+type+'/adaboost/labels_AdaBoost.txt'
	comm = 'nohup python Run_AdaBoost.py '+trainset+' '+testset+' '+output+' &'
	os.system(comm)
