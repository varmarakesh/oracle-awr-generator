# Oracle-Awr-Generator #

This project is for generating AWR (automation workload repository) data from Oracle database and load it hadoop distributed file system/hive for analysis.
AWR captures Oracle database stats. For more info, refer to this link.

https://docs.oracle.com/cd/E11882_01/server.112/e41573/autostat.htm#PFGRF02601

The AWR data is loaded by each snapshot and the solution loads all snapshots data for the current day it runs. To leverage concurrency in loading
the AWR data, the generate_awr.py spawns multiple threads and each threads work on extracting one snapshot data at a time.

Also, we used a queue solution, Apache Kafka, to assist in pushing the AWR data to its final solution. 

This has been tested so far using.
*python 2.7
*mac osx 10.9.5
*centos 7