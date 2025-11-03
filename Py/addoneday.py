import sqlite3
import shutil
from datetime import datetime, timedelta
import os

# Connect to the SQLite database
def connect_db(db_path):
    return sqlite3.connect(db_path)

# Function to update ply_start by adding 1 day
def update_ply_start_by_1_day(db_path):
    conn = connect_db(db_path)
    cursor = conn.cursor()

    # Select all rows from the playlist table
    cursor.execute("SELECT ply_id, ply_start FROM playlist")
    rows = cursor.fetchall()

    # Loop through the rows and update the ply_start by adding 1 day
    for row in rows:
        ply_id = row[0]
        ply_start_str = row[1]

        # Parse the ply_start into a datetime object
        ply_start_datetime = datetime.strptime(ply_start_str, "%Y-%m-%d %H:%M:%S.%f")

        # Add 1 day to the date part (keep the time part same)
        new_ply_start = ply_start_datetime + timedelta(days=7)

        # Convert the updated datetime back to string format
        new_ply_start_str = new_ply_start.strftime("%Y-%m-%d %H:%M:%S.%f")

        # Update the ply_start in the database
        cursor.execute('''UPDATE playlist 
                          SET ply_start = ? 
                          WHERE ply_id = ?''', 
                       (new_ply_start_str, ply_id))
        print(f"Updated ply_start for ply_id {ply_id} to {new_ply_start_str}")

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

# Function to copy the database and create a .ply file
def copy_db_and_create_ply_file(db_path):
    # Make a copy of the SQLite database
    copy_db_path = db_path.replace('.db', '_copy.db')
    shutil.copy(db_path, copy_db_path)
    print(f"Database copied to {copy_db_path}")

    # Connect to the original database to fetch the first ply_start date part
    conn = connect_db(db_path)
    cursor = conn.cursor()

    # Fetch the first row's ply_start date part
    cursor.execute("SELECT ply_start FROM playlist LIMIT 1")
    first_row = cursor.fetchone()
    
    # Extract the date part from the first ply_start row
    if first_row:
        first_ply_start = first_row[0]
        first_date = datetime.strptime(first_ply_start, "%Y-%m-%d %H:%M:%S.%f").date()

        # Create a .ply file with the date part from the first ply_start
        ply_filename = f"{first_date}.ply"
        with open(ply_filename, 'w') as f:
            f.write(f"Playlist for {first_date}\n")
        print(f"Created .ply file: {ply_filename}")
    
    # Close the connection
    conn.close()

if __name__ == "__main__":
    # Path to your SQLite database file
    db_path = r'V:\Playlist Creation\Create-Playlist\out.db'  # Adjust the path as needed

    # Step 1: Update ply_start by adding 1 day to each date part
    update_ply_start_by_1_day(db_path)

    # Step 2: Create a copy of the database and generate a .ply file
    copy_db_and_create_ply_file(db_path)
    
    print("Database and .ply file processing complete.")
