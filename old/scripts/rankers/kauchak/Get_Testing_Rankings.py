import os

def getPrefixes():
        files = os.listdir('../../../corpora/substitutions/biran/')
        result = set([])
        for file in files:
                if file.startswith('substitutions'):
                        if len(file.split('.'))>2:
                                prefix = file.split('.')[1].strip()
                                result.add(prefix)
        return result

methods = ['all', 'biran', 'kauchak', 'merriam', 'wordnet', 'yamamoto']
prefixes = getPrefixes()
models = os.listdir('./models/')

for method in methods:
	print('For method ' + method + ':')
	for prefix in prefixes:
		svm_model_path = './models/model_0.1_0.01_0.dat'
		svm_values_path = './features/test/features.'+method+'.'+prefix+'.txt'
		ranking_path = './rankings/test/rankings.'+method+'.'+prefix+'.txt'
		comm = 'nohup /export/tools/svm-rank/svm_rank_classify '+svm_values_path +' '+svm_model_path+' '+ranking_path+' &'
		print(str(comm))
		os.system(comm)
