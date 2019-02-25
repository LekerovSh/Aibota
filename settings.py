import gensim
import numpy as np
from scipy import spatial
from gensim.models.word2vec import Word2Vec
import numpy as np
from database import select_questions, select_answers, insert

def init():
    
    global w2v_fpath
    w2v_fpath = "all.norm-sz100-w10-cb0-it1-min100.w2v"
    
    global model
    model = gensim.models.KeyedVectors.load_word2vec_format(w2v_fpath, binary=True, unicode_errors='ignore')

    global index2word_set
    index2word_set = set(model.wv.index2word)
    
    #insert() #- uncomment this line only when adding questions and answers
    
    global q
    #q = ["Вот не думала что боты умеют понимать", "А где же ты выучился читать", "А где же ты выучился читать", "ты откуда", "Никто не может быть отовсюду"]

    global a
    #a = ["Ботам незачем понимать. Люди научат большему", "Где все, там и я. В школе.", "Где все, там и я. В школе.", "Отовсюду.", "Ну, в таком случае я родилась в Астане."]

    
    q = select_questions()
    a = select_answers()

    global context
    context = {}
    
    context['service'] = ''
    context['city'] = 'Астана'
    context['date'] = 'сегодня'
    context['query'] = '' # wiki query

