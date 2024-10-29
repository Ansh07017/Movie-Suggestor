import pandas as pd
import numpy as np
import ast
import nltk
m=pd.read_csv(r"C:\Users\Anshp\OneDrive\Desktop\mrs\data\tmdb_5000_movies.csv (7)\tmdb_5000_movies.csv")
c=pd.read_csv(r"C:\Users\Anshp\OneDrive\Desktop\mrs\data\tmdb_5000_credits.csv\tmdb_5000_credits.csv")
m=m.merge(c,on='title')
#genres id keywords title overview cast crew
m=m[['movie_id','keywords','title','overview','cast','crew','genres']]
m.isnull().sum()
m.dropna(inplace=True)
#print(m.iloc[0].genres)
def convert(obj):
    l=[]
    for i in ast.literal_eval(obj):#obj pehle string tha baad me list ban gaya ye use karne se
        l.append(i['name'])
        return l
m['genres']=m['genres'].apply(convert)
m['keywords'] = m['keywords'].apply(convert)
def convert3(obj):
    l=[]
    counter=0
    for i in ast.literal_eval(obj):#obj pehle string tha baad me list ban gaya ye use karne se
        if counter!=3:
            l.append(i['name'])
            counter+=1
        else:
            break
    return l
m['cast']=m['cast'].apply(convert3)
def fetch_director(obj):
    l=[]
    for i in ast.literal_eval(obj):#obj pehle string tha baad me list ban gaya ye use karne se
        if i['job'] =='Director':
            l.append(i['name'])
        else:
            break
    return l
m['crew']=m['crew'].apply(fetch_director)
#our filtered data
m['overview']=m['overview'].apply(lambda x:x.split())
m['genres']=m['genres'].apply(lambda x:[i.replace(" ","") for i in x]if x is not None else x)
m['keywords']=m['keywords'].apply(lambda x:[i.replace(" ","") for i in x]if x is not None else x)
m['cast']=m['cast'].apply(lambda x:[i.replace(" ","") for i in x]if x is not None else x)
m['crew']=m['crew'].apply(lambda x:[i.replace(" ","") for i in x]if x is not None else x)

m['tags']=m['overview']+m['cast']+m['crew']+m['keywords']+m['genres']
# Create a copy of the selected columns to avoid SettingWithCopyWarning
new_df = m[['movie_id', 'title', 'tags']].copy()

# Convert the list in 'tags' to a single string
new_df['tags'] = new_df['tags'].apply(lambda x: " ".join(x) if isinstance(x, list) else "")
new_df['tags']=new_df['tags'].apply(lambda x:x.lower())
#text vectorisation
#bag of words techniques
#stop words not considered(in,a,the...)
from sklearn.feature_extraction.text import CountVectorizer
cv=CountVectorizer(max_features=5000,stop_words='english')
vectors=cv.fit_transform(new_df['tags']).toarray()
#stemming applied(making 1 word for similar words like action ,actions,action hero)
from nltk.stem.porter import PorterStemmer
ps=PorterStemmer()
def stem(text):
    y=[]
    for i in text.split():
        y.append(ps.stem(i))
    return " ".join(y)
new_df['tags']=new_df['tags'].apply(stem)
#cosine distance(i.e angle) calculated instead of euclidian distance as it is unreliable over large data
from sklearn.metrics.pairwise import cosine_similarity
similarity=cosine_similarity(vectors)
def recommend(movie):
    m_index=new_df[new_df['title']==movie].index[0]
    distances=similarity[m_index]
    m_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]
    for i in m_list:
        print(new_df.iloc[i[0]].title)
import pickle
pickle.dump(new_df.to_dict(),open('movies_dict.pkl','wb'))
pickle.dump(similarity,open('similarity.pkl','wb'))