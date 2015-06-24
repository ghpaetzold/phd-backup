import os

#Parameters:
positive_ranges = ['1']
folds = ['5', '7', '10']
test_sizes = ['0.25', '0.5', '0.75']

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
	testsets = testsetmap[generator]
	for testset in testsets:
		testsetd = testset.strip().split('_')
		selector = testsetd[1].strip()
		if selector == 'WSD':
			selector = testsetd[2].strip()
		for p in positive_ranges:
			for f in folds:
				for t in test_sizes:
					output = '../../rankings/boundaryCV/ranks_'+generator+'_'+selector+'_'+p+'_'+f+'_'+t+'.txt'
					comm = 'nohup python Run_BoundaryCV.py ../../corpora/lexmturk_gold.txt '+p+' '+f+' '+t
					comm += ' ../../substitutions/'+generator+'/'+testset+' '+output+' &'
					os.system(comm)
