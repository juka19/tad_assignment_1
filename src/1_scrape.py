import re
import urllib.request
import pandas as pd
import pickle

  
data = urllib.request.urlopen('https://www.gutenberg.org/cache/epub/1934/pg1934.txt')

poem_title_pattern = re.compile('[A-Z]+\s?[A-Z]{2}')
end = '*** END OF THE PROJECT GUTENBERG EBOOK SONGS OF INNOCENCE AND OF EXPERIENCE ***\r\n'



n = 0
book = 'Songs of Innocence'
st_n = -1
poem = 'INTRODUCTION'
rec_list = []
skip_lines = True
for line in data.readlines():
    dec_line = line.decode()
    if skip_lines:
        if dec_line == 'INTRODUCTION\r\n':
            skip_lines = False
        continue
    n += 1
    if dec_line == end:
        break
    if dec_line == 'SONGS OF EXPERIENCE\r\n':
        book = 'Songs of Experience'
    if re.match(poem_title_pattern, dec_line) != None:
        poem = dec_line.replace('\r\n', '')
        st_n = -1
        n = 0
    if dec_line == '\r\n':
        if st_n <= 0:
            st_n += 1
        elif st_n > 0:
            st_n += 1
        if n > 0:
            n -= 1
        else:
            n = 0
    rec_list.append(
        {'line': dec_line.replace('\r\n', ''), 'line_number': n, 'stanza_number': st_n, 
         'poem_title' : poem, 'book_title': book}
        )
    
poems = pd.DataFrame.from_records(rec_list)

poems = poems[poems['line'] != '']
poems = poems[poems.line != poems.poem_title]

poems.to_pickle('data\\poems_data.pickle')