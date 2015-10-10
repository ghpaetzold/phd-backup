import os, sys

size = sys.argv[1]
pos_type = sys.argv[2]
retrofitted = sys.argv[3]

#Get model:
prefix = ''
if pos_type=='none' and retrofitted=='0':
	prefix = 'TEM'
if pos_type=='none' and retrofitted=='1':
	prefix = 'REM'
if pos_type=='paetzold' and retrofitted=='0':
	prefix = 'SEM'
if pos_type=='paetzold' and retrofitted=='1':
	prefix = 'RSEM'


model = '/export/data/ghpaetzold/word2vecvectors/models/word_vectors_all_'
if pos_type=='paetzold':
	model += 'generalized_'
model += size+'_cbow'
if retrofitted=='1':
	model += '_retrofitted'
model += '.bin'
print(str(model))

#Generators:
generators = os.listdir('../../substitutions/')
generators = ['all']

#Dataset:
victor_corpus = '/export/data/ghpaetzold/benchmarking/lexmturk/corpora/lexmturk_all.txt'

#Run WordVec selector:
proportions = ['0.5']
stopwordsfiles = ['../../../lexmturk/corpora/stop_words.txt']
windows = ['5']
informatives = ['True']
targets = ['False']
ones = ['True']

os.system('mkdir ../../selections/'+prefix)
out = '../../selections/'+prefix+'/'+size
comm = 'nohup python Run_WordVector.py all ' + victor_corpus + ' 0.5 '
comm += '../../../lexmturk/corpora/stop_words.txt 0 True True True ' + out + ' '
comm += model + ' ' + pos_type + ' &'
os.system(comm)
