import os

#Parameters:
Cs = ['0.01', '0.1']
epsilons = ['0.0001', '0.001']
kernels = ['0', '1', '2', '3']

generators = os.listdir('../../substitutions/')

testsetmap = {}
f = open('../evaluators/best_ss.txt')
for line in f:
        data = line.strip().split('\t')
        generator = data[0].strip()
        testsets = data[1:len(data)]
        testsetmap[generator] = testsets
f.close()

counter = -1
for generator in generators:
	print(generator)
	testset = testsetmap[generator]
	for testset in testsets:
		testsetd = testset.strip().split('_')
		selector = testsetd[1].strip()
		if selector == 'WSD':
			selector = testsetd[2].strip()
		for C in Cs:
			for e in epsilons:
				for k in kernels:
					counter += 1
					output = '../../rankings/svm/ranks_'+generator+'_'+selector+'_'+C+'_'+e+'_'+k+'.txt'
					trfile = './temp/train_feature_file_'+str(counter)+'.txt'
					mfile = './temp/model_'+str(counter)+'.txt'
					tefile = './temp/test_feature_file_'+str(counter)+'.txt'
					sfile = './temp/scores_'+str(counter)+'.txt'
					comm = 'nohup python Run_SVMRank.py ../../corpora/lexmturk_gold.txt '+trfile+' '+C+' '+e+' '+k+' '+mfile
					comm += ' '+tefile+' '+sfile
					comm +=' ../../substitutions/'+generator+'/'+testset+' '+output+' &'
					os.system(comm)
					#print(comm)
