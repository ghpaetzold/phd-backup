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

#methods = ['all', 'biran', 'kauchak', 'merriam', 'wordnet', 'yamamoto']
#prefixes = getPrefixes()
models = os.listdir('./models/')

#for method in methods:
#	print('For method ' + method + ':')
#	for prefix in prefixes:
for model in models:
	svm_model_path = './models/'+model
	svm_values_path = './features/train/training_features.txt'
	ranking_path = './rankings/train/rankings.'+model+'.txt'
	comm = 'nohup /export/tools/svm-rank/svm_rank_classify '+svm_values_path +' '+svm_model_path+' '+ranking_path+' &'
	print(str(comm))
	os.system(comm)
