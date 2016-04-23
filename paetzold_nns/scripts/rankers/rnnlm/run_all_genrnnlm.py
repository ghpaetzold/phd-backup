import os

valids = ['ssuserstudy', 'lexmturk', 'nnseval', 'all']

generators = os.listdir('../../../substitutions/')

os.system('mkdir ../../../rankings/rnnlm/')

for valid in valids:
	for generator in generators:
		comm = 'nohup python run_genrnnlm.py '+valid+' '+generator+' &'
		os.system(comm)
