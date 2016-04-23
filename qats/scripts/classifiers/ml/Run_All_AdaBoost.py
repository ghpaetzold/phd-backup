import os

#Parameters:
types = ['G', 'S', 'M', 'O']

for type in types:
        trainset = '../../../corpora/'+type+'_train.txt'
        testset = '../../../corpora/'+type+'_test.txt'
        os.system('mkdir ../../../labels/'+type+'/adaboost')
	output = '../../../labels/'+type+'/adaboost/labels_AdaBoost.txt'
	comm = 'nohup python Run_AdaBoost.py '+trainset+' '+testset+' '+output+' &'
	os.system(comm)
