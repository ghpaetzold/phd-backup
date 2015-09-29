import os

sizes = range(50, 550, 50)
sizes = [str(size) for size in sizes]

dataset = '../../corpora/datasets/training_synonyms_antonymsnonorm.txt'

for size in sizes:
	comm = 'nohup python glavas_selected.py ' + dataset + ' ' + size + ' &'
	os.system(comm)
