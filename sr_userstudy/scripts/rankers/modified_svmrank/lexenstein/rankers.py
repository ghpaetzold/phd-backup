import os
from sklearn.preprocessing import normalize
from sklearn.feature_selection import f_classif
from sklearn import linear_model
import kenlm
import math
from nltk.corpus import wordnet as wn

class BottRanker:

	def __init__(self, simple_lm):
		"""
		Creates an instance of the BottRanker class.
	
		@param simple_lm: Path to a language model built over simple text.
		For more information on how to create the file, refer to the LEXenstein Manual.
		"""
		
		self.simple_lm = kenlm.LanguageModel(simple_lm)
		
	def getRankings(self, victor_corpus, a1=1.0, a2=1.0):
		"""
		Ranks candidates with respect to their simplicity.
	
		@param victor_corpus: Path to a testing corpus in VICTOR format.
		For more information about the file's format, refer to the LEXenstein Manual.
		@return: A list of ranked candidates for each instance in the VICTOR corpus, from simplest to most complex.
		"""
		#Create object for results:
		result = []
		
		#Read feature values for each candidate in victor corpus:
		f = open(victor_corpus)
		for line in f:
			#Get all substitutions in ranking instance:
			data = line.strip().split('\t')
			substitutions = data[3:len(data)]
			
			#Create dictionary of substitution to feature value:
			scores = {}
			for substitution in substitutions:
				word = substitution.strip().split(':')[1].strip()
				scores[word] = self.getCandidateComplexity(word, a1, a2)
			
			#Sort substitutions:
			sorted_substitutions = sorted(scores.keys(), key=scores.__getitem__, reverse=False)
		
			#Add them to result:
			result.append(sorted_substitutions)
		f.close()
		
		#Return result:
		return result
		
	def getCandidateComplexity(self, word, a1, a2):
		ScoreWL = 0
		if len(word)>4:
			ScoreWL = math.sqrt(len(word)-4)
		ScoreFreq = -1*self.simple_lm.score(word, bos=False, eos=False)
		return a1*ScoreWL + a2*ScoreFreq

class YamamotoRanker:

	def __init__(self, simple_lm, cooc_model):
		"""
		Creates an instance of the YamamotoRanker class.
	
		@param simple_lm: Path to a language model built over simple text.
		For more information on how to create the file, refer to the LEXenstein Manual.
		@param cooc_model: Path to a word co-occurrence model.
		For instructions on how to create the model, please refer to the LEXenstein Manual.
		"""
		
		self.simple_lm = kenlm.LanguageModel(simple_lm)
		self.cooc_model = self.getModel(cooc_model)
		
	def getRankings(self, victor_corpus, a1=1.0, a2=1.0, a3=1.0, a4=1.0, a5=1.0):
		"""
		Ranks candidates with respect to their simplicity.
	
		@param victor_corpus: Path to a testing corpus in VICTOR format.
		For more information about the file's format, refer to the LEXenstein Manual.
		@return: A list of ranked candidates for each instance in the VICTOR corpus, from simplest to most complex.
		"""
		#Create object for results:
		result = []
		
		#Read feature values for each candidate in victor corpus:
		f = open(victor_corpus)
		for line in f:
			#Get all substitutions in ranking instance:
			data = line.strip().split('\t')
			sent = data[0].strip()
			target = data[1].strip()
			head = int(data[2].strip())
			substitutions = data[3:len(data)]
			
			#Create dictionary of substitution to feature value:
			scores = {}
			for substitution in substitutions:
				word = substitution.strip().split(':')[1].strip()
				scores[word] = self.getCandidateScore(sent, target, head, word, a1, a2, a3, a4, a5)
			
			#Sort substitutions:
			sorted_substitutions = sorted(scores.keys(), key=scores.__getitem__, reverse=True)
		
			#Add them to result:
			result.append(sorted_substitutions)
		f.close()
		
		#Return result:
		return result
		
	def getModel(self, path):
		result = {}
		f = open(path)
		for line in f:
			data = line.strip().split('\t')
			target = data[0].strip()
			coocs = data[1:len(data)]
			result[target] = {}
			for cooc in coocs:
				coocd = cooc.strip().split(':')
				word = coocd[0].strip()
				count = int(coocd[1].strip())
				result[target][word] = count
		return result
		
	def getCandidateScore(self, sent, target, head, word, a1, a2, a3, a4, a5):
		Fcorpus = a1*self.simple_lm.score(word, bos=False, eos=False)
		Sense = a2*self.getSenseScore(word, target)
		Cooc = a3*self.getCoocScore(word, sent)
		Log = a4*self.getLogScore(Cooc, sent, word)
		Trigram = a5*self.getTrigramScore(sent, head, word)
		
		score = Fcorpus+Sense+Cooc+Log+Trigram
		return score
	
	def getTrigramScore(self, sent, head, word):
		tokens = ['', ''] + sent.strip().split(' ') + ['', '']
		h = head + 2
		t1 = tokens[h-2] + ' ' + tokens[h-1] + ' ' + word
		t2 = tokens[h-1] + ' ' + word + ' ' + tokens[h+1]
		t3 = word + ' ' + tokens[h+1] + ' ' + tokens[h+2]
		bos = False
		eos = False
		if tokens[h-1]=='':
			bos = True
		if tokens[h+1]=='':
			eos = True
		result = self.simple_lm.score(t1, bos=bos, eos=eos)+self.simple_lm.score(t2, bos=bos, eos=eos)+self.simple_lm.score(t3, bos=bos, eos=eos)
		return result
	
	def getLogScore(self, Cooc, sent, word):
		dividend = Cooc
		divisor = self.simple_lm.score(word, bos=False, eos=False)*self.simple_lm.score(sent, bos=True, eos=True)
		if divisor==0:
			return 0
		else:
			result = 0
			try:
				result = math.log(dividend/divisor)
			except ValueError:
				result = 0
			return result
		
	def getCoocScore(self, word, sent):
		tokens = sent.strip().split(' ')
		if word not in self.cooc_model.keys():
			return 0
		else:
			result = 0
			for token in tokens:
				if token in self.cooc_model[word].keys():
					result += self.cooc_model[word][token]
			return result
		
	def getSenseScore(self, word, target):
		candidate_sense = None
		try:
			candidate_sense = wn.synsets(word)[0]
		except Exception:
			candidate_sense = None
		target_sense = None
		try:
			target_sense = wn.synsets(target)[0]
		except Exception:
			target_sense = None
		result = 999999
		if candidate_sense and target_sense:
			result = candidate_sense.shortest_path_distance(target_sense)
		if not result:
			result = 999999
		return result

