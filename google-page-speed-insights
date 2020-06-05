#Import Required Packages 
import json
import requests
import pandas as pd
import urllib
import time
from google.colab import files
import io
import numpy as np


#FOR GOOGLE COLAB ONLY

#Read a csv file
uploaded = files.upload() 
column_header='url' #name of the column

#Read CSV file in Google Colab
for key in uploaded.keys():
  filename = key
# Read the selected file into a Pandas Dataframe
df = pd.read_csv(io.BytesIO(uploaded[filename]))


#FOR STANDALONE FILES

df = pd.read_csv('file_path')
column_header='url' #name of the column

#Check the data frame
df.head()



#Create an object to hold the json

response_object = {}


# Iterate through the df
for i in range(0, len(df)):

        print('Requesting row #:', i)

        # Define request parameter
        url = df.iloc[i][column_header]

        #[use your own API key for page speed insights]
        # Make request
        pagespeed_results = urllib.request.urlopen('https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={}/&strategy=mobile&key=AIzaSyChv9I9NdMJSue4rXbPJPE195Gudy2mMec'\
            .format(url)).read().decode('UTF-8')

        # Convert to json format
        pagespeed_results_json = json.loads(pagespeed_results)

        # Insert returned json response into response_object
        response_object[url] = pagespeed_results_json
        time.sleep(30)
        
        print(response_object[url])

        #Optional download of json files, comment out to skip this step 
        #with open('pagespeed_results_json', 'w') as outfile:
            #json.dump(response_object[url], outfile)
        
        #files.download('pagespeed_results_json')



# Create dataframe to store field data responses
df_pagespeed_results = pd.DataFrame(
columns=['url',
         'FCP_category',
         'FCP_percentile',
         'FID_category',
         'FID_percentile',
         'Time_to_Interactive',
         'Speed_Index',
         'First_CPU_Idle',
         'First_Meaningful_Paint',
         'TTFB',
         'Total_Blocking_Time'])  

print(df_pagespeed_results)


#Putting the value from the object to the new dataframe

for (url, x) in zip(
    response_object.keys(),
    range(0, len(response_object))
):

        # URLs
        df_pagespeed_results.loc[x, 'url'] =\
            response_object[url]['lighthouseResult']['finalUrl']

        # Overall Category
        df_pagespeed_results.loc[x, 'Overall_Category'] =\
            response_object[url]['loadingExperience']['overall_category']   

        # Core Web Vitals     

        # Largest Contentful Paint    
        df_pagespeed_results.loc[x, 'Largest_Contentful_Paint'] =\
        response_object[url]['lighthouseResult']['audits']['largest-contentful-paint']['displayValue']

        # First Input Delay 
        fid = response_object[url]['loadingExperience']['metrics']['FIRST_INPUT_DELAY_MS']
        df_pagespeed_results.loc[x, 'First_Input_Delay'] = fid['percentile']

        # Cumulative Layout Shift    
        df_pagespeed_results.loc[x, 'Cumulative_Layout_Shift'] =\
        response_object[url]['lighthouseResult']['audits']['cumulative-layout-shift']['displayValue']

        # Additional Loading Metrics 

        # First Contentful Paint 
        df_pagespeed_results.loc[x, 'First_Contentful_Paint'] =\
        response_object[url]['lighthouseResult']['audits']['first-contentful-paint']['displayValue']

        # Additional Interactivity Metrics 

        # Time to Interactive  
        df_pagespeed_results.loc[x, 'Time_to_Interactive'] =\
        response_object[url]['lighthouseResult']['audits']['interactive']['displayValue']

        # Total Blocking Time   
        df_pagespeed_results.loc[x, 'Total_Blocking_Time'] =\
        response_object[url]['lighthouseResult']['audits']['total-blocking-time']['displayValue']

        # Speed Index
        df_pagespeed_results.loc[x, 'Speed_Index'] =\
        response_object[url]['lighthouseResult']['audits']['speed-index']['displayValue']



summary = df_pagespeed_results

#df_pagespeed_results.head()

#Download csv file 
summary.to_csv('pagespeed_results.csv')
files.download('pagespeed_results.csv')
