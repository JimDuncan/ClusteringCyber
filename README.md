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

###Data Cleaning, Feature Engineering, and choosing to cluster the data

What kind of dataframe do I know ultimately have?  It is a dataframe with over 4 million rows whose features include
source and destination IPs, source and destination ports, time of attack, and message column that had a small English description that specific data point.  Except for the time column all the columns/features were categorical.  There was no
primer or guide as to what exactly was going on.  I just had a data dump of 4 million observations. In order to
ascertain trends within the data and make sense of it I decided to use a clustering algorithm.  Given that I had mostly categorical features I chose the K-modes unsupervised learning technique.    

![alt tag](https://github.com/ajduncan3/ClusteringCyber/blob/master/Graphs/Annotated_heat_map.png)
