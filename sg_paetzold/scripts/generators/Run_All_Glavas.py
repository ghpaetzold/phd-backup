import os

def getData(model):
	ann = None
	if 'generalized' in model and 'retrofitted' in model:
		ann = 'retroannotated'
	elif 'generalized' in model and 'retrofitted' not in model:
		ann = 'annotated'
	elif 'generalized' not in model and 'retrofitted' in model:
		ann = 'retro'
	else:
		ann = 'normal'

	size = None
	if '300' in model:
		size = '300'
	elif '500' in model:
		size = '500'
	else:
		size = '700'

	arc = 'skip'
	if 'cbow' in model:
		arc = 'cbow'
	return ann, size, arc

#Parameters:
folder = '/export/data/ghpaetzold/word2vecvectors/models/'
sizes = ['500']
archs = ['cbow', 'skip']
retros = [True, False]

#Get models:
models = set([])
mprefix = 'word_vectors_all_'
for size in sizes:
	for arch in archs:
		for retro in retros:
			model = str(mprefix)
			model += size + '_'
			model += arch
			if retro:
				model += '_retrofitted'
			model += '.bin'
			models.add(model)
print(str(models))

dataset = '/export/data/ghpaetzold/benchmarking/lexmturk/corpora/lexmturk_all.txt'

for model in models:
	ann, size, arc = getData(model)
	output = '../../substitutions/'+ann+'_'+size+'_'+arc
	comm = 'nohup python Run_Glavas.py ' + dataset + ' ' + folder+model + ' ' + output + ' &'
	print(comm)
	os.system(comm)
