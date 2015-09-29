from lexenstein.generators import *
from lexenstein.morphadorner import *
from lexenstein.spelling import *
import sys
import os

victor_corpus = sys.argv[1].strip()
w2vmodel = sys.argv[2].strip()
output = sys.argv[3].strip()

kg = GlavasGenerator(w2vmodel)

amounts = ['5', '10', '15', '20', '25']
for amount in amounts:
	if not os.path.isfile(output+'_'+amount):
		subs = kg.getSubstitutions(victor_corpus, int(amount))
	
		out = open(output+'_'+amount, 'w')
		for k in subs.keys():
			newline = k + '\t'
			if len(subs[k])>0:
				for c in subs[k]:
					newline += c + '|||'
				newline = newline[0:len(newline)-3]
				out.write(newline.strip() + '\n')
		out.close()
		
