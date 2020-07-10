#This code is especially for Google Colab

#Import necessary packages

import pandas as pd
from googlesearch import search
from google.colab import files
import io
import time


#Upload the CSV file consisting of Keywords (Make sure the header of column is "keyword"

#Read a csv file
uploaded = files.upload() 
column_header='keyword' #name of the column

#Read CSV file in Google Colab
for key in uploaded.keys():
  filename = key
# Read the selected file into a Pandas Dataframe
df = pd.read_csv(io.BytesIO(uploaded[filename]))

#Get user input for the no of results to look into
num = int(input("No of Google Search Results to look into, eg: 10, 20, 30:"))

#take domain name from user

domain_name = input("Enter your domain name:")

url_list = []
keyword = []
rank = []

for i in range(0, len(df)):
  print('Processing Keyword #', i+1)
  key = df.iloc[i][column_header]
  for url in search(key, tld='com', num = num, stop = num, pause=3.0):
    url_list.append(url) 
  for i in range (1, num+1):
    kw = key
    keyword.append(kw)
    rank.append(i)
  time.sleep(20)
  
d = {'Keyword': keyword, 'Rank':rank, 'URL': url_list}


result = pd.DataFrame(d)
result = result[result['URL'].str.contains(domain_name)]

result.to_csv('keyword_ranking.csv') 
files.download('keyword_ranking.csv')
