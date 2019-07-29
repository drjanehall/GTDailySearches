# GTDailySearches
Python Script for downloading Google Trends daily search data in 10x replicate by year
Currently used for evaluating pollen patterns across the U.S, matching National Allergy Bureau (NAB) data matched 
with Google Trends (GT) data by smallest geographical unit (Desginated Market Area).


This script is based off of the Google Trends pseudo-API pytrends (https://github.com/GeneralMills/pytrends)

The following major changes were made:

-Use of Pandas for CSV import
-Iteration over range of years
-Iteration over DMAs in imported CSV
-Download each year of daily data in two parts: Jan-Jun / Apr-Dec
-Iteration over dates for offset-day replicate downloads for each year-part
-Implement exponential backoff script to prevent Google server overloading error 429 
(rate of requests over accepted limit)

The script used for this project evaluates searches of "pollen" and "ragweed" from 2012-2018.
