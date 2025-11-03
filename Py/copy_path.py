import sqlite3

# Connect to the SQLite database
def connect_db(db_path):
    return sqlite3.connect(db_path)

# Update the `ply_path` and `ply_duration` for rows where `ply_cat = 'Show'`
def update_ply_path_and_duration(db_path):
    conn = connect_db(db_path)
    cursor = conn.cursor()

    # Update the ply_path and ply_duration for rows where ply_cat = 'Show'
    cursor.execute('''
        UPDATE playlist
        SET ply_path = next_item_path, ply_duration = next_item_duration
        WHERE ply_cat = 'Show' AND next_item_path IS NOT NULL AND next_item_duration IS NOT NULL
    ''')

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

    print("Database updated successfully.")

if __name__ == "__main__":
    # Specify the path to your database
    db_path = r'V:\Playlist Creation\Create-Playlist\out.db'  # Path to the output SQLite database

    # Call the function to update the database
    update_ply_path_and_duration(db_path)