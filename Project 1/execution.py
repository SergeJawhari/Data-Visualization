from wordcloud import WordCloud
from IPython.core.display import HTML
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
embed_code=wc.get_embed_code(text=texts,random_color=True,topn=40)
HTML(embed_code)


#don't randomize color, show only top 50
embed_code=wc.get_embed_code(text=texts,random_color=True,topn=50)
HTML(embed_code)
with open("./wordcloudoutput.html","w") as file:
    file.write(embed_code)
new = 2 # open in a new tab, if possible
url = "file:///" + os.path.realpath('wordcloudoutput.html')
webbrowser.open(url,new=new)
