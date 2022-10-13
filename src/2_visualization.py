import pickle
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer, ENGLISH_STOP_WORDS
from matplotlib.ticker import MaxNLocator

poem_data = pd.read_pickle('data\poems_data.pickle')
grp = poem_data.groupby(['book_title', 'poem_title'])['line_number'].max().reset_index()

## histogram
sns.set_style('darkgrid')
ax = sns.histplot(
    grp, 
    x='line_number', 
    color='navy', 
    binwidth=5)
ax.set_title('Count of lines')
ax.set_xlabel('Number of lines per poem')
plt.margins(x=.01)
plt.show()

ax = sns.displot(
    grp, 
    x='line_number',
    binwidth=5,
    hue='book_title',
    alpha=.4)
ax.set_title('Count of lines')
plt.xlabel('Number of lines per poem by book')
plt.margins(x=.01)
plt.show()

stop_words = ENGLISH_STOP_WORDS.union(['thee', 'thy']) # same as you and yours, I think

def create_dfm(text, vectorizer=CountVectorizer(stop_words=stop_words)):
    dfm = vectorizer.fit_transform(text)
    return pd.DataFrame(dfm.todense(),
        columns=vectorizer.get_feature_names_out())
    

create_dfm(poem_data.line).to_csv('outputs\\dfm_1.csv', index=False)

grp = (poem_data
       .groupby(['book_title', 'poem_title'])['line'] # grouping by book in order to avoid double counting
       .aggregate(lambda x: ' '.join(x))
       .reset_index()
       )

create_dfm(grp.line, vectorizer=TfidfVectorizer(stop_words=stop_words)).to_csv('outputs\\dfm_tfidf_2.csv',)


for book in grp.book_title.unique():
    data = (create_dfm(
        grp[grp.book_title == book].line
        )
    .sum()
    .sort_values(ascending=False)
    [0:20]  # top 20 enetries
    .reset_index()
    )
    sns.barplot(data=data, x=0, y='index').xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.title(f'Word count of {book}')
    plt.xlabel('Count')
    plt.ylabel('Terms')
    plt.show()
    plt.clf()
