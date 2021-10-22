from sklearn.base import TransformerMixin
import string
import spacy
import gensim
import time
import re

class cleaner_review(TransformerMixin):
    
    def __init__(self,n_jobs=30,batch_size=1000,
                 disable_spacy=["parser","ner"],limit_size_to_multiprocessing=5000,
                 loading_spacy="en_core_web_sm"):
        self.n_process=n_jobs
        self.batch_size=batch_size
        self.nlp = spacy.load(loading_spacy,disable=disable_spacy)
        self.trigram_mod = None
        self.limit_size_to_multiprocessing=limit_size_to_multiprocessing
    # On prépare le trigram mod lors du fit
    
    def clean_data(self,doc,allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV'],stop_word_add=None):
        all_stopword = self.nlp.Defaults.stop_words
        all_stopword.update(string.punctuation)
        if not stop_word_add is None: 
            all_stopword.update(stop_word_add)
        return [token.lemma_ for token in doc if (token.pos_ in allowed_postags) and (not token.text in all_stopword)]
    
    def first_clean(self,doc):
        doc = [re.sub('\n+', ' ', text.lower()) for text in doc]
        doc = [re.sub('[éèêë]','e',text) for text in doc]
        doc = [re.sub('[ïîì]','i',text) for text in doc]
        doc = [re.sub('[àâä]','a',text) for text in doc]
        doc = [re.sub('[ôö]','o',text) for text in doc]
        doc = [re.sub('[üûù]','u',text) for text in doc]
        doc = [re.sub('[ç]','c',text) for text in doc]
        doc = [re.sub(r'[^a-z \'-]+',' ',text) for text in doc]
        doc = [re.sub(r'([a-z])\1{2,}', r'\1', text) for text in doc]
        return [re.sub(' {2,}', ' ', text) for text in doc]

    
    def fit(self,X,y=None):
        X = self.first_clean(X)
        if type(X) is list:
            size=len(X)
        else:
            size=X.shape[0]
        if size > self.limit_size_to_multiprocessing:
            data = [doc for doc in self.nlp.pipe(X,n_process=self.n_process,batch_size=self.batch_size)]
        else:
            data = [self.nlp(doc) for doc in X]
            
        all_review_clean = [clean_data(doc) for doc in data]
        
        bigram = gensim.models.Phrases(all_review_clean, min_count=2, threshold=100) # higher threshold fewer phrases.
        trigram = gensim.models.Phrases(bigram[all_review_clean],threshold=100)
        
        self.trigram_mod = gensim.models.phrases.Phraser(trigram)
        return self
    # On prépare le trigram mod lors du fit
    def fit_transform(self,X,y=None):
        X = self.first_clean(X)
        if type(X) is list:
            size=len(X)
        else:
            size=X.shape[0]
        temps1=time.time()
        if size > self.limit_size_to_multiprocessing:
            data = [doc for doc in self.nlp.pipe(X,n_process=self.n_process,batch_size=self.batch_size)]
        else:
            data = [self.nlp(doc) for doc in X]
        temps2=time.time()
        duration1=temps2-temps1

        print("formatting in :","%8.2f" %duration1,"secondes")

        all_review_clean = [self.clean_data(doc) for doc in data]
        temps3=time.time()
        duration2=time.time()-temps2
        print("clean in :","%8.2f" %duration2,"secondes")

        bigram = gensim.models.Phrases(all_review_clean, min_count=2, threshold=100) # higher threshold fewer phrases.
        trigram = gensim.models.Phrases(bigram[all_review_clean],threshold=100)
        self.trigram_mod = gensim.models.phrases.Phraser(trigram)

        duration3=time.time()-temps3
        duration_total=time.time()-temps1
        print("trigram mod created in :","%8.2f" %duration3,"secondes")
        print("total formatting, cleaning, trigram in :", "%8.2f" %duration_total,"secondes")
        return [" ".join(self.trigram_mod[doc]) for doc in all_review_clean]
    
    # On renvoie les données propre avec on sans le trigram_mod (si l'entrainement à était effecuté avant)
    def transform(self,X,**transform_params):
        X = self.first_clean(X)
        if type(X) is list:
            size=len(X)
        else:
            size=X.shape[0]
        if size > self.limit_size_to_multiprocessing:
            data = [doc for doc in self.nlp.pipe(X,n_process=self.n_process,batch_size=self.batch_size)]
        else:
            data = [self.nlp(doc) for doc in X]
        if self.trigram_mod is None:
            return [" ".join(doc) for doc in [self.clean_data(doc) for doc in data]]
        return [" ".join(self.trigram_mod[doc]) for doc in [self.clean_data(doc) for doc in data]]
    
    def get_params(self, deep=True):
        return {}