class BiranRanker:

	def __init__(self, complex_lm, simple_lm):
		"""
		Creates an instance of the BiranRanker class.
	
		@param complex_lm: Path to a language model built over complex text.
		For more information on how to create the file, refer to the LEXenstein Manual.
		@param simple_lm: Path to a language model built over simple text.
		For more information on how to create the file, refer to the LEXenstein Manual.
		"""
		
		self.complex_lm = kenlm.LanguageModel(complex_lm)
		self.simple_lm = kenlm.LanguageModel(simple_lm)
		
	def getRankings(self, victor_corpus):
		"""
		Ranks candidates with respect to their simplicity.
	
		@param victor_corpus: Path to a testing corpus in VICTOR format.
		For more information about the file's format, refer to the LEXenstein Manual.
		@return: A list of ranked candidates for each instance in the VICTOR corpus, from simplest to most complex.
		"""
		#Create object for results:
		result = []
		
		#Read feature values for each candidate in victor corpus:
		f = open(victor_corpus)
		for line in f:
			#Get all substitutions in ranking instance:
			data = line.strip().split('\t')
			substitutions = data[3:len(data)]
			
			#Create dictionary of substitution to feature value:
			scores = {}
			for substitution in substitutions:
				word = substitution.strip().split(':')[1].strip()
				scores[word] = self.getCandidateComplexity(word)
			
			#Sort substitutions:
			sorted_substitutions = sorted(scores.keys(), key=scores.__getitem__, reverse=False)
		
			#Add them to result:
			result.append(sorted_substitutions)
		f.close()
		
		#Return result:
		return result
		
	def getCandidateComplexity(self, word):
		C = (self.complex_lm.score(word, bos=False, eos=False))/(self.simple_lm.score(word, bos=False, eos=False))
		L = float(len(word))
		return C*L

