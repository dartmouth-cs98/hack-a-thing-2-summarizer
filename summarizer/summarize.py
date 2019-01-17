import numpy as np
import pandas as pd
import nltk
import re
import io
import networkx as nx
import json
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from sklearn.metrics.pairwise import cosine_similarity

class GTSummarizer():
    def __init__(self, controller=None, trainingData="./data/glove.6B.50d.txt"):
        # NLTK init
        nltk.download('punkt') # one time execution
        nltk.download('stopwords')
        self.stop_words = stopwords.words('english')
        self.trainingData = trainingData
        self.controller = controller

    def remove_stopwords(self, sen):
        sen_new = " ".join([i for i in sen if i not in self.stop_words])
        return sen_new

    def getSentences(self, sentences):
        sentences = [x for y in sentences for x in y]
        clean_sentences = pd.Series(sentences).str.replace("[^a-zA-Z]", " ")

        # make alphabets lowercase
        clean_sentences = [s.lower() for s in clean_sentences]

        # remove stopwords from the sentences
        clean_sentences = [self.remove_stopwords(r.split()) for r in clean_sentences]

        # print(" ".join(sentences))
        return sentences

    # Extract word vectors
    def getWordWeightVectors(self):
        word_embeddings = {}
        f = io.open(self.trainingData, encoding='utf-8')
        for line in f:
            values = line.split()
            word = values[0]
            coefs = np.asarray(values[1:], dtype='float32')
            word_embeddings[word] = coefs
        f.close()
        return word_embeddings

    def getSentenceVectors(self, sentences, word_embeddings):
        sentence_vectors = []
        for i in sentences:
            if len(i) != 0:
                v = sum([word_embeddings.get(w, np.zeros((50,))) for w in i.split()])/(len(i.split())+0.001)
            else:
                v = np.zeros((50,))
            sentence_vectors.append(v)
        return sentence_vectors

    def calculateSimilarityMatrix(self, sentences, sentence_vectors):
        # similarity matrix
        similarity_matrix = np.zeros([len(sentences), len(sentences)])

        for i in range(len(sentences)):
            for j in range(len(sentences)):
                if i != j:
                    similarity_matrix[i][j] = cosine_similarity(sentence_vectors[i].reshape(1,50), sentence_vectors[j].reshape(1,50))[0,0]
        return similarity_matrix

    def getSummaryScores(self, similarity_matrix):
        nx_graph = nx.from_numpy_array(similarity_matrix)
        scores = nx.pagerank(nx_graph)
        return scores


    def readCSV(self, fileName, textField):
        sentences = []
        df = pd.read_csv(fileName)
        for sentence in df[textField]:
            sentences.append(sent_tokenize(sentence))
        return sentences


# sentences = getSentences(readCSV("tennis_articles_v4.csv", "article_text"))
# word_embeddings = getWordWeightVectors()
# sentence_vectors = getSentenceVectors(sentences, word_embeddings)
# similarity_matrix = calculateSimilarityMatrix(sentences, sentence_vectors)
# scores = getSummaryScores(similarity_matrix)
# ranked_sentences = sorted(((scores[i],s) for i,s in enumerate(sentences)), reverse=True)
# for i in range(5):
#   print(ranked_sentences[i][1])
#   print(str(ranked_sentences[i]))
#   print()

    def summarize_csv(self, fileName, textFieldName, topN=5):
        sentences = self.getSentences(self.readCSV(fileName, textFieldName))
        word_embeddings = self.getWordWeightVectors()
        sentence_vectors = self.getSentenceVectors(sentences, word_embeddings)
        similarity_matrix = self.calculateSimilarityMatrix(sentences, sentence_vectors)
        scores = self.getSummaryScores(similarity_matrix)
        ranked_sentences = sorted(((scores[i],s) for i,s in enumerate(sentences)), reverse=True)

        results = []
        for i in range(topN):
            results.append(ranked_sentences[i])
        return results


    def summarize_csv_wrapper(self, sid, message):
        print("Received request")
        data = json.loads(message)
        results = self.summarize_csv(data['fileName'], data['textFieldName'])
        return results

