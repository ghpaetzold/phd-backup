import os

#Parameters:
losses = ['hinge', 'modified_huber']
penalties = ['l2', 'l1', 'elasticnet']
alphas = ['0.001', '0.01', '0.1']
l1ratios = ['0.01', '0.10', '0.15']
epsilons = ['0.0001', '0.001']

generators = os.listdir('../../substitutions/')
#generators = ['yamamoto']

testsets = []
testsets.append('substitutions_svmrank_0.125_1_1_0.0001.txt')
#testsets.append('substitutions_boundaryCV_0.125.txt')
#testsets.append('substitutions_WSD_enhancedlesk.txt')
#testsets.append('substitutions_void.txt')
#testsets.append('substitutions_wordvector_0.125_HasStop_0_True_True_True.txt')
#testsets.append('substitutions_biran_0.0_0.8.txt')
#testsets.append('substitutions_WSD_first.txt')
#testsets.append('substitutions_WSD_lesk.txt')
#testsets.append('substitutions_WSD_path.txt')
#testsets.append('substitutions_WSD_random.txt')

for generator in generators:
	print(generator)
	for testset in testsets:
		testsetd = testset.strip().split('_')
		selector = testsetd[1].strip()
		if selector == 'WSD':
			selector = testsetd[2].strip()
		for l in losses:
			for p in penalties:
				for a in alphas:
					for r in l1ratios:
						for e in epsilons:
							output = '../../rankings/boundary/ranks_'+generator+'_'+selector+'_'+l+'_'+p+'_'+a+'_'+r+'_'+e+'.txt'
							comm = 'nohup python Run_Boundary.py ../../corpora/lexmturk_all.txt 1 '+l+' '+p+' '+a+' '+r+' '+e
							comm += ' ../../substitutions/'+generator+'/'+testset+' '+output+' &'
							os.system(comm)
