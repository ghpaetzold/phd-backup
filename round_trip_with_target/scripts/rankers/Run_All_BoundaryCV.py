import os

#Parameters:
positive_ranges = ['1']
folds = ['5', '7', '10']
test_sizes = ['0.25', '0.5', '0.75']

generators = os.listdir('../../substitutions/')

testsets = os.listdir('../../substitutions/kauchak/')
#testsets = []
#testsets.append('substitutions_svmrank_0.125_1_1_0.0001.txt')
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
		for p in positive_ranges:
			for f in folds:
				for t in test_sizes:
					output = '../../rankings/boundaryCV/ranks_'+generator+'_'+selector+'_'+p+'_'+f+'_'+t+'.txt'
					comm = 'nohup python Run_BoundaryCV.py ../../corpora/lexmturk_all.txt '+p+' '+f+' '+t
					comm += ' ../../substitutions/'+generator+'/'+testset+' '+output+' &'
					os.system(comm)
