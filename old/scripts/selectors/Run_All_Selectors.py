import os

def getPrefix(selector):
	return selector.strip().split('.')[0].strip().lower()
	
subfolder = '/export/data/ghpaetzold/benchmark/corpora/substitutions/'
selfolder = '/export/data/ghpaetzold/benchmark/scripts/selectors/'

#methods = ['biran', 'kauchak', 'merriam', 'wordnet', 'yamamoto']
methods = ['biran']
selectors = set(os.listdir(selfolder))
selectors.remove('Enhanced_Lesk.py')
selectors.remove('Run_All_Selectors.py')
#selectors.remove('No_Selection.py')


print(str(selectors))

comm = 'nohup python '

for method in methods:
	for selector in selectors:
		sel_prefix = getPrefix(selector)
		subs_path = subfolder + method + '/substitutions.txt'
		out_path = subfolder + method + '/substitutions.' + sel_prefix + '.txt'
		temp_path = subfolder + method + '/temp/'
		os.system(comm + selfolder + selector + ' ' + subs_path + ' ' + out_path + ' ' + temp_path + ' &')
