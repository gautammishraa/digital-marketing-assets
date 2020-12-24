from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

import pandas as pd

# Adding The Scope and Token
SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
KEY_FILE_LOCATION = './GoogleAnalytics Test-4362934d74d8.json'
VIEW_ID = 'xxxxxxxxxx'


# Initializing Google Analytics Reporting
def initialize_analyticsreporting():
    credentials = ServiceAccountCredentials.from_json_keyfile_name(KEY_FILE_LOCATION, SCOPES)
    analytics = build('analyticsreporting', 'v4', credentials=credentials)
    return analytics


# Get one report page
def get_report(analytics, pageTokenVar):
    return analytics.reports().batchGet(
        body={
            'reportRequests': [
                {
                    'viewId': VIEW_ID,
                    'dateRanges': [{'startDate': '365daysAgo', 'endDate': 'today'}],
                    'metrics': [{'expression': 'ga:users'},
                                {'expression': 'ga:goalCompletionsAll'},
                                {'expression': 'ga:sessions'}],
                    'dimensions': [{'name': 'ga:sourceMedium'}],
                    'pageSize': 100000,
                    'pageToken': pageTokenVar,
                    'samplingLevel': 'LARGE'
                }]
        }
    ).execute()


def handle_report(analytics, pagetoken, rows):
    response = get_report(analytics, pagetoken)

    # Header, Dimensions Headers, Metric Headers
    columnHeader = response.get("reports")[0].get('columnHeader', {})
    dimensionHeaders = columnHeader.get('dimensions', [])
    metricHeaders = columnHeader.get('metricHeader', {}).get('metricHeaderEntries', [])

    # Pagination
    pagetoken = response.get("reports")[0].get('nextPageToken', None)

    # Rows
    rowsNew = response.get("reports")[0].get('data', {}).get('rows', [])
    rows = rows + rowsNew
    print("len(rows): " + str(len(rows)))

    # Recursivly query next page
    if pagetoken != None:
        return handle_report(analytics, pagetoken, rows)
    else:
        # nicer results
        nicerows = []
        for row in rows:
            dic = {}
            dimensions = row.get('dimensions', [])
            dateRangeValues = row.get('metrics', [])

            for header, dimension in zip(dimensionHeaders, dimensions):
                dic[header] = dimension

            for i, values in enumerate(dateRangeValues):
                for metric, value in zip(metricHeaders, values.get('values')):
                    if ',' in value or ',' in value:
                        dic[metric.get('name')] = float(value)
                    else:
                        dic[metric.get('name')] = int(value)
            nicerows.append(dic)
        return nicerows


# Start
def main():
    analytics = initialize_analyticsreporting()

    global dfanalytics

    dfanalytics = []

    rows = []
    rows = handle_report(analytics, '0', rows)

    dfanalytics = pd.DataFrame(list(rows))
    print(dfanalytics.head())
    dfanalytics.to_csv('dfanalytics.csv') # Exporting the Analytics Report to CSV


if __name__ == '__main__':
    main()
