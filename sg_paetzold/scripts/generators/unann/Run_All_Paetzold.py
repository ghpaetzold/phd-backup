import os

def getData(model):
	ann = 'normal'
	if 'generalized' in model:
		ann = 'annotated'

	size = '500'
	if '300' in model:
		size = '300'

	arc = 'skip'
	if 'cbow' in model:
		arc = 'cbow'
	return ann, size, arc

#Parameters:
folder = '/export/data/ghpaetzold/word2vecvectors/models/'
models = set(os.listdir(folder))
modelsr = set([])
for m in models:
	if 'generalized' not in m and 'treebank' not in m:
		modelsr.add(m)
models = modelsr
print(str(models))

amounts = ['10', '15', '20', '25']

dataset = '/export/data/ghpaetzold/benchmarking/lexmturk/corpora/lexmturk_all.txt'

for model in models:
	for amount in amounts:
		ann, size, arc = getData(model)
		output = '../../../substitutions/'+ann+'_'+size+'_'+arc+'_'+amount
		comm = 'nohup python Run_Paetzold.py ' + dataset + ' ' + folder+model + ' ' + amount + ' ' + output + ' &'
		print(comm)
		os.system(comm)
