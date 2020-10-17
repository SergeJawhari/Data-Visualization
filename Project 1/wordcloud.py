#!/usr/bin/env python
# coding: utf-8
#references:
# https://github.com/kavgan/word_cloud/blob/master/word_cloud/word_cloud_generator.py
# https://stackoverflow.com/questions/16729574/how-to-get-a-value-from-a-cell-of-a-dataframe
# https://investigate.ai/text-analysis/counting-words-with-scikit-learns-countvectorizer/
# In[72]:

import pandas as pd
import logging
import numpy as np
import random
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer


class WordCloud:

    def __init__(self, stopwords=[], use_tfidf=False):

        self.use_tfidf = use_tfidf
        self.data = []
        self.color_choices = ['#b82c2c',
                              '#a55571',
                              '#bc72d0',
                              '#8000FF',
                              '#3498DB',
                              '#FF5733',
                              '#223AE6',
                              '#2ECC71',
                              '#5F6A6A',
                              '#6C22E6',
                              '#CE22E6',
                              '#ACB02E',
                              '#B18904',
                              '#848484',
                              '#04B404',
                              '#5882FA',
                              '#FF0080',
                              '#0489B1',
                              '#FA5858',
                              '#DBA901',
                              '#00b4ff',
                              '#008080',
                              '#003366',
                              '#725394'
                              ]
       

        # load a set of stop words
        self.stopwords = stopwords

    def get_color_code(self, score):
        """Get the appropriate color codes."""

        step = 0.05
        current_incremented_score = 0
        idx = 0

        while current_incremented_score < 1:
            if score <= current_incremented_score:
                return self.color_choices[idx]
            idx += 1
            current_incremented_score = current_incremented_score + step

        return self.color_choices[0]


    def get_font_size(self, score: float):
        """Increment scale until score almost equals current_incremented_score."""

        # font size start and increment
        scale = 0.5
        scale_step = 0.15

        # score increment
        score_step = 0.05
        current_incremented_score = 0

        while current_incremented_score < 1:

            # increment scale until score almost equals current_incremented_score
            # the larger the score, the more the scale increment
            if score <= current_incremented_score:
                return scale

            current_incremented_score = current_incremented_score + score_step
            scale += scale_step    

        return scale
    
    # getting the word count
    def word_counting(self,text:list):
        wc = CountVectorizer(text,stop_words=self.stopwords)
        wc_vector = wc.fit_transform(text)
        return wc_vector


    def get_embed_code(self, text_scores: pd.DataFrame = None, text: list = [], topn=100, random_color=True):

        if text_scores is None and len(text) > 0:
            items = self.extract_topn_from_vector(text, topn=topn)
            text_df = pd.DataFrame(items, columns=['words', 'score'])

        elif text_scores is not None:
            text_df = text_scores
            text_df.columns = ['words', 'score']
           
        else:
            logging.error(
                "There is a problem with your input text. Did you provide any?")
            return

        if random_color:
            random.shuffle(self.color_choices)

        word_cloud_items = []

        html = [
            "<html><head><style>.tooltip{position: relative;display:inline-block;}.tooltip .tooltiptext {visibility: hidden;width: 120px;background-color: black;color: #fff;text-align: center;border-radius: 6px;padding: 5px 0;position: absolute;z-index: 1;top: -5px;left: 110%;font-size: 12px;}.tooltip .tooltiptext::after {content: '';position: absolute;top: 50%;right: 100%;margin-top: -5px;border-width: 5px;border-style: solid;border-color: transparent black transparent transparent;font-size: 12px;}.tooltip:hover .tooltiptext {visibility: visible;font-size: 12px;}</style></head><body><div align='center' style='width:100%'><div align='center' style='text-align:justify; border-radius: 25px;background: #fff7f7;overflow: auto; width:500px !important; padding:20px; '; text-align: center; word-wrap: break-word;> "]
        
        wc = CountVectorizer(text,stop_words=self.stopwords)
        wc_vector = wc.fit_transform(text)
        counts=pd.DataFrame(wc_vector.toarray(),columns=wc.get_feature_names())

        for idx, row in text_df.iterrows():
            
            word = row.words.replace(" ", "-") # 2
            word_count = counts.at[0,word]# 3, The number of words should be found and assigned to this variable.
            scale = self.get_font_size(row.score) # 1
            color_code = self.get_color_code(row.score) # 0
            word_cloud_items.append(
                " <span style='color:{0};font-size:{1}em;white-space: normal;font-family:verdana;display: inline-block;line-height:30px'><div class = 'tooltip'>{2}&nbsp&nbsp;<span class='tooltiptext'>{3} instances</span></div></span>".format(
                    color_code, scale, word, word_count))

        random.shuffle(word_cloud_items)
        random.shuffle(word_cloud_items)

        html.extend(word_cloud_items)
        html.append("</div></div>")
        return ''.join(html)

    def sort_coo(self, coo_matrix):
        tuples = zip(coo_matrix.col, coo_matrix.data)
        return sorted(tuples, key=lambda x: (x[1], x[0]), reverse=True)
    


    def get_ranks(self,word_vector):
        """Get normalized tf."""

        max = np.max(word_vector)

        # normalize raw counts
        word_count_vector = np.multiply(word_vector, 1/(max))

        return word_count_vector
    
    def get_normalized_tf(self, cv: CountVectorizer, text: list):
        """Get normalized tf."""

        big_text = ' '.join(text)
        word_count_vector = cv.fit_transform([big_text])
        max = np.max(word_count_vector)

        # normalize raw counts
        word_count_vector = np.multiply(word_count_vector, 1/(max))

        return word_count_vector

    def get_tfidf_scores(self, cv: CountVectorizer, text: list):
        """Get tfidf values."""

        word_count_vector = cv.fit_transform(text)
        big_text = ' '.join(text)

        # compute word scores
        tfidf_transformer = TfidfTransformer(
            smooth_idf=False, use_idf=True, norm='l2')
        tfidf_transformer.fit(word_count_vector)
        tf_idf_vector = tfidf_transformer.transform(cv.transform([big_text]))
        return tf_idf_vector

    def extract_topn_from_vector(self, text: list, topn=10):
        """Extract keywords based on tf-idf score."""

        # get word count
        cv = CountVectorizer(stop_words=self.stopwords)
        word_scores_vector = None
        if self.use_tfidf:
            word_scores_vector = self.get_tfidf_scores(cv, text)
        else:
            word_scores_vector = self.get_normalized_tf(cv, text)

        #word_scores_vector=self.get_ranks(word_scores_vector)

        # sort the tf-idf vectors by descending order of scores
        sorted_items = self.sort_coo(word_scores_vector.tocoo())
        sorted_items = sorted_items[:topn]


        final_items = []

        # word index and corresponding tf-idf score
        for idx, score in sorted_items:
            final_items.append([cv.get_feature_names()[idx], score])

        return final_items


# In[73]:


from IPython.core.display import HTML
from bs4 import BeautifulSoup
from nltk.corpus import reuters
import nltk
import pandas as pd
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
import os
import webbrowser
nltk.download('stopwords')
ENGLISH_STOP_WORDS = set(stopwords.words('english'))

#taking the input from a text file at the given file path
#example of a path in windows: C:/Users/rishi/OneDrive/Desktop/testingdoc.txt

file_path = input("Please provide the path of the text file: ")
assert os.path.exists(file_path), "File not found at , "+str(file_path)
with open(file_path, 'r', encoding='utf-8') as file:
    text = file.read().replace('\n', '')

texts=[]
texts.append(text)

wc=WordCloud(use_tfidf=False,stopwords=ENGLISH_STOP_WORDS)


#don't randomize color, show only top 50
embed_code=wc.get_embed_code(text=texts,random_color=True,topn=50)
HTML(embed_code)

with open("./wordcloudoutput.html","w") as file:
    file.write(embed_code)
new = 2 # open in a new tab, if possible
url = "file:///" + os.path.realpath('wordcloudoutput.html')
webbrowser.open(url,new=new)