class BoundaryRanker:

	def __init__(self, fe):
		"""
		Creates an instance of the BoundaryRanker class.
	
		@param fe: A configured FeatureEstimator object.
		"""
		
		self.fe = fe
		self.classifier = None
		
	def trainRanker(self, victor_corpus, positive_range, loss, penalty, alpha, l1_ratio, epsilon):
		"""
		Trains a Boundary Ranker according to the parameters provided.
	
		@param victor_corpus: Path to a training corpus in VICTOR format.
		For more information about the file's format, refer to the LEXenstein Manual.
		@param positive_range: Maximum rank to which label 1 is assigned in the binary classification setup.
		Recommended value: 1.
		@param loss: Loss function to be used.
		Values available: hinge, log, modified_huber, squared_hinge, perceptron.
		@param penalty: Regularization term to be used.
		Values available: l2, l1, elasticnet.
		@param alpha: Constant that multiplies the regularization term.
		Recommended values: 0.0001, 0.001, 0.01, 0.1
		@param l1_ratio: Elastic net mixing parameter.
		Recommended values: 0.05, 0.10, 0.15
		@param epsilon: Acceptable error margin.
		Recommended values: 0.0001, 0.001
		"""
	
		#Read victor corpus:
		data = []
		f = open(victor_corpus)
		for line in f:
			data.append(line.strip().split('\t'))
		f.close()
		
		#Create matrixes:
		X = self.fe.calculateFeatures(victor_corpus)
		Y = self.generateLabels(data, positive_range)
	
		#Train classifier:
		self.classifier = linear_model.SGDClassifier(loss=loss, penalty=penalty, alpha=alpha, l1_ratio=l1_ratio, epsilon=epsilon)
		self.classifier.fit(X, Y)
		
	def getRankings(self, victor_corpus):
		"""
		Ranks candidates with respect to their simplicity.
		Requires for the trainRanker function to be previously called so that a model can be trained.
	
		@param victor_corpus: Path to a testing corpus in VICTOR format.
		For more information about the file's format, refer to the LEXenstein Manual.
		@return: A list of ranked candidates for each instance in the VICTOR corpus, from simplest to most complex.
		"""
		
		#Read victor corpus:
		data = []
		f = open(victor_corpus)
		for line in f:
			data.append(line.strip().split('\t'))
		f.close()
		
		#Create matrixes:
		X = self.fe.calculateFeatures(victor_corpus)
		
		#Get boundary distances:
		distances = self.classifier.decision_function(X)
		
		#Get rankings:
		result = []
		index = 0
		for i in range(0, len(data)):
			line = data[i]
			scores = {}
			for subst in line[3:len(line)]:
				word = subst.strip().split(':')[1].strip()
				scores[word] = distances[index]
				index += 1
			ranking_data = sorted(scores.keys(), key=scores.__getitem__, reverse=True)
			result.append(ranking_data)
		
		#Return rankings:
		return result

	def generateLabels(self, data, positive_range):
		Y = []
		for line in data:
			max_range = min(int(line[len(line)-1].split(':')[0].strip()), positive_range)
			for i in range(3, len(line)):
				rank_index = int(line[i].split(':')[0].strip())
				if rank_index<3+max_range:
					Y.append(1)
				else:
					Y.append(0)
		return Y
		
