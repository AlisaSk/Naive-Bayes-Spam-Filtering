from corpus import Corpus
from trainingcorpus import TrainingCorpus
import os
import math
 
class MyFilter:
    ''' Spam filter based on the simplier model of Naive Bayes classifier'''
    def __init__(self):
        self.positive = "SPAM"
        self.negative = "OK"
        self.probabilities = []
 
    def train(self, corpus_path):
        training_corpus = TrainingCorpus(corpus_path)
         
        found_hams = training_corpus.set_hams_and_spams(self.negative)
        found_spams = training_corpus.set_hams_and_spams(self.positive)
 
        training_corpus.count_all_words(found_hams, self.negative)
        training_corpus.count_all_words(found_spams, self.positive)
 
        training_corpus.count_probability()
        self.probabilities = training_corpus.probabilities
 
    def test(self, corpus_path):
        corpus = Corpus(corpus_path)
        my_file = open(os.path.join(corpus_path, "!prediction.txt"), "w+", encoding="utf-8")
        for email, content  in corpus.emails():
            if "!" in email:
                continue
            # using coefficient 0.2 as the minimum for setting email as spam
            # (set this coefficient by testing diffent ones)
            if self.test_email(content) >= 0.2:
                prediction = self.positive
            else:
                prediction = self.negative
            # create line and add it to !prediction.txt
            answer = f"{email} {prediction}\n"
            my_file.write(answer)
        my_file.close()
 
    def test_email(self, content):
        # Сondition used in case, when train() function didn't run
        if self.probabilities == []:
            return 0.1
         
        # Initial probabilities
        content_spam_prob = content_ham_prob = 0.0
         
        for word, spam_prob, ham_prob in self.probabilities:
 
            # just for safety
            if spam_prob <= 0 or ham_prob <= 0:
                return 0
             
            # in fact we should just multiply all the separate probs,
            # but in reality we will loose too many digits
            # (spam and ham prob are too small to multiply them with each other)
            # so we find out log function, which will help to solve this problem
            if word in content:
                content_spam_prob += math.log(spam_prob)
                content_ham_prob += math.log(ham_prob)
            else:
                content_spam_prob += math.log(1.0 - spam_prob)
                content_ham_prob += math.log(1.0 - ham_prob)
     
 
        e_spam_prob = math.exp(content_spam_prob)
        e_ham_prob = math.exp(content_ham_prob)
        sum_e_prob = (e_ham_prob + e_spam_prob)
 
        # for now we have no idea, why sometimes sum_e_probability = 0,
        # so we fixed it this way
        if sum_e_prob == 0:
            return 0.0
 
        return e_spam_prob / sum_e_prob