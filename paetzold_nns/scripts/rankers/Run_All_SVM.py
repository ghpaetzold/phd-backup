import os

#Parameters:
Cs = ['0.01', '0.1']
epsilons = ['0.0001', '0.001']
kernels = ['0', '1', '2', '3']

generators = os.listdir('../../substitutions/')
#generators = ['yamamoto']

testsets = []
testsets.append('substitutions_svmrank_0.125_1_1_0.0001.txt')
#testsets.append('substitutions_boundaryCV_0.5.txt')
#testsets.append('substitutions_WSD_enhancedlesk.txt')
#testsets.append('substitutions_wordvector_0.125_HasStop_0_True_True_True.txt')
#testsets.append('substitutions_void.txt')
#testsets.append('substitutions_biran_0.0_0.8.txt')
#testsets.append('substitutions_WSD_first.txt')
#testsets.append('substitutions_WSD_lesk.txt')
#testsets.append('substitutions_WSD_path.txt')
#testsets.append('substitutions_WSD_random.txt')

counter = -1
for generator in generators:
	print(generator)
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
					comm = 'nohup python Run_SVMRank.py ../../corpora/lexmturk_all.txt '+trfile+' '+C+' '+e+' '+k+' '+mfile
					comm += ' '+tefile+' '+sfile
					comm +=' ../../substitutions/'+generator+'/'+testset+' '+output+' &'
					os.system(comm)
					#print(comm)
