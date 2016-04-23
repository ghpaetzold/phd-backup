import os

#Parameters:
Cs = ['0.01', '0.1']
epsilons = ['0.0001', '0.001']
kernels = ['0', '2', '3']

generators = os.listdir('../../substitutions/')
generators = ['kauchak']

best_map = {}
f = open('../evaluators/best_ss.txt')
for line in f:
        data = line.strip().split('\t')
        gen = data[0].strip()
        sel = data[1].strip()
        file = data[2].strip()
        if gen not in best_map:
                best_map[gen] = {}
        best_map[gen][sel] = file
f.close()

counter = -1
for generator in generators:
#	for selector in best_map[generator]:
	for selector in ['void']:
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
					comm +=' ../../substitutions/'+generator+'/'+best_map[generator][selector]+' '+output+' &'
					os.system(comm)
					#print(comm)
