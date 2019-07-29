# Set directory in terminal
# cd /Users/...

''' General script is based loosely off of information from Github
regarding the pytrends pseudoAPI, supplied by the user General Mills
https://github.com/GeneralMills/pytrends/blob/master/README.md

Changes:
-Use of Pandas for CSV import
-Iteration over range of years
-Iteration over DMAs in imported CSV
-Download each year of daily data in two parts: Jan-Jun / Apr-Dec
-Iteration over dates for offset-day replicate downloads for each year-part
-Implement exponential backoff script to prevent Google server overloading error 429 
(rate of requests over accepted limit)


Implementation of exponential backoff script is based off of info from Google
https://cloud.google.com/iot/docs/how-tos/exponential-backoff
'''

# Import packages
from datetime import datetime, timedelta
from pytrends.request import TrendReq
import pandas as pd
import os
import time
from random import randint
import pandas


# Set download path 
path = '/Users/...'
os.chdir(path)
filename = 'test'

# Connect to Google
pytrends = TrendReq(hl='en-US', tz=360)

# Google Trends download parameters - array of search terms
# kw_list = ['ragweed']
kw_list = ['pollen','ragweed']

# Import GT-NAB matches csv
# state and dma code are for Google API input; nab name is for output filename
df = pandas.read_csv('GT-NAB-matches.csv', 
            names=['nabname', 'nabstate','dmaCodeMatch','completionLimit','vectorSeriesNum'])

# define local variables from csv
nabnameArray = df['nabname']
nabstateArray = df['nabstate']
dmaCodeMatchArray = df['dmaCodeMatch']

for i in range (1,len(nabnameArray)):

    # Set location 
    GeoLocation = 'US-' + str(nabstateArray[i]) + '-' + str(dmaCodeMatchArray[i])
    print(GeoLocation)
    # print('ragweed')

    iYear = 2012

    # iterate over years
    while iYear < 2018:
        iter1 = 1
        iter2 = 11

        # download first half of year
        while iter1 < 11:

            # Create new timeframe for which we download data
            timeframe = str(iYear) + '-1-1 ' + str(iYear) + '-6-' + str(iter1)

            # Build Payload
            pytrends.build_payload(kw_list=kw_list, timeframe=timeframe, geo=GeoLocation)
            interest_over_time_df = pytrends.interest_over_time()

            # save and output file
            filename = str(nabnameArray[i]) + '-' + str(iYear) + '-JanToJun' + '-' + str(iter1) + '.csv'
            # filename = str(nabnameArray[i]) + '-' + str(iYear) + '-JanToJun' + '-' + str(iter1) + 'ragweed.csv'

            interest_over_time_df.to_csv(filename)

            print(filename)
            iter1 = iter1 + 1 
        
            # truncated exponential backoff with introduced jitter to prevent overloading GT servers/429 error
            time.sleep((2^iter1) + randint(5, 10))
            print("sleep")

        # download second half of year
        while iter2 < 21:

            # Create new timeframe for which we download data
            timeframe = str(iYear) + '-4-' + str(iter2) + ' ' + str(iYear) + '-12-31'

            # Build Payload
            pytrends.build_payload(kw_list=kw_list, timeframe=timeframe, geo=GeoLocation)
            interest_over_time_df = pytrends.interest_over_time()

            # save and output file
            filename = str(nabnameArray[i]) + '-' + str(iYear) + '-AprToDec' + '-' + str(iter2) + '.csv'
            # filename = str(nabnameArray[i]) + '-' + str(iYear) + '-AprToDec' + '-' + str(iter2) + 'ragweed.csv'
            interest_over_time_df.to_csv(filename)

            print(filename)
            iter2 = iter2 + 1 

            # truncated exponential backoff with introduced jitter to prevent overloading GT servers/429 error
            time.sleep((2^iter2) + randint(5, 10))
            print("sleep")

        iYear = iYear + 1 
        print(iYear)





  

