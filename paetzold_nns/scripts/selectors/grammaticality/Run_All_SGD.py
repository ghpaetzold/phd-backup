import os

generators = os.listdir('/export/data/ghpaetzold/benchmarking/ss_userstudy/substitutions/')
#generators.remove('all')

#Parameters:
#losses = ['hinge', 'log', 'modified_huber', 'squared_hinge', 'perceptron']
#ks = ['10', '15', '20']
ks = ['all']
losses = ['hinge', 'modified_huber']
#losses = ['modified_huber']
penalties = ['elasticnet']
#penalties = ['l2']
alphas = ['0.001', '0.1']
#alphas = ['0.1']
#l1ratios = ['0.25', '0.5', '0.75']
l1ratios = ['0.5']
epsilons = ['0.0001']
#epsilons = ['0.1']

for l in losses:
	for p in penalties:
		for a in alphas:
			for r in l1ratios:
				for e in epsilons:
					for k in ks:
						for i in range(1, 6):
							for generator in generators:
								trainset = '/export/data/ghpaetzold/benchmarking/ss_userstudy/corpora/grammaticality_victor_training_'
								trainset += str(i) + '.txt'
								testset = '../../../substitutions/'
								testset += generator + '/substitutions_void.txt'
								output = '../../../substitutions/' + generator + '/'
								output += 'substitutions_GrammaticalitySGD_'+l+'_'+p+'_'+a+'_'+r+'_'+e+'_'+k+'_'+str(i)+'.txt'
								comm = 'nohup python Run_SGDClassifier.py '+trainset+' '+k+' '+l+' '+p+' '+a+' '+r+' '+e+' '+testset+' '+output+' &'
								os.system(comm)
