# -*- coding: utf-8 -*-
import gensim
import numpy as np
from scipy import spatial
from gensim.models.word2vec import Word2Vec
import numpy as np
import settings
import string 

def avg_feature_vector(sentence, model, num_features, index2word_set):
    words = sentence.split()
    feature_vec = np.zeros((num_features, ), dtype='float32')
    n_words = 0
    for word in words:
        if word in settings.index2word_set:
            n_words += 1
            feature_vec = np.add(feature_vec, settings.model[word])
    if (n_words > 0):
        feature_vec = np.divide(feature_vec, n_words)
    return feature_vec

def chat(uinput):
    ans = ""
    translator = str.maketrans('', '', string.punctuation)
    #check for weather service keywords
    uinput =uinput.translate(translator).lower()
    i = 0
    s1 = uinput
    max_sim = 0
    for question in settings.q:
        s2 = question
        s1_afv = avg_feature_vector(s1, model=settings.model, num_features=100, index2word_set=settings.index2word_set)
        s2_afv = avg_feature_vector(s2, model=settings.model, num_features=100, index2word_set=settings.index2word_set)
        sim = 1 - spatial.distance.cosine(s1_afv, s2_afv)
        print(sim)
        if (sim>max_sim and sim>0.6):
            max_sim = sim
            ans = settings.a[i]
        i = i + 1
    
    if ans=="" or ans is None: ans = u"Я не знаю ответ на этот вопрос. Я все еще учусь."
    return ans
