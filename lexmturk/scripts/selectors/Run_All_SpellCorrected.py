from lexenstein.spelling import *
import os

generators = os.listdir('../../substitutions/')
victor_corpus = '../../corpora/lexmturk_all.txt'

for generator in generators:
	out = '../../substitutions/'+generator+'/'
	out += 'substitutions_spellcorrected.txt'
	comm = 'nohup python Run_SpellCorrected.py ' + generator + ' ' + victor_corpus + ' ' + out + ' &'
	os.system(comm)
