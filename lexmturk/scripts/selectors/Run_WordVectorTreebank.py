import sys
import pywsd
import gensim
from scipy.spatial.distance import cosine
import nltk
from nltk.tag.stanford import StanfordTagger
import numpy as np
import os

generator = sys.argv[1]
victor_corpus = sys.argv[2]
proportion = float(sys.argv[3])
stop_words_file = sys.argv[4]
if stop_words_file=='None':
	stop_words_file = None
window = int(sys.argv[5].strip())
onlyInformative = False
if sys.argv[6].strip()=='True':
	onlyInformative = True
keepTarget = False
if sys.argv[7].strip()=='True':
	keepTarget = True
onePerWord = False
if sys.argv[8].strip()=='True':
	onePerWord = True
out = sys.argv[9].strip()

class VoidSelector:

	def selectCandidates(self, substitutions, victor_corpus):
		"""
		Selects which candidates can replace the target complex words in each instance of a VICTOR corpus.
	
		@param substitutions: Candidate substitutions to be filtered.
		It can be in two formats:
		A dictionary produced by a Substitution Generator linking complex words to a set of candidate substitutions.
		Example: substitutions['perched'] = {'sat', 'roosted'}
		A list of candidate substitutions selected for the "victor_corpus" dataset by a Substitution Selector.
		Example: [['sat', 'roosted'], ['easy', 'uncomplicated']]
		@param victor_corpus: Path to a corpus in the VICTOR format.
		For more information about the file's format, refer to the LEXenstein Manual.
		@return: Returns a vector of size N, containing a set of selected substitutions for each instance in the VICTOR corpus.
		"""
		selected_substitutions = []

		if isinstance(substitutions, list):
			return substitutions	

		lexf = open(victor_corpus)
		for line in lexf:
			data = line.strip().split('\t')
			sent = data[0].strip()
			target = data[1].strip()
		
			candidates = []
			if target in substitutions.keys():
				candidates = substitutions[target]
		
			selected_substitutions.append(candidates)
		lexf.close()
		return selected_substitutions
		
	def toVictorFormat(self, victor_corpus, substitutions, output_path, addTargetAsCandidate=False):
		"""
		Saves a set of selected substitutions in a file in VICTOR format.
	
		@param victor_corpus: Path to the corpus in the VICTOR format to which the substitutions were selected.
		@param substitutions: The vector of substitutions selected for the VICTOR corpus.
		@param output_path: The path in which to save the resulting VICTOR corpus.
		@param addTargetAsCandidate: If True, adds the target complex word of each instance as a candidate substitution.
		"""
		o = open(output_path, 'w')
		f = open(victor_corpus)
		for subs in substitutions:
			data = f.readline().strip().split('\t')
			sentence = data[0].strip()
			target = data[1].strip()
			head = data[2].strip()
			
			newline = sentence + '\t' + target + '\t' + head + '\t'
			for sub in subs:
				newline += '0:'+sub + '\t'
			o.write(newline.strip() + '\n')
		f.close()
		o.close()

