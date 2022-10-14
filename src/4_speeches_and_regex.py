import pandas as pd
import re
from collections import defaultdict
import string

speeches = pd.read_excel('data\\bt_session.xlsx')

print(f'Number of speeches in the 58th session: {len(speeches)}')
print(f"""
      Alexander Dobrindt's speech:\n
      ____________________________\n
      {speeches.text.iloc[28]}
      """)

def find_matches(speeches):
    protocol = ' '.join(speeches).split(' ')
    matches = defaultdict(int)
    pattern = re.compile('.*[kK][oO][hH][lL][eE]')
    for token in protocol:
        token = token.translate(
            str.maketrans('', '', string.punctuation))
        if re.match(pattern, token) != None:
            matches[token] += 1
    return matches

kohle = find_matches(speeches.text)
(pd.DataFrame.from_dict(dict(kohle), orient='index')
 .reset_index()
 .rename(columns={'index': 're-match', 0:'Count'})
 .to_csv('outputs\\kohle.csv', index=False)
)
