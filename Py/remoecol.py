import sqlite3

# Connect to the SQLite database
def connect_db(db_path):
    return sqlite3.connect(db_path)

# Function to remove the last two columns from the playlist table
def remove_last_two_columns(db_path):
    conn = connect_db(db_path)
    cursor = conn.cursor()

    # Step 1: Check the table schema (list of columns in playlist table)
    cursor.execute("PRAGMA table_info(playlist);")
    table_info = cursor.fetchall()

    # Get the column names from the schema info
    column_names = [col[1] for col in table_info]
    
    # Ensure there are at least 2 columns to drop
    if len(column_names) < 3:
        print("Error: The table does not have enough columns to remove.")
        conn.close()
        return
    
    # Last two columns to drop
    columns_to_keep = column_names[:-2]

    # Step 2: Create a new temporary table with the columns to keep
    create_table_query = f"CREATE TABLE playlist_temp ({', '.join([col + ' TEXT' for col in columns_to_keep])});"
    cursor.execute(create_table_query)

    # Step 3: Copy data from the original table to the new table (only the columns we want to keep)
    columns_to_insert = ", ".join(columns_to_keep)
    placeholders = ", ".join(["?" for _ in columns_to_keep])
    cursor.execute(f"INSERT INTO playlist_temp ({columns_to_insert}) SELECT {columns_to_insert} FROM playlist;")

    # Step 4: Drop the original table
    cursor.execute("DROP TABLE playlist;")

    # Step 5: Rename the temporary table to the original table name
    cursor.execute("ALTER TABLE playlist_temp RENAME TO playlist;")

    # Commit changes and close the connection
    conn.commit()
    conn.close()

    print(f"Last two columns removed and table renamed successfully.")

if __name__ == "__main__":
    # Specify the path to your SQLite database
    db_path = r'V:\Playlist Creation\Create-Playlist\out.db'  # Path to the SQLite database

    # Step 1: Remove the last two columns from the playlist table
    remove_last_two_columns(db_path)

    print(f"Database {db_path} updated successfully.")
