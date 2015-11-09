import os

files = set(os.listdir('./'))
files.remove('Run_All.py')
files.remove('lexenstein')
files.remove('Create_All.py')
files.remove('old')
#files = set(['Run_Merriam.py'])

victor_corpus = '../../corpora/lexmturk_all.txt'

for file in files:
	os.system('nohup python ' + file + ' ' + victor_corpus + ' &')
