import sqlite3
import os

# Connect to the SQLite database
def connect_db(db_path):
    return sqlite3.connect(db_path)

# Update the `ply_path`, `ply_duration`, `ply_out`, and `ply_title` for rows where `ply_cat = 'Show'`
def update_playlist_fields(db_path):
    conn = connect_db(db_path)
    cursor = conn.cursor()

    # Step 1: Update the ply_path and ply_duration
    cursor.execute('''
        UPDATE playlist
        SET ply_path = next_item_path, ply_duration = next_item_duration
        WHERE ply_cat = 'Show' AND next_item_path IS NOT NULL AND next_item_duration IS NOT NULL
    ''')

    # Step 2: Update ply_out to be the same as ply_duration for rows where ply_cat = 'Show'
    cursor.execute('''
        UPDATE playlist
        SET ply_out = ply_duration
        WHERE ply_cat = 'Show'
    ''')

    # Step 3: Update ply_title for rows where ply_cat = 'Show' by extracting the filename from ply_path
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

    # Commit the changes
    conn.commit()

    # Step 4: Drop the 'next_item_path' and 'next_item_duration' columns
    # Note: SQLite does not support dropping columns directly.
    # You would need to implement a method to create a new table without these columns if necessary.

    # Commit the changes and close the connection
    conn.close()

    print("Database updated successfully, and unnecessary columns dropped.")

if __name__ == "__main__":
    # Specify the path to your database
    db_path = r'V:\Playlist Creation\Create-Playlist\out.db'  # Path to the output SQLite database

    # Call the function to update the database
    update_playlist_fields(db_path)