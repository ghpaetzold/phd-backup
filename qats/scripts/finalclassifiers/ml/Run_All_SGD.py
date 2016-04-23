import os

#Parameters:
ks = ['all']
losses = ['hinge', 'squared_hinge', 'modified_huber']
penalties = ['l2', 'l1', 'elasticnet']
alphas = ['0.01', '0.1']
l1ratios = ['0.05', '0.10', '0.15']
types = ['G', 'S', 'M', 'O']

for type in types:
        trainset = '../../../corpora/'+type+'_train.txt'
        testset = '../../../corpora/'+type+'_test.txt'
        os.system('mkdir ../../../labels/'+type+'/sgd')
	for l in losses:
		for p in penalties:
			for a in alphas:
				for r in l1ratios:
					for k in ks:
						output = '../../../labels/'+type+'/sgd/labels_SGD_'+l+'_'+p+'_'+a+'_'+r+'_'+k+'.txt'
						comm = 'nohup python Run_SGD.py '+trainset+' '+k+' '+l+' '+p+' '+a+' '+r+' '+testset+' '+output+' &'
						os.system(comm)
