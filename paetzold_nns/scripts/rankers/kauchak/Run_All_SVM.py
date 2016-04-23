import os

#Parameters:
Cs = ['1']
epsilons = ['0.0001']
kernels = ['0']

generators = os.listdir('../../../substitutions/')
#generators = ['all', 'biran', 'kauchak', 'wordnet']
#generators = ['glavas', 'merriam', 'yamamoto', 'paetzold']
generators = ['allvocab']

best_map = {}
f = open('../../evaluators/best_ss.txt')
for line in f:
        data = line.strip().split('\t')
        gen = data[0].strip()
        sel = data[1].strip()
        file = data[2].strip()
        if gen not in best_map:
                best_map[gen] = {}
        best_map[gen][sel] = file
f.close()

for gen in best_map:
        best_map[gen]['void'] = 'substitutions_void.txt'

counter = -1
for generator in generators:
	selectors = best_map[generator].keys()
        #selectors = ['boundaryUnsupervisedCV']
        for selector in selectors:
		for C in Cs:
			for e in epsilons:
				for k in kernels:
					counter += 1
					output = '../../../rankings/kauchak/ranks_'+generator+'_'+selector+'_'+C+'_'+e+'_'+k+'.txt'
					trfile = './temp/train_feature_file_'+str(counter)+'.txt'
					mfile = './temp/model_'+str(counter)+'.txt'
					tefile = './temp/test_feature_file_'+str(counter)+'.txt'
					sfile = './temp/scores_'+str(counter)+'.txt'
					#comm = 'nohup python Run_SVMRank.py ../../../../semeval/corpora/semeval/semeval_all.txt '+trfile+' '+C+' '+e+' '+k+' '+mfile
					#comm = 'python Run_SVMRank.py ../../../../lexmturk/corpora/lexmturk_all.txt '+trfile+' '+C+' '+e+' '+k+' '+mfile
					comm = 'nohup python Run_SVMRank.py ../../../../lexmturk/corpora/lexmturk_all.txt '+trfile+' '+C+' '+e+' '+k+' '+mfile
					comm += ' '+tefile+' '+sfile
					comm +=' ../../../substitutions/'+generator+'/'+best_map[generator][selector]+' '+output+' &'
					#comm +=' ../../../substitutions/'+generator+'/'+best_map[generator][selector]+' '+output
					os.system(comm)
					#print(comm)
