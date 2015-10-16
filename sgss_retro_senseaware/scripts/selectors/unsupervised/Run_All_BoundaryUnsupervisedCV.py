import os, sys

type = sys.argv[1]

model = None
pos_type = None
retrofitted = None
size = '500'
arch = 'cbow'

#Open model:
mpath = '/export/data/ghpaetzold/word2vecvectors/models/word_vectors_all_'
if 'S' in type:
        mpath += 'generalized_'
mpath += size + '_' + arch
if 'R' in type:
        mpath += '_retrofitted'
mpath += '.bin'

model = mpath
if 'S' in type:
	pos_type = 'paetzold'
else:
	pos_type = 'none'
if 'R' in type:
	retrofitted = '1'
else:
	retrofitted = '0'

#Create prefix:
prefix = 'ubr'
if pos_type=='none':
        if retrofitted=='1':
                prefix += 'REM'
        else:
                prefix += 'TEM'
elif pos_type=='paetzold':
        if retrofitted=='1':
                prefix += 'RSEM'
        else:
                prefix += 'SEM'

#Generators:
generators = os.listdir('../../../substitutions/')
generators = ['all']
#generators = ['glavas1300', 'glavas_retrofitted1300', 'paetzold1300', 'paetzold_retrofitted1300']

#Dataset:
train_victor_corpus = '../../../substitutions/all/substitutions_unsupervised.txt'
test_victor_corpus = '/export/data/ghpaetzold/benchmarking/lexmturk/corpora/lexmturk_all.txt'

#Parameters:
rs = ['1']
fs = ['5']
ts = ['0.75']
ks = ['all']
ks = ['8']
proportions = ['0.5'] 

#Run Boundary selector:
c = 0
for generator in generators:
	train_victor_corpus = '../../../substitutions/all/substitutions_unsupervised.txt'
	for proportion in proportions:
		for positive_range in rs:
			for folds in fs:
				for test_size in ts:
					for k in ks:
						c += 1
						temp_file = './temp/temp_file_boundary_' + str(c) + '.txt'
						out = '../../../substitutions/'+generator+'/'
						out += 'substitutions_'+prefix+'_'+proportion+'_'+positive_range+'_'+folds+'_'+test_size+'_'+k+'.txt'
						comm = 'nohup python Run_BoundaryUnsupervisedCV.py ' + generator + ' ' + train_victor_corpus + ' ' + test_victor_corpus + ' '
						comm += positive_range+' '+folds + ' ' + test_size +' 0 '
						comm += '0 0 0 0 ' + k + ' ' + temp_file + ' ' + proportion + ' ' + out + ' '
						comm += model + ' ' + pos_type + ' &'
						os.system(comm)
