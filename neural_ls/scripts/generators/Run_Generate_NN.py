import os

included = set(os.listdir('../../substitutions'))

files = os.listdir('../../models/')
models = set([])
for file in files:
	models.add(file.split(r'.')[0])

for model in models:
#	if model not in included:
		comm = 'nohup python Generate_NN.py ' + model + ' &'
		os.system(comm)

