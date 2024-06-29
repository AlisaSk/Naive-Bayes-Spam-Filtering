from corpus import Corpus
import os
from collections import defaultdict
 
class TrainingCorpus(Corpus):
    '''Class where we hold all useful functions for our main train() function'''
    def __init__(self, corpus_path):
        self.corpus_path = corpus_path
 
        self.positive_tag = "SPAM"
        self.negative_tag = "OK"
 
        self.all_words = defaultdict(lambda: [0,0])
        self.words_counter = 0
        # total count of spam and ham emails
        self.spam_count = 0
        self.hams_count = 0
        self.probabilities = []
        # words, that won't help us detect the spam message
        self.words_to_delete = ['the', 'are', 'to', 'at', 'you', 'can', 'of', 'or', 'as', 'com', 'and', 'net', 'for',
                                 'by', 'have', 'is', 'that', 'it', 'will', 'be', 'name', 'http', 'www', 'your', 'in', 'email', 'from', 'this', 'click', 'html', 'bgcolor', 'ffffff',
                                'table', 'width', 'height', 'tr', 'td', 'font', 'size', 'on', 'home', 'if', 'href', 'not', 'nbsp', 'with',
                                'all', 'value', 'free', 'online', 'we', 'our', 'list', 'div', 'align', 'center', 'border', 'face', 'color',
                                'verdana', 'style', 'arial', 'money', 'br', 'li', 'src', 'no', 'cellspacing', 'cellpadding', 'blockquote',
                                'span', 'helvetica', 'sans', 'serif', 'alt', 'img', 'gif', 'cnet', 'zdnet', 'clickthru']
 
    # this function set spam and ham content
    def set_hams_and_spams(self, tag):
        truth_path = os.path.join(self.corpus_path, "!truth.txt")
        with open(truth_path, 'r', encoding='utf-8') as truth:
            for line in truth:
                words = line.split()
                if words[1] == tag:
                    # count spam/ham messages here
                    if tag == self.positive_tag:
                        self.spam_count += 1
                    if tag == self.negative_tag: 
                        self.hams_count += 1
 
                    yield words[0], super().readfile(os.path.join(self.corpus_path, words[0]))
 
                else:
                    continue
 
 
    # define frequency of apperance for each word in spam and ham
    def count_all_words(self, data, tag):
        counts = defaultdict(lambda: [0, 0])
        for name, content in data:
            for word in content:
                # count all words that we use to train our function
                if word not in self.all_words:
                    self.words_counter += 1
 
                index = 0
                # 0 spam index, 1 ham index
                index += 0 if tag == self.positive_tag else 1
                if not  (word.isdigit() == 1 or len(word) == 1 or word in self.words_to_delete):
                    self.all_words[word][index] += 1
 
         
 
    def count_probability(self):
    # k for correction (to avoid zero probability in cases, when word didn't appear in spam/ham)
        k = 1
        for word, count in self.all_words.items():
            # (remembering, that 0 index is spam, 1 -- ham)
            # we use Naive Bayes classifier method, to count this probabilities
            spam_prob = (count[0] + k) / (self.spam_count + self.words_counter * k)
            ham_prob = (count[1] + k) / (self.hams_count + self.words_counter * k)
 
            # adding set contains word and it's spam and ham probability
            result = (word, spam_prob, ham_prob)
            self.probabilities.append(result)