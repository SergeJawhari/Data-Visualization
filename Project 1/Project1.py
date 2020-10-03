#!/usr/bin/env python
# coding: utf-8

# In[1]:


import nltk
from urllib.request import urlopen
from bs4 import BeautifulSoup
url = "https://www.nytimes.com/2017/04/26/magazine/baking-is-all-in-the-hands.html"
html = urlopen(url).read()


# In[2]:


soup = BeautifulSoup(html)
# kill all script and style elements
for script in soup(["script", "style"]):
    script.extract()    # rip it out


# In[3]:


text = soup.get_text()
# break into lines and remove leading and trailing space on each
lines = (line.strip() for line in text.splitlines())
# break multi-headlines into a line each
chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
# drop blank lines
text = 'n'.join(chunk for chunk in chunks if chunk)


# In[4]:


#download and print the stop words for the English language
from nltk.corpus import stopwords
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

#tokenise the data set
from nltk.tokenize import sent_tokenize, word_tokenize
words = word_tokenize(text)

# removes punctuation and numbers
wordsFiltered = [word.lower() for word in words if word.isalpha()]

# remove stop words from tokenised data set
filtered_words = [word for word in wordsFiltered if word not in stopwords.words('english')]


# In[5]:


from wordcloud import WordCloud
import matplotlib.pyplot as plt
wc = WordCloud(max_words=1000, margin=10, background_color='white',
scale=3, relative_scaling = 0.5, width=500, height=400,min_font_size=6,
random_state=1).generate(' '.join(filtered_words))
plt.figure(figsize=(20,10))
plt.imshow(wc)
plt.axis("off")
plt.show()
#wc.to_file("/wordcloud.png")









