import sqlite3

# Connect to the SQLite database
def connect_db(db_path):
    return sqlite3.connect(db_path)

# Remove rows where ply_cat = '[Fix Start]' except for the first row
def remove_fix_start_rows(db_path):
    conn = connect_db(db_path)
    cursor = conn.cursor()

    # First, get the id of the first row (ply_id = 0)
    cursor.execute("SELECT ply_id FROM playlist WHERE ply_id = 0")
    first_row = cursor.fetchone()

    if first_row:
        # Remove rows where ply_cat = '[Fix Start]' except for the first row
        cursor.execute('''
            DELETE FROM playlist
            WHERE ply_cat = '[Fix Start]' AND ply_id != 0
        ''')
        
        # Commit the changes and close the connection
        conn.commit()
        print("Rows with ply_cat = '[Fix Start]' (except first row) have been removed.")
    else:
        print("First row with ply_id = 0 not found.")

    conn.close()

if __name__ == "__main__":
    # Specify the path to your database
    db_path = r'V:\Playlist Creation\Create-Playlist\out.db'  # Path to the SQLite database

    # Call the function to remove the rows
    remove_fix_start_rows(db_path)
