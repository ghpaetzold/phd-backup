import os

#Parameters:
types = ['G', 'S', 'M', 'O']

for type in types:
        trainset = '../../../corpora/'+type+'_train.txt'
        testset = '../../../corpora/'+type+'_test.txt'
        os.system('mkdir ../../../labels/'+type+'/randomforest')
	output = '../../../labels/'+type+'/randomforest/labels_RandomForests.txt'
	comm = 'nohup python Run_RandomForests.py '+trainset+' '+testset+' '+output+' &'
	os.system(comm)
