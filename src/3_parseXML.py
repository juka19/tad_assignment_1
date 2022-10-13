import urllib.request
import pandas as pd
import bs4

f = urllib.request.urlopen('https://www.bundestag.de/resource/blob/913444/aeecd11842a5e9e64c0aac4fbd2dd4b9/20058-data.xml')

data = f.read()
soup = bs4.BeautifulSoup(data, 'html')

def get_speech(soup):
    try: 
        redner = soup.find("redner")
        f_name = redner.find("vorname").get_text()
        name = redner.find("nachname").get_text()
        party = redner.find("fraktion").get_text()
        t = soup.find_all("p", {"klasse" : ["J", "J_1", "O"]})
        t = " ".join([p.get_text() for p in t])
        output = {
            'text': t,
            "name" :  f_name + ' ' + name,
            "party" : party
            }
    except Exception:
        t = soup.find_all("p", {"klasse" : ["J", "J_1", "O"]})
        t = " ".join([p.get_text() for p in t])
        output = {
            'text': t,
            "name" : f_name + ' ' + name,
            "party" : ''
            }
    return(output)


pd.DataFrame([get_speech(r) for r in soup.find_all('rede')]).to_excel('data\\bt_session.xlsx')
