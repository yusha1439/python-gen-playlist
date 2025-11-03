import sqlite3
import shutil
import os
from datetime import datetime

# Connect to the SQLite database
def connect_db(db_path):
    return sqlite3.connect(db_path)

# Function to copy the database and rename it using the first ply_start
def copy_and_rename_db(db_path, output_dir):
    # Connect to the original database to fetch the first ply_start date part
    conn = connect_db(db_path)
    cursor = conn.cursor()

    # Fetch the first row's ply_start
    cursor.execute("SELECT ply_start FROM playlist LIMIT 1")
    first_row = cursor.fetchone()
    
    # Extract the date and time part from the first ply_start row
    if first_row:
        first_ply_start = first_row[0]
        first_datetime = datetime.strptime(first_ply_start, "%Y-%m-%d %H:%M:%S.%f")

        # Format the datetime as required: YYYY_MM_DD_HH_MM_SS
        new_db_filename = first_datetime.strftime("%Y_%m_%d_%H_%M_%S") + ".ply"
        
        # Ensure the output directory exists
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Define the full path for the new file in the output directory
        new_db_path = os.path.join(output_dir, new_db_filename)
        
        # Copy the original db to the new location with the new filename
        shutil.copy(db_path, new_db_path)
        print(f"Database copied and renamed to {new_db_path}")
    
    # Close the connection
    conn.close()

if __name__ == "__main__":
    # Path to your SQLite database file
    db_path = r'V:\Playlist Creation\Create-Playlist\out.db'  # Adjust the path as needed
    # Path to the output directory
    output_dir = r'V:\Playlist Creation\Create-Playlist\output'  # Adjust the path as needed

    # Copy and rename the database file
    copy_and_rename_db(db_path, output_dir)
    
    print("Database copying and renaming complete.")
