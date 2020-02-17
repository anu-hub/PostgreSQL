Project Summary:

Sparkify wants to analyze the data they've been collecting on songs and user activity on their new music streaming app.
This involves creation of new database, creation of fact & dimention tables. Reading and processing song & log json files.

Data Modeling: 

Database: Sparkify

Fact Table: songplays (songplay_id pk)
Fact table is loaded from the log files based on the artist and song information from the songs collection data. 

Artist_Id & Song_Id - These columns are populated from songs and artists dimention table, based on the song title, song duration & artist name.
Start_Time,User_Id,Level,Session_ID,Location & user_agent - Log files


Dimension Tables: users(user_id pk), songs(song_id pk), artists(artist_id pk), time(start_time pk)

User & Time Dimenensions are populated from the log files.
Songs & Artist dimentions are populated from the songs collection files.

ER Diagram - Please refre to the ER_Diagram picture.


ETL: etl.py script 

We are using three scripts for the ETL process (inclusing the etl.py)
sql_queries: table creation, table drop, insert & select query formats are storted in this script, which is being imported in the etl.py scripy and create_table.py script.
create_tables.py : This script should be executed before the etl script, it will create the database and the tables (fact & dimension).

ETL script is reading the song & log json files from the data/song_data & data/log_data file path and processing the data before loading into the tables. 


Steps to execute the scripts:

1. Execte create_tables.py script - This creates the database & tables, also drops the tables if exists

2. sql_queries: No action required - This script is imported in create_table & etl script.
*This script has been modifies as per the review comments:
1. Added primary keys in all the tables
2. Added ON CONFLICT in the insert statements

2. Execute etl.py script  - This will read, transform and insert the data into the tables
*assert is used for song & artist insert to verify the record count in the file, assuming we have 1 record per file. Otherwise we will get assertion error exception.
*NULL values for the USER_ID column in the USERS table has been handeled in the script. USER_ID column doesn't have NULL values.
*After the ETL process only one song_id & artist_id is matching with the song collection data provided. Refre to the dashboard for the queries.

3. Run Dashboard.ipynb to generate the report on the data loaded. 
*Analayis on sparkify data.
