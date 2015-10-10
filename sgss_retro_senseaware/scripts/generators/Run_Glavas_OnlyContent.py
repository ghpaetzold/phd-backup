import xml.etree.ElementTree as ET
import re
import urllib2 as urllib
from nltk.corpus import wordnet as wn
import subprocess
import nltk
from nltk.tag.stanford import StanfordPOSTagger
import kenlm
import codecs
import os, sys
import gensim
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer

class GlavasGenerator:

	def __init__(self, w2vmodel):
		"""
		Creates a GlavasGenerator instance.
	
		@param w2vmodel: Binary parsed word vector model.
		For more information on how to produce the model, please refer to the LEXenstein Manual.
		"""
		self.lemmatizer = WordNetLemmatizer()
		self.stemmer = PorterStemmer()
		self.model = gensim.models.word2vec.Word2Vec.load_word2vec_format(w2vmodel, binary=True)

	def getSubstitutions(self, victor_corpus, amount):
		"""
		Generates substitutions for the target words of a corpus in VICTOR format.
	
		@param victor_corpus: Path to a corpus in the VICTOR format.
		For more information about the file's format, refer to the LEXenstein Manual.
		@return: A dictionary that assigns target complex words to sets of candidate substitutions.
		Example: substitutions['perched'] = {'sat', 'roosted'}
		"""

		#Get initial set of substitutions:
		substitutions = self.getInitialSet(victor_corpus, amount)
		return substitutions

	def getInitialSet(self, victor_corpus, amount):
		lexf = open(victor_corpus)
		data = []
		for line in lexf:
			d = line.strip().split('\t')
			data.append(d)
		lexf.close()
		
		trgs = []
		trgsstems = []
		trgslemmas = []
		for i in range(0, len(data)):
			d = data[i]
			target = d[1].strip().lower()
			head = int(d[2].strip())
			trgs.append(target)
		trgslemmas = self.lemmatizeWords(trgs)
		trgsstems = self.stemWords(trgs)
		
		trgmap = {}
		for i in range(0, len(trgslemmas)):
			target = data[i][1].strip().lower()
			head = int(data[i][2].strip())
			lemma = trgslemmas[i]
			stem = trgsstems[i]
			trgmap[target] = (lemma, stem)
	
		subs = []
		cands = set([])
		for i in range(0, len(data)):
			d = data[i]

			t = trgs[i]
			tstem = trgsstems[i]
			tlemma = trgslemmas[i]

			word = t

			most_sim = []
			try:
				most_sim = self.model.most_similar(positive=[word], topn=50)
			except KeyError:
				most_sim = []

			subs.append([word[0] for word in most_sim])
			
		subsr = subs
		subs = []
		for l in subsr:
			lr = []
			for inst in l:
				cand = inst.split('|||')[0].strip()
				encc = None
				try:
					encc = cand.encode('ascii')
				except Exception:
					encc = None
				if encc:
					cands.add(cand)
					lr.append(inst)
			subs.append(lr)
			
		cands = list(cands)
		candslemmas = self.lemmatizeWords(cands)
		candsstems = self.stemWords(cands)
		candmap = {}
		for i in range(0, len(cands)):
			cand = cands[i]
			lemma = candslemmas[i]
			stem = candsstems[i]
			candmap[cand] = (lemma, stem)
		
		subs_filtered = self.filterSubs(data, subs, candmap, trgs, trgsstems, trgslemmas)
		
		final_cands = {}
		for i in range(0, len(data)):
			target = data[i][1]
			cands = subs_filtered[i][0:min(amount, subs_filtered[i])]
			cands = [str(word.split('|||')[0].strip()) for word in cands]
			if target not in final_cands:
				final_cands[target] = set([])
			final_cands[target].update(set(cands))
		
		return final_cands
		
	def lemmatizeWords(self, words):
		result = []
		for word in words:
			result.append(self.lemmatizer.lemmatize(word))
		return result
		
	def stemWords(self, words):
		result = []
		for word in words:
			result.append(self.stemmer.stem(word))
		return result
	
	def filterSubs(self, data, subs, candmap, trgs, trgsstems, trgslemmas):
		result = []
		for i in range(0, len(data)):
			d = data[i]

			t = trgs[i]
			tstem = trgsstems[i]
			tlemma = trgslemmas[i]

			word = t

			most_sim = subs[i]
			most_simf = []

			for cand in most_sim:
				cword = cand
				clemma = candmap[cword][0]
				cstem = candmap[cword][1]

				if clemma!=tlemma and cstem!=tstem:
					most_simf.append(cand)

			result.append(most_simf)
		return result

size = sys.argv[1]

victor_corpus = '/export/data/ghpaetzold/benchmarking/lexmturk/corpora/lexmturk_all.txt'

w2v = '/export/data/ghpaetzold/word2vecvectors/models/word_vectors_all_'+size+'_cbow_onlycontent.bin'

folderExists = os.path.isdir('../../substitutions/glavasonlycontent'+size)

if not folderExists:
	kg = GlavasGenerator(w2v)
	subs = kg.getSubstitutions(victor_corpus, 10)
	
	os.system('mkdir ../../substitutions/glavasonlycontent'+size)
	out = open('../../substitutions/glavasonlycontent'+size+'/substitutions.txt', 'w')
	for k in subs.keys():
	        newline = k + '\t'
	        if len(subs[k])>0:
	                for c in subs[k]:
	                        newline += c + '|||'
	                newline = newline[0:len(newline)-3]
	                out.write(newline.strip() + '\n')
	out.close()
else:
	print('Folder already exists!')
