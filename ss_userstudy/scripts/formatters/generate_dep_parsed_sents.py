from nltk.parse.stanford import StanfordParser
from lexenstein.util import *
import os, sys

input = sys.argv[1]
output = sys.argv[2]

stanford_parser = '/export/data/ghpaetzold/generalpurpose/binaryfeatureslex/stanford/stanford-parser/stanford-parser.jar'
dependency_models = '/export/data/ghpaetzold/generalpurpose/binaryfeatureslex/stanford/stanford-parser/stanford-parser-3.4.1-models.jar'
java = '/usr/bin/java'

os.environ['JAVAHOME'] = java
parser = StanfordParser(path_to_jar=stanford_parser, path_to_models_jar=dependency_models)

f = open(input)
sentences = []
for line in f:
	sentences.append(line.strip().split('\t')[0].strip().split(' '))
f.close()

print('Tagging...')
dep_parsed_sents = parser = dependencyParseSentences(parser, sentences)
print('Tagged!')

o = open(output, 'w')
for inst in dep_parsed_sents:
	line = ''
	for dep in inst:
		line += dep[0]+'|||'+dep[1]+'|||'+dep[2]+'|||'+dep[3]+'|||'+dep[4] + '\t'
	o.write(line.strip() + '\n')	
o.close()
