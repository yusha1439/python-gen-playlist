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

# Update the 'next_item_path' and 'next_item_duration' in the database where 'ply_cat' = 'Show'
def update_next_item_info_from_json(db_path, json_path):
    # Load JSON data
    json_data = load_json(json_path)

    # Create a mapping of video file paths to their next item paths and durations
    video_file_info = {}
    folder_first_files = {}  # To store the first file in each folder

    for folder in json_data['folders']:
        folder_name = folder['folder']
        video_files = folder['video_files']
        
        # Store the first file in the folder for later use
        if video_files:
            folder_first_files[folder_name] = video_files[0]['path']  # The first video file in the folder
        
        for i, video_file in enumerate(video_files):
            path = video_file['path']
            # Store the next item path and the duration of the next item, or None if this is the last item
            next_item_path = video_files[(i + 1) % len(video_files)]['path'] if len(video_files) > 1 else None
            next_item_duration = video_files[(i + 1) % len(video_files)]['duration'] if len(video_files) > 1 else None
            video_file_info[path] = {'next_item_path': next_item_path, 'next_item_duration': next_item_duration}

    # Connect to the database
    conn = connect_db(db_path)
    cursor = conn.cursor()

    # Step 1: Fetch all records where ply_cat is 'Show'
    cursor.execute("SELECT ply_id, ply_path, ply_cat FROM playlist WHERE ply_cat = 'Show'")
    records_to_update = cursor.fetchall()

    # Step 2: Update the next_item_path and next_item_duration for each record
    for row in records_to_update:
        ply_id = row[0]
        ply_path = row[1]
        ply_cat = row[2]

        # Now we go through the folders and check for a match in the video files
        for folder in json_data['folders']:
            folder_name = folder['folder']
            video_files = folder['video_files']

            # Check if any video file path matches the ply_path
            for i, video_file in enumerate(video_files):
                path = video_file['path']
                
                # If we find a matching ply_path, we need to update it
                if ply_path == path:
                    next_item_info = video_file_info.get(path)

                    if not next_item_info['next_item_path']:
                        # If no next_item_path, use the first file in the same folder
                        next_item_info['next_item_path'] = folder_first_files.get(folder_name)
                        next_item_info['next_item_duration'] = next_item_info.get('next_item_duration', '')

                    if next_item_info['next_item_path']:
                        # Update ply_path, ply_duration, next_item_path, and next_item_duration
                        cursor.execute('''UPDATE playlist 
                                           SET next_item_path = ?, next_item_duration = ? 
                                           WHERE ply_id = ?''',
                                       (next_item_info['next_item_path'], next_item_info['next_item_duration'], ply_id))
                        print(f"Updated {ply_path} (ID: {ply_id}) with next_item_path {next_item_info['next_item_path']} and next_item_duration {next_item_info['next_item_duration']}")
                    else:
                        print(f"No next item available for {ply_path} and no first item found in folder.")
                    break  # Break the inner loop once we have matched the ply_path

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
