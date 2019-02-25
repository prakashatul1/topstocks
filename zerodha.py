import requests
from bs4 import BeautifulSoup
import pandas as pd
import zipfile
import redis

conn = redis.Redis(host='redis://h:pe9af2c4711610cb70f32b3c0c36b33d2f9f72a25dca00a1876148a8b5ae0f174@ec2-52-44-176-48.compute-1.amazonaws.com',port=12639)

url = 'https://www.bseindia.com/markets/MarketInfo/BhavCopy.aspx'
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')
zip_url = soup.find_all('a')[1]['href']

date = zip_url.split("/")[6][2:8]

target_path = 'EQ'+date+'_CSV.ZIP'

response = requests.get(zip_url, stream=True)
handle = open(target_path, "wb")
for chunk in response.iter_content(chunk_size=512):
    if chunk:
        handle.write(chunk)
handle.close()

zf = zipfile.ZipFile('EQ'+date+'_CSV.ZIP')
df = pd.read_csv(zf.open('EQ'+date+'.CSV'))
df = df.astype('object')

top_10 = {}

for i in range(df.index[-1]+1):

    close = dict(df.loc[i, ['SC_NAME', 'OPEN', 'HIGH', 'LOW', 'CLOSE', 'SC_CODE']])['CLOSE']

    if len(top_10) == 10:
        if close > top_10[min(top_10, key=top_10.get)]:
            del top_10[min(top_10, key=top_10.get)]
            top_10[i] = close
    else:
        top_10[i] = close

    conn.hmset(i,dict(df.loc[i,['SC_NAME','OPEN','HIGH','LOW','CLOSE','SC_CODE']]) )

for each in top_10:
    pass
    conn.zadd("top_10",{each:top_10[each]})

print(conn.zrange("top_10", 0, -1, desc=True))

# print(top_10)
print("finished successfully")