class WordVectorSelector:
	
	def __init__(self, vector_model):
		"""
		Creates an instance of the WordVectorSelector class.
	
		@param vector_model: Path to a binary word vector model.
		For instructions on how to create the model, please refer to the LEXenstein Manual.
		"""
		self.model = gensim.models.word2vec.Word2Vec.load_word2vec_format(vector_model, binary=True)
	
	def selectCandidates(self, substitutions, victor_corpus, proportion=1.0, stop_words_file=None, window=99999, onlyInformative=False, keepTarget=False, onePerWord=False):
		"""
		Selects which candidates can replace the target complex words in each instance of a VICTOR corpus.
	
		@param substitutions: Candidate substitutions to be filtered.
		It can be in two formats:
		A dictionary produced by a Substitution Generator linking complex words to a set of candidate substitutions.
		Example: substitutions['perched'] = {'sat', 'roosted'}
		A list of candidate substitutions selected for the "victor_corpus" dataset by a Substitution Selector.
		Example: [['sat', 'roosted'], ['easy', 'uncomplicated']]
		@param victor_corpus: Path to a corpus in the VICTOR format.
		For more information about the file's format, refer to the LEXenstein Manual.
		@param proportion: Percentage of substitutions to keep.
		@param stop_words_file: Path to the file containing stop words of the desired language.
		The file must contain one stop word per line.
		@param window: Number of tokens around the target complex sentence to consider as its context.
		@param onlyInformative: If True, only content words are considered as part of the complex word's context, such as nouns, verbs, adjectives and adverbs.
		@param keepTarget: If True, the complex target word is also included as part of its context.
		@param onePerWord: If True, a word in the complex word's context can only contribute once to its resulting word vector.
		@return: Returns a vector of size N, containing a set of selected substitutions for each instance in the VICTOR corpus.
		"""
		stop_words = set([])
		if stop_words_file != None:
			stop_words = set([word.strip() for word in open(stop_words_file)])
	
		selected_substitutions = []

		substitution_candidates = []
		if isinstance(substitutions, list):
			substitution_candidates = substitutions
		elif isinstance(substitutions, dict):
			void = VoidSelector()
			substitution_candidates = void.selectCandidates(substitutions, victor_corpus)
		else:
			print('ERROR: Substitutions are neither a dictionary or a list!')
			return selected_substitutions			

		c = -1
		lexf = open(victor_corpus)
		for line in lexf:
			c += 1
			data = line.strip().split('\t')
			sent = data[0].strip()
			target = data[1].strip()
			head = int(data[2].strip())
			pos_tokens = []
			try:
				pos_tokens = nltk.pos_tag(sent.split(' '))
			except UnicodeDecodeError:
				pos_tokens = sent.split(' ')

			target_vec = self.getSentVec(sent, head, stop_words, window, onlyInformative, keepTarget, onePerWord, pos_tokens)
		
			candidates = substitution_candidates[c]

			candidate_dists = {}
			for candidate in candidates:
				candidate_vec = self.getWordVec(candidate, pos_tokens[head][1].strip())
				try:
					candidate_dists[candidate] = cosine(candidate_vec, target_vec)
				except ValueError:
					candidate_dists = candidate_dists

			final_candidates = self.getFinalCandidates(candidate_dists, proportion)

			selected_substitutions.append(final_candidates)
		lexf.close()
		return selected_substitutions
		
	def getSentVec(self, sentence, head, stop_words, window, onlyInformative, keepTarget, onePerWord, pos_tokens):
		informative_tags = set([])
		if onlyInformative:
			informative_tags = set(['nn', 'nns', 'jj', 'jjs', 'jjr', 'vb', 'vbd', 'vbg', 'vbn', 'vbp', 'vbz', 'rb', 'rbr', 'rbs'])
		
		tokensr = sentence.split(' ')
		
		tokens = []
		for i in range(0, len(tokensr)):
			token = tokensr[i]
			tokens.append(token+'|||'+pos_tokens[i][1].strip())

		valid_tokens = []
		if keepTarget:
			valid_tokens.append(tokens[head].strip())
		
		if head>0:
			for i in range(max(0, head-window), head):
				if len(informative_tags)==0 or pos_tokens[i][1].lower().strip() in informative_tags:
					if tokens[i] not in stop_words:
						valid_tokens.append(tokens[i])
		
		if head<len(tokens)-1:
			for i in range(head+1, min(len(tokens), head+1+window)):
				if len(informative_tags)==0 or pos_tokens[i][1].lower().strip() in informative_tags:
					if tokens[i] not in stop_words:
						valid_tokens.append(tokens[i])
						
		if onePerWord:
			valid_tokens = list(set(valid_tokens))
		
		result = []
		for	token in valid_tokens:
			if len(result)==0:
				try:
					result = self.model[token]
				except KeyError:
					try:
						result = self.model[token.lower()]
					except KeyError:
						result = []
			else:
				try:
					result = np.add(result, self.model[token])
				except KeyError:
					try:
						result = np.add(result, self.model[token.lower()])
					except KeyError:
						result = result
		return result
		
	def getWordVec(self, candidate, tag):
		result = []
		try:
			result = self.model[candidate+'|||'+tag]
		except KeyError:
			try:
				result = self.model[candidate.lower()+'|||'+tag]
			except KeyError:
				result = result
		return result
				
	def getFinalCandidates(self, candidate_dists, proportion):
		result = sorted(list(candidate_dists.keys()), key=candidate_dists.__getitem__)
		return result[0:max(1, int(proportion*float(len(result))))]
		
	def toVictorFormat(self, victor_corpus, substitutions, output_path, addTargetAsCandidate=False):
		"""
		Saves a set of selected substitutions in a file in VICTOR format.
	
		@param victor_corpus: Path to the corpus in the VICTOR format to which the substitutions were selected.
		@param substitutions: The vector of substitutions selected for the VICTOR corpus.
		@param output_path: The path in which to save the resulting VICTOR corpus.
		@param addTargetAsCandidate: If True, adds the target complex word of each instance as a candidate substitution.
		"""
		o = open(output_path, 'w')
		f = open(victor_corpus)
		for subs in substitutions:
			data = f.readline().strip().split('\t')
			sentence = data[0].strip()
			target = data[1].strip()
			head = data[2].strip()
			
			newline = sentence + '\t' + target + '\t' + head + '\t'
			for sub in subs:
				newline += '0:'+sub + '\t'
			o.write(newline.strip() + '\n')
		f.close()
		o.close()

def getSubs(generator):
	result = {}
	f = open('../../substitutions/' + generator + '/substitutions.txt')
	for line in f:
		data = line.strip().split('\t')
		target = data[0].strip()
		candidates = data[1].strip().split('|||')
		result[target] = candidates
	f.close()
	return result

subs = getSubs(generator)

wordvecselector = WordVectorSelector('/export/data/ghpaetzold/word2vecvectors/models/word_vectors_all_treebank_300_cbow.bin')
selected = wordvecselector.selectCandidates(subs, victor_corpus, proportion=proportion, stop_words_file=stop_words_file, window=window, onlyInformative=onlyInformative, keepTarget=keepTarget, onePerWord=onePerWord)

outf = open(out, 'w')
vicf = open(victor_corpus)
for cands in selected:
	data = vicf.readline().strip().split('\t')
	newline = data[0] + '\t' + data[1] + '\t' + data[2] + '\t'
	for cand in cands:
		newline += '0:'+cand + '\t'
	outf.write(newline.strip() + '\n')
outf.close()
vicf.close()
