# Mechiron
## Overview
[Mechiron] (http://mceranlevy.wixsite.com/shkifut-real) has been developed in order to unify the products information, its prices and other relevant metadata being published by the largest grocery stores in Israel on a daily basis and visualize into beautiful dashboards.
Now that its all **unified** into one place, anyone can navigate through the data, slice & dice and drill down into specific product's information easily.The information published by law and being updated frequently during the day (2~ hours). 

## Goal
It is a **non-profit initiative** and the goal is to give the power to the public! So anyone can navigate through the prices, manufacturers' details and other interesting information to spot trends and see in a **bird's eye-view** market information. 
Whats the price of a specific product over time?
Who are the main manufacturers that compete on the money that we spend as consumers?
What are the pricing trends for a specific products category?
and much more!

**Ah, hmmm, Its also an opensource project!** You can use it and I will be more than happy if you could contribute to it...

## The overall project structure
The **Mechiron** project has been seperated into 2 opensource GitHub repositories:
- Mechiron (this GitHub repository) - is responsible to gather the information published from the configured FTP sources and export into a unified CSV format. Written in Python and can be extended easily. For more information see the GitHub repository README.
- [MechironAnalyzer] (https://github.com/eran-levy/MechironAnalyzer) - which is reponsible for the data processing - see more information in the repository itself.

## Mechiron project structure
Its an experimental project and has been seperated into units:
- pricesgzextractor - extract the downloaded XML information from all sources that are located in the download folder into a CSV per store file, i.e. RamiLevi_YYYY-MM-dd_HH_mm_SS.csv
- storesextractor - extract the download stores XML file per store and unify all of them into a single stores CSV file
- rundataflow - download data from all the configured stores located in mechiron-config.cfg

## Prerequisite
Python 2.7.11

* Clone this repository into your local projects folder
* Configure the relevant properties under the mechiron/mechron-conf.cfg file
* Project can be opened using PyCharm or one of your favorite IDEs
* Run the rundataflow.py file for the complete process

For comments or further details, please don't hesitate to mail me anytime: mceranlevy@gmail.com
I will continue to maintain the project - new features, unit tests, better error handling, etc.
Stay tuned,
Eran Levy


