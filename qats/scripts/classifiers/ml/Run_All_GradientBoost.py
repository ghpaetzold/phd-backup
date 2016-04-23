import os

#Parameters:
types = ['G', 'S', 'M', 'O']

for type in types:
        trainset = '../../../corpora/'+type+'_train.txt'
        testset = '../../../corpora/'+type+'_test.txt'
        os.system('mkdir ../../../labels/'+type+'/gradientboost')
	output = '../../../labels/'+type+'/gradientboost/labels.txt'
	comm = 'nohup python Run_GradientBoost.py '+trainset+' '+testset+' '+output+' &'
	os.system(comm)
