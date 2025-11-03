import sqlite3
import os
import re

# Connect to an existing SQLite database
def connect_db(db_path):
    return sqlite3.connect(db_path)

# Create the episode_metadata table
def create_episode_metadata_table(db_path):
    conn = connect_db(db_path)
    cursor = conn.cursor()

    # Create the episode_metadata table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS episode_metadata (
            ply_cat TEXT,
            ply_title TEXT,
            ply_path TEXT,
            ply_episode TEXT
        );
    ''')
    print("Created 'episode_metadata' table.")
    
    conn.commit()
    conn.close()

# Extract episode path and replace backslashes with spaces
def extract_episode_path(ply_path):
    # Match the part between 'V:\AV MEDIA\PROGRAM\' and the filename
    match = re.search(r'V:\\AV MEDIA\\PROGRAM\\(.*)\\[^\\]+$', ply_path)
    if match:
        # Replace backslashes with spaces
        episode_path = match.group(1).replace("\\", " ")  # Replacing "\" with " "
        return episode_path
    return None

# Populate the episode_metadata table based on playlist table
def populate_episode_metadata(db_path):
    conn = connect_db(db_path)
    cursor = conn.cursor()

    # Fetch relevant data from the playlist table
    cursor.execute("SELECT ply_cat, ply_title, ply_path FROM playlist WHERE ply_cat = 'Show'")
    rows = cursor.fetchall()

    # Insert data into the episode_metadata table
    for row in rows:
        ply_cat = row[0]
        ply_title = row[1]
        ply_path = row[2]
        
        # Extract the ply_episode part
        ply_episode = extract_episode_path(ply_path)
        
        if ply_episode:
            # Insert into episode_metadata
            cursor.execute('''
                INSERT INTO episode_metadata (ply_cat, ply_title, ply_path, ply_episode)
                VALUES (?, ?, ?, ?)
            ''', (ply_cat, ply_title, ply_path, ply_episode))
            print(f"Inserted into episode_metadata: {ply_cat}, {ply_title}, {ply_path}, {ply_episode}")
        else:
            print(f"Failed to extract ply_episode for path: {ply_path}")

    conn.commit()
    conn.close()

# Create the 'ep' table
def create_ep_table(db_path):
    conn = connect_db(db_path)
    cursor = conn.cursor()

    # Create the 'ep' table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ep (
            episode_name TEXT,
            episode_last_path TEXT
        );
    ''')
    print("Created 'ep' table.")
    
    conn.commit()
    conn.close()

# Populate the 'ep' table with distinct episodes and the last path for each
def populate_ep_table(db_path):
    conn = connect_db(db_path)
    cursor = conn.cursor()

    # Step 1: Get the distinct ply_episode and the last ply_path for each episode
    cursor.execute('''
        SELECT ply_episode, ply_path FROM episode_metadata
        ORDER BY ply_episode, ply_path DESC
    ''')
    rows = cursor.fetchall()

    last_path_dict = {}
    
    for row in rows:
        ply_episode = row[0]
        ply_path = row[1]

        # If the episode hasn't been recorded yet, add it
        if ply_episode not in last_path_dict:
            last_path_dict[ply_episode] = ply_path

    # Step 2: Insert the distinct episodes and their last ply_path into the 'ep' table
    for episode_name, episode_last_path in last_path_dict.items():
        cursor.execute('''
            INSERT INTO ep (episode_name, episode_last_path)
            VALUES (?, ?)
        ''', (episode_name, episode_last_path))
        print(f"Inserted into ep: {episode_name}, {episode_last_path}")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    # Path to your SQLite database
    db_path = r'V:\Playlist Creation\Create-Playlist\out.db'  # Path to the output SQLite database

    # Step 1: Create the episode_metadata table if it doesn't exist
    create_episode_metadata_table(db_path)

    # Step 2: Populate the episode_metadata table with data from the playlist
    populate_episode_metadata(db_path)

    # Step 3: Create the 'ep' table to store episode names and their last path
    create_ep_table(db_path)

    # Step 4: Populate the 'ep' table with the distinct episodes and their last path
    populate_ep_table(db_path)

    print("Successfully populated 'ep' table with episode names and last paths.")
