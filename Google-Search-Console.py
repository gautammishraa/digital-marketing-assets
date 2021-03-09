# Retrieve all search data from Google Search Console


import pickle
import pandas as pd

from datetime import datetime, timedelta
from google_auth_oauthlib.flow import InstalledAppFlow
from apiclient.discovery import build

SITE_URL = "https://medigence.com"
OAUTH_SCOPE = ('https://www.googleapis.com/auth/webmasters.readonly', 'https://www.googleapis.com/auth/webmasters')
REDIRECT_URI = 'urn:ietf:wg:oauth:2.0:oob'
SECRET_KEY = "/Users/gautammishra/Desktop/MediGence Data Analytics/Google Search Console/client_secrets.json"


# This is auth flow walks you through the Web auth flow the first time you run the script and stores the credentials in a file
# Every subsequent time you run the script, the script will use the "pickled" credentials stored in config/credentials.pickle
try:
    credentials = pickle.load(open("credentials.pickle", "rb"))
except (OSError, IOError) as e:
    flow = InstalledAppFlow.from_client_secrets_file(SECRET_KEY, scopes=OAUTH_SCOPE)
    credentials = flow.run_console()
    pickle.dump(credentials, open("credentials.pickle", "wb"))

# Connect to Search Console Service using the credentials
webmasters_service = build('webmasters', 'v3', credentials=credentials)

maxRows = 25000
i = 0
output_rows = []
start_date = datetime.strptime("01-03-2020", "%d-%m-%Y")
end_date = datetime.strptime("28-02-2021", "%d-%m-%Y")


def date_range(start_date, end_date, delta=timedelta(days=1)):
    current_date = start_date
    while current_date <= end_date:
        yield current_date
        current_date += delta

for date in date_range(start_date, end_date):
    date = date.strftime("%Y-%m-%d")
    print(date)
    i = 0
    while True:

        request = {
            'startDate' : date,
            'endDate' : date,
            'dimensions' : ["query","page","device","country"],
            "searchType": "Web",
            'rowLimit' : maxRows,
            'startRow' : i * maxRows

        }


        response = webmasters_service.searchanalytics().query(siteUrl = SITE_URL, body=request).execute()
        print()
        if response is None:
            print("there is no response")
            break
        if 'rows' not in response:
            print("row not in response")
            break
        else:
            for row in response['rows']:
                keyword = row['keys'][0]
                page = row['keys'][1]
                device = row['keys'][2]
                country = row['keys'][3]
                output_row = [date, keyword, page, device, country, row['clicks'], row['impressions'], row['ctr'], row['position']]
                output_rows.append(output_row)
            i = i + 1


df = pd.DataFrame(output_rows, columns=['date','query','page', 'country', 'device', 'clicks', 'impressions', 'ctr', 'avg_position'])
df.to_csv("GoogleSearchConsole.csv")
