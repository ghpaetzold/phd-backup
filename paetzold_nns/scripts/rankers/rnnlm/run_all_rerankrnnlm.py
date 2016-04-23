import os

valids = ['ssuserstudy', 'lexmturk', 'nnseval', 'all']
#valids = ['ssuserstudy']

for valid in valids:
	comm = 'nohup python run_rerankrnnlm.py '+valid+' &'
	#comm = 'python run_rerankrnnlm.py '+valid
	os.system(comm)