class SVMRanker:

	def __init__(self, fe, svmrank_path):
		"""
		Creates an instance of the SVMRanker class.
	
		@param fe: A configured FeatureEstimator object.
		@param svmrank_path: Path to SVM-Rank's root installation folder.
		"""
		
		self.fe = fe
		self.svmrank = svmrank_path
		if not self.svmrank.endswith('/'):
			self.svmrank += '/'
	
	def getFeaturesFile(self, victor_corpus, output_file):
		"""
		Creates a file containing feature values in SVM-Rank format.
		Produces the "features_file" parameter for functions getTrainingModel, getScoresFile and getRankings.
	
		@param victor_corpus: Path to a corpus in the VICTOR format.
		For more information about the file's format, refer to the LEXenstein Manual.
		@param output_file: Path in which to save the resulting feature values.
		"""
		
		#Read victor corpus:
		data = []
		f = open(victor_corpus)
		for line in f:
			data.append(line.strip().split('\t'))
		
		#Get feature values:
		features_train = self.fe.calculateFeatures(victor_corpus)
		features_train = normalize(features_train, axis=0)
		
		#Save training file:
		out = open(output_file, 'w')
		index = 0
		for i in range(0, len(data)):
			inst = data[i]
			for subst in inst[3:len(inst)]:
				rank = subst.strip().split(':')[0].strip()
				word = subst.strip().split(':')[1].strip()
				newline = rank + ' qid:' + str(i+1) + ' '
				feature_values = features_train[index]
				index += 1
				for j in range(0, len(feature_values)):
					newline += str(j+1) + ':' + str(feature_values[j]) + ' '
				newline += '# ' + word + '\n'
				out.write(newline)
		out.close()
	
	def getTrainingModel(self, features_file, c, epsilon, kernel, output_file):
		"""
		Trains an SVM-Rank ranking model.
		The model produced can be used as the "model_file" parameter of the getScoresFile function.

		@param features_file: Path to features file produced over a training VICTOR corpus.
		Should be produced by the getFeaturesFile function.
		@param c: Trade-off between training error and margin.
		Recommended values: 0.001, 0.01
		@param epsilon: Acceptable error margin.
		Recommended values: 0.00001, 0.0001
		@param kernel: ID for the kernel to be used.
		Kernels available:
		0 - Linear
		1 - Polynomial
		2 - Radial Basis Function
		3 - Sigmoid
		@param output_file: Path in which to save the resulting SVM-Rank model.
		"""
		
		print('Training...')
		comm = self.svmrank+'svm_rank_learn -c '+str(c)+' -e '+str(epsilon)+' -t '+str(kernel)+' '+features_file+' '+output_file
		os.system(comm)
		print('Trained!')
	
	def getScoresFile(self, features_file, model_file, output_file):
		"""
		Produces ranking scores in SVM-Rank format.
		The scores file produced can be used as the "scores_file" parameter of the getRankings function.
	
		@param features_file: Path to features file produced over a testing VICTOR corpus.
		Should be produced by the getFeaturesFile function.
		@param model_file: Path to a trained model file in SVM-Rank format.
		Should be produced by the getTrainingModel function.
		@param output_file: Path in which to save the resulting ranking scores in SVM-Rank format.
		"""
		
		print('Scoring...')
		comm = self.svmrank+'svm_rank_classify '+features_file+' '+model_file+' '+output_file
		os.system(comm)
		print('Scored!')
	
	def getRankings(self, features_file, scores_file):
		"""
		Produces ranking scores in SVM-Rank format.
		The scores file produced can be used as the "scores_file" parameter of the getRankings function.
	
		@param features_file: Path to features file produced over a testing VICTOR corpus.
		Should be produced by the getFeaturesFile function.
		@param scores_file: Path to a scores file in SVM-Rank format.
		Should be produced by the getScoresFile function.
		@return: A list of ranked candidates, from simplest to most complex.
		"""
		
		#Read features file:
		f = open(features_file)
		data = []
		for line in f:
			data.append(line.strip().split(' '))
		f.close()
		
		#Read scores file:
		f = open(scores_file)
		scores = []
		for line in f:
			scores.append(float(line.strip()))
		f.close()
		
		#Combine data:
		ranking_data = {}
		index = 0
		for line in data:
			id = int(line[1].strip().split(':')[1].strip())
			starti = 0
			while line[starti]!='#':
				starti += 1
			word = ''
			for i in range(starti+1, len(line)):
				word += line[i] + ' '
			word = word.strip()
			score = scores[index]
			index += 1
			if id in ranking_data.keys():
				ranking_data[id][word] = score
			else:
				ranking_data[id] = {word:score}
		
		#Produce rankings:
		result = []
		for id in sorted(ranking_data.keys()):
			candidates = ranking_data[id].keys()
			candidates = sorted(candidates, key=ranking_data[id].__getitem__, reverse=False)
			result.append(candidates)
			
		#Return rankings:
		return result
	
class MetricRanker:

	def __init__(self, fe):
		"""
		Creates an instance of the MetricRanker class.
	
		@param fe: A configured FeatureEstimator object.
		"""
		
		self.fe = fe
		self.feature_values = None
		
	def getRankings(self, victor_corpus, featureIndex):
		"""
		Ranks candidates with respect to their simplicity.
		Requires for the trainRanker function to be previously called so that a model can be trained.
	
		@param victor_corpus: Path to a testing corpus in VICTOR format.
		For more information about the file's format, refer to the LEXenstein Manual.
		@param featureIndex: Index of the feature in the FeatureEstimator to be used as a ranking metric.
		@return: A list of ranked candidates for each instance in the VICTOR corpus, from simplest to most complex.
		"""
		
		#If feature values are not available, then estimate them:
		if self.feature_values == None:
			self.feature_values = self.fe.calculateFeatures(victor_corpus)
		
		#Create object for results:
		result = []
		
		#Read feature values for each candidate in victor corpus:
		f = open(victor_corpus)
		index = 0
		for line in f:
			#Get all substitutions in ranking instance:
			data = line.strip().split('\t')
			substitutions = data[3:len(data)]
			
			#Create dictionary of substitution to feature value:
			scores = {}
			for substitution in substitutions:
				word = substitution.strip().split(':')[1].strip()
				scores[word] = self.feature_values[index][featureIndex]
				index += 1
			
			#Check if feature is simplicity or complexity measure:
			rev = False
			if self.fe.identifiers[featureIndex][1]=='Simplicity':
				rev = True
			
			#Sort substitutions:
			sorted_substitutions = sorted(scores.keys(), key=scores.__getitem__, reverse=rev)
		
			#Add them to result:
			result.append(sorted_substitutions)
		f.close()
		
		#Return result:
		return result
		
	def size(self):
		"""
		Returns the number of features available for a given MetricRanker.
		
		@return: The number of features in the MetricRanker's FeatureEstimator object.
		"""
		return len(self.fe.identifiers)