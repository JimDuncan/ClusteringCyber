# ClusteringCyber

A graphical representation of an SSH Honey Pot

##Project Summary

This project is intended to graphically illustrate pertinent aspects of a cybersecurity dataset.  The dataset is an SSH Honey Pot that
logged over 4 million possible attacks over the course of a week in 2009.  The goal of this project is to identify useful and interesting
trends amongst the given data.  Additionally, this project will hopefully educate the reader on ways to cluster data that is in categorical
form.

###Data Collection

I downloaded the data in .pcap form from an old data visualization contest for cybersecurity.  Link to contest here: http://2009.hack.lu/index.php/InfoVisContest#data_set.   I then used Wireshark to take an initial look at the data.  Wireshark
is a common network protocol analyzer.  

![alt tag](https://github.com/ajduncan3/ClusteringCyber/blob/master/Graphs/Wireshark_screengrab.png)

Wireshark has a variety of functionality, the most useful for this project was the ability to export all the information into
a csv file.  From there it was simple to load the .csv into a Pandas dataframe.  

###Data Cleaning, choosing to cluster the data, and feature engineering

What kind of dataframe do I know ultimately have?  It is a dataframe with over 4 million rows whose features include
source and destination IPs, source and destination ports, time of attack, and message column that had a small English description that specific data point.  Except for the time column all the columns/features were categorical.  There was no
primer or guide as to what exactly was going on.  I just had a data dump of 4 million observations. In order to
ascertain trends within the data and make sense of it I decided to use a clustering algorithm.  Given that I had mostly categorical features I chose the K-modes unsupervised learning technique.

Before I put my data into my K-modes algorithm I wanted to see if I could engineer some better features that would
be more useful than my initial data.  I was able to grab the source and destination port numbers from the message text.  Additionally, using IPinfo.com and their API, I was able to engineer Latitude, Longitude, City, and Country all from the
IP address.  Finally, I normalized the only continuous numerical variable I had, the time of each attack.

![alt tag](https://github.com/ajduncan3/ClusteringCyber/blob/master/Graphs/dataframe_screenshot.png)

###Using K-modes on the data
With all the data cleaned, I input it into K-modes to see what I kind of clustering I would get.  The goal was to
minimize the distance between clusters(cost) and maximize interpretability of the results.  The sweet spot of these two
seemed to be around 7 or 8.. I ended up going with 7 clusters.   

![alt tag](https://github.com/ajduncan3/ClusteringCyber/blob/master/Graphs/Elbow_Plot.png)

Below you can see how the source countries ended up clustering.  
![alt tag](https://github.com/ajduncan3/ClusteringCyber/blob/master/Graphs/Annotated_heat_map.png)

Probably the most illustrative visualization is the two graphs below.  This data is subsetted into 500 observations.
Immediately, below are the destination countries with the frequency of attack per country.  The second graph is the
exact same information but shows how the 500 observations ended being clustered.

###Next Steps

Use MCA,multiple categorical analysis, to further reduce the dimensionality of the data and hopefully
make the clusters even more insightful.  

Create a Netowrk X graph of the data to elucidate more trends and connections within the dataset.
