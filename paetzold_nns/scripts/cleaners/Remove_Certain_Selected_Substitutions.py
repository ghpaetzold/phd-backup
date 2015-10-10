import os, sys

selector = sys.argv[1]

generators = os.listdir('../../substitutions/')
for generator in generators:
	os.chdir('../../substitutions/'+generator+'/')
	os.system('rm substitutions_'+selector+'*')

