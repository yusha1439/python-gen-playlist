import sqlite3
import os

# Function to connect to the SQLite database
def connect_db(db_path):
    return sqlite3.connect(db_path)

# Function to update ply_out and update ply_title based on ply_path
def update_fields(db_path):
    # Connect to the database
    conn = connect_db(db_path)
    cursor = conn.cursor()

    # Step 1: Update ply_out to be the same as ply_duration for all rows
    cursor.execute('''
        UPDATE playlist
        SET ply_out = ply_duration;
    ''')

    # Step 2: Update ply_title for rows where ply_cat = 'Show' by extracting the filename from ply_path
    cursor.execute('''
        SELECT ply_id, ply_path
        FROM playlist
        WHERE ply_cat = 'Show';
    ''')

    # Fetch all rows where ply_cat = 'Show'
    rows = cursor.fetchall()

    for row in rows:
        ply_id = row[0]
        ply_path = row[1]

        # Extract the filename without the extension from ply_path
        filename = os.path.splitext(os.path.basename(ply_path))[0]

        # Update the ply_title for this row
        cursor.execute('''
            UPDATE playlist
            SET ply_title = ?
            WHERE ply_id = ?
        ''', (filename, ply_id))

        print(f"Updated ply_title for ply_id {ply_id}: {filename}")

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

if __name__ == "__main__":
    # Path to your SQLite database file
    db_path = r'V:\Playlist Creation\Create-Playlist\out.db'  # Update this path as necessary
    
    # Update ply_out and update ply_title
    update_fields(db_path)

    print("Successfully updated ply_out and ply_title.")
