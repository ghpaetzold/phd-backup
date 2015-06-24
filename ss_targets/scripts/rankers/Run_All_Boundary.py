import os

#Parameters:
losses = ['modified_huber']
penalties = ['l2', 'l1', 'elasticnet']
alphas = ['0.001', '0.01', '0.1']
l1ratios = ['0.10', '0.15']
epsilons = ['0.0001']

generators = os.listdir('../../substitutions/')

testsetmap = {}
f = open('../evaluators/best_ss.txt')
for line in f:
        data = line.strip().split('\t')
        generator = data[0].strip()
        testsets = data[1:len(data)]
        testsetmap[generator] = testsets
f.close()

for generator in generators:
	print(generator)
	testset = testsetmap[generator]
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
							comm = 'nohup python Run_Boundary.py ../../corpora/lexmturk_gold.txt 1 '+l+' '+p+' '+a+' '+r+' '+e
							comm += ' ../../substitutions/'+generator+'/'+testset+' '+output+' &'
							os.system(comm)
