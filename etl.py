import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    """
    Function to process song data
    :param cur: connection cursor
    :param filepath: song file path
    :return: none
    """
    # open song file
    df = pd.read_json(filepath, lines=True)

    # insert song record
    song_data = song_data = df[['song_id', 'title', 'artist_id', 'year', 'duration']].values.tolist()
    assert (len(song_data) == 1) #Check to confirm we have one record
    cur.execute(song_table_insert, song_data[0])
    
    # insert artist record
    artist_data = df[['artist_id', 'artist_name', 'artist_location', 'artist_latitude', 'artist_longitude']] \
        .values.tolist()
    assert (len(artist_data) == 1) #Check to confirm we have one record
    cur.execute(artist_table_insert, artist_data[0])


def process_log_file(cur, filepath):
    """
    Function to process log data
    :param cur: connection cursor
    :param filepath: log file path
    :return: none
    """
    # open log file
    df_log = pd.read_json(filepath, lines=True) #creating a common data frames which can be used for User & Songplay 
    df_log['ts'] = pd.to_datetime(df_log['ts'])  # convert to timestamp

    # filter by NextSong action
    df = df_log[df_log['page'] == 'NextSong']
    

    # convert timestamp column to datetime
    df = df[['page', 'ts']].copy()  # create data frames for required columns
    try:
        df['hour'] = df.ts.dt.hour
        df['day'] = df.ts.dt.day
        df['week'] = df.ts.dt.week
        df['month'] = df.ts.dt.month
        df['year'] = df.ts.dt.year
        df['weekday'] = df.ts.dt.weekday
        t = df[['ts', 'hour', 'day', 'week', 'month', 'year', 'weekday']]
    except: print("Error decoding time stamp")
        
        
    # insert time data records
    #     time_data =         #not required in my code
    #     column_labels =
    time_df = t[['ts', 'hour', 'day', 'week', 'month', 'year', 'weekday']]

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df_log[['userId', 'firstName', 'lastName', 'gender', 'level']].copy()

    # insert user records
    for i, row in user_df.iterrows():
        if row.userId != "":   # Data quality check to handle NULL records - Do not insert ""
            cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df_log.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        if row.userId != "":   # Data quality check to handle NULL records - Do not insert ""
            songplay_data = (row.ts, row.userId, row.level,songid,artistid,row.sessionId,row.location,row.userAgent) 
            cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    """
    Function to process song and log json files
    :param cur: connection cursor
    :param conn: database connection details
    :param filepath: song/log file path
    :param func: calling process_song_file & process_log_file functions
    :return: none
    """
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()