import sqlite3
import json

# Connect to an existing SQLite database
def connect_db(db_path):
    return sqlite3.connect(db_path)

# Load the JSON data
def load_json(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

# Check if the 'next_item_path' and 'next_item_duration' columns exist in the playlist table
def check_and_add_columns(db_path):
    conn = connect_db(db_path)
    cursor = conn.cursor()

    # Check the schema of the playlist table
    cursor.execute("PRAGMA table_info(playlist);")
    table_info = cursor.fetchall()

    # Check if 'next_item_path' and 'next_item_duration' columns exist in the table schema
    columns = [col[1] for col in table_info]
    if 'next_item_path' not in columns:
        cursor.execute('''ALTER TABLE playlist ADD COLUMN next_item_path TEXT;''')
        print("Column 'next_item_path' added to the playlist table.")
    
    if 'next_item_duration' not in columns:
        cursor.execute('''ALTER TABLE playlist ADD COLUMN next_item_duration TEXT;''')
        print("Column 'next_item_duration' added to the playlist table.")

    conn.commit()
    conn.close()

# Fetch the next item path from the JSON structure
def get_next_item_path(json_data, current_path):
    for folder in json_data['folders']:
        video_files = folder['video_files']
        for i, video_file in enumerate(video_files):
            path = video_file['path']
            if path == current_path:
                # Return the next item path (if exists)
                next_item = video_files[(i + 1) % len(video_files)]  # Wrap around for the next item
                return next_item['path'] if len(video_files) > 1 else None
    return None

# Update the 'next_item_path' and 'next_item_duration' in the database where 'ply_cat' = 'Show'
def update_next_item_info_from_json(db_path, json_path):
    # Load JSON data
    json_data = load_json(json_path)

    # Connect to the database
    conn = connect_db(db_path)
    cursor = conn.cursor()

    # Step 1: Fetch all records where ply_cat is 'Show'
    cursor.execute("SELECT ply_id, ply_path, ply_cat FROM playlist WHERE ply_cat = 'Show'")
    records_to_update = cursor.fetchall()

    # Step 2: For each record, fetch ply_episode from episode_metadata and get episode_last_path from ep table
    for row in records_to_update:
        ply_id = row[0]
        ply_path = row[1]
        ply_cat = row[2]

        # Fetch ply_episode from episode_metadata table
        cursor.execute("SELECT ply_episode FROM episode_metadata WHERE ply_path = ?", (ply_path,))
        ply_episode_row = cursor.fetchone()

        if ply_episode_row:
            ply_episode = ply_episode_row[0]

            # Fetch episode_last_path from ep table using ply_episode
            cursor.execute("SELECT episode_name, episode_last_path FROM ep WHERE episode_name = ?", (ply_episode,))
            ep_row = cursor.fetchone()

            if ep_row:
                episode_name = ep_row[0]
                episode_last_path = ep_row[1]

                # Step 3: Get next item path using episode_last_path from JSON data
                next_item_path = get_next_item_path(json_data, episode_last_path)

                if next_item_path:
                    # Step 4: Update the ep table with the new episode_last_path
                    cursor.execute('''UPDATE ep
                                      SET episode_last_path = ?
                                      WHERE episode_name = ?''',
                                   (next_item_path, episode_name))
                    print(f"Updated episode_last_path for {episode_name} to {next_item_path}")

                    # Step 5: Get next_item_duration from JSON data (optional)
                    next_item_duration = None
                    for folder in json_data['folders']:
                        for video_file in folder['video_files']:
                            if video_file['path'] == next_item_path:
                                next_item_duration = video_file.get('duration', None)
                                break

                    # Step 6: Update the playlist table with next_item_path and next_item_duration
                    cursor.execute('''UPDATE playlist
                                      SET next_item_path = ?, next_item_duration = ?
                                      WHERE ply_id = ?''',
                                   (next_item_path, next_item_duration, ply_id))
                    print(f"Updated next_item_path for ply_id {ply_id} to {next_item_path} with duration {next_item_duration}")
                else:
                    print(f"No next path available for episode {episode_name}.")
            else:
                print(f"No matching episode found for ply_episode {ply_episode}.")
        else:
            print(f"No matching ply_episode found for ply_path {ply_path}.")

    # Commit changes and close the connection
    conn.commit()
    conn.close()

if __name__ == "__main__":
    # Specify the paths to your database and JSON file
    db_path = r'V:\Playlist Creation\Create-Playlist\out.db'  # Path to the output SQLite database
    json_path = r'V:\Playlist Creation\Create-Playlist\json\video_files_meta.json'  # Path to the JSON file

    # Step 1: Check and add the 'next_item_path' and 'next_item_duration' columns if missing
    check_and_add_columns(db_path)

    # Step 2: Update the database with next_item_path, next_item_duration, and ply_path values from JSON
    update_next_item_info_from_json(db_path, json_path)

    print(f"Database updated successfully with next_item_path and next_item_duration values.")
