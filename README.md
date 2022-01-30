# sp500_historical_components
Historical components of the S&amp;P500 and other indexes.

Many sources give the current components of the S&amp;P500, but the historical components are hard to find for free. At the same time, many blogs show how to get the current components yourself from Wikipedia, but for historical components they rely on Wikipedia's list of selected changes, which is far from complete. 

Here, we fill this gap by looking at Wikipedia's revision history to get the historical components. 

## Problems and Disclaimer
The Wikipedia lists sometimes have errors and are not always up to date. Check the data for anomalies and use at your own risk. 

## How it Works
The current S&ampP500 components are listed on Wikipedia at [List of S&P500 companies](https://en.wikipedia.org/wiki/List_of_S%26P_500_companies). Since Wikipedia saves the full revision history for every article, if we want to see what the S&amp;P500 components were in October 2015, we just need to access any revision from around that time. We can do this using the MediaWiki API. 

