import os

generators = os.listdir('../../substitutions/')
for generator in generators:
	os.chdir('../../substitutions/'+generator+'/')
	os.system('rm substitutions_*')

