# Creating a simple database with PostgreSQL

This is a simple project to demonstrate how to setup a simple datatbase in postgreSQL, extract data from JSON files, transform the data and load the data into the anaytical tables. 

## Data Analysis
Let us create a simple datatbase for a fictitious music streaming company **Sparkify** whose requirement is to analyze the data they've been collecting on songs and user activity on their new music streaming app. To help Sparkify analyze their data, we will create a database and then fact and dimension tables. We will then read and process their log files and create a dashboard to summarize the data.

## Data Modeling: 
* Fact Table: songplays (songplay_id pk)
  Fact table is loaded from the log files based on the artist and song information from the songs collection data. 
  Artist_Id & Song_Id - These columns are populated from songs and artists dimention table, based on the song title, song duration &  
   artist name.
  Start_Time,User_Id,Level,Session_ID,Location & user_agent - Log files

* Dimension Tables: users(user_id pk), songs(song_id pk), artists(artist_id pk), time(start_time pk)
  User & Time Dimenensions are populated from the log files.
  Songs & Artist dimentions are populated from the songs collection files.

## ER Diagram
![ER_Diagram](https://github.com/anu-hub/PostgreSQL/blob/master/images/ER_Diagram.jpg)

## Extract Transform Load(ETL)
We will use three scripts for the ETL process
  1. ```sql_queries.py```: This file contains the queries which can be imported into ```etl.py``` and ```create_table.py```.
  2. ```create_tables.py```: This script will create our database and the tables.
  3. ```etl.py``` will read the JSON logs, transform the data and load into the tables in the database. 

## Running the project:
  1. Execute ```create_tables.py``` to create the database & tables
  2. Execute ```etl.py``` to read, transform and load the data into the tables
  3. In jupyter notebook run ```Dashboard.ipynb``` to generate a report with insights into our data. 
