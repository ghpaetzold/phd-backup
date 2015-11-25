import os

#Parameters:
Cs = ['1']
epsilons = ['0.001']
kernels = ['2']

generators = os.listdir('../../../substitutions/')
#generators = ['kauchak']

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

datasets = {}
datasets['semeval'] = '../../../../semeval/corpora/semeval/semeval_all.txt'
datasets['nnsimplex'] = '../../../../sr_userstudy/corpora/NNSimpLex.txt'
datasets['lexmturk'] = '../../../../lexmturk/corpora/lexmturk_all.txt'
datasets['debelder'] = '../../../../../dataset_benchmarking/DeBelder_VICTOR_inflected.txt'

counter = -1
for generator in generators:
	#selectors = best_map[generator].keys()
        selectors = ['void']
        for selector in selectors:
		for C in Cs:
			for e in epsilons:
				for k in kernels:
					for dataset in datasets:
						os.system('mkdir ../../../dt_rankings/'+dataset)
						os.system('mkdir ../../../dt_rankings/'+dataset+'/kauchak')
						counter += 1
						output = '../../../dt_rankings/'+dataset+'/kauchak/ranks_'+generator+'_'+selector+'_'+C+'_'+e+'_'+k+'.txt'
						trfile = './temp/train_feature_file_'+str(counter)+'.txt'
						mfile = './temp/model_'+str(counter)+'.txt'
						tefile = './temp/test_feature_file_'+str(counter)+'.txt'
						sfile = './temp/scores_'+str(counter)+'.txt'
						comm = 'nohup python Run_SVMRank.py '+datasets[dataset]+' '+trfile+' '+C+' '+e+' '+k+' '+mfile
						comm += ' '+tefile+' '+sfile
						comm +=' ../../../substitutions/'+generator+'/'+best_map[generator][selector]+' '+output+' &'
						os.system(comm)
						#print(comm)
