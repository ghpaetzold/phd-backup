import os

os.system('mkdir ../../../classes/meaning/sgd/')

#Parameters:
#losses = ['hinge', 'log', 'modified_huber', 'squared_hinge', 'perceptron']
ks = ['all']
#ks = ['all']
losses = ['hinge', 'squared_hinge', 'modified_huber']
#losses = ['modified_huber']
penalties = ['elasticnet']
#penalties = ['l2']
alphas = ['0.001', '0.1']
#alphas = ['0.1']
l1ratios = ['0.25', '0.5', '0.75']
#l1ratios = ['0.15']
epsilons = ['0.0001']
#epsilons = ['0.1']

trainset = '../../../datasets/grammaticality_victor_training.txt'
testset = '../../../datasets/grammaticality_victor_testing.txt'
for l in losses:
	for p in penalties:
		for a in alphas:
			for r in l1ratios:
				for e in epsilons:
					for k in ks:
						output = '../../../classes/meaning/sgd/labels_SGDClassifier_'+l+'_'+p+'_'+a+'_'+r+'_'+e+'_'+k+'w2vtransprob.txt'
						comm = 'nohup python Run_SGDClassifier.py '+trainset+' '+k+' '+l+' '+p+' '+a+' '+r+' '+e+' '+testset+' '+output+' &'
						os.system(comm)
