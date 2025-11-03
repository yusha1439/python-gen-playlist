import os
import shutil
from datetime import datetime

# Define the source and destination folders
source_folder = r'V:\Playlist Creation\Create-Playlist\Source'  # Folder containing the single .ply file
destination_file = r'V:\Playlist Creation\Create-Playlist\out.db'  # The file to be overwritten with the renamed .ply file

# Function to rename the .ply file (using the current timestamp for the new name)
def rename_ply_file(file_name):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    new_name = f"renamed_{timestamp}.ply"  # Or use a different naming convention
    return new_name

# Function to move and overwrite out.db with the renamed .ply file
def overwrite_out_db(source_folder, destination_file, ply_file):
    source_ply_path = os.path.join(source_folder, ply_file)
    
    if not os.path.exists(source_ply_path):
        print(f"Error: The file {ply_file} does not exist in the source folder.")
        return
    
    # Rename the .ply file
    new_ply_name = rename_ply_file(ply_file)
    new_ply_path = os.path.join(source_folder, new_ply_name)
    
    # Copy and rename the .ply file to the destination (overwriting out.db if it exists)
    shutil.copy2(source_ply_path, destination_file)  # Copy with metadata (timestamps)
    print(f"Renamed {ply_file} to {new_ply_name} and copied to {destination_file}.")
    
    # Optionally, you can remove the original .ply file from the source folder after moving it
    # os.remove(source_ply_path)  # Uncomment if you want to remove the source file

# Main workflow
if __name__ == "__main__":
    # List the files in the source folder and assume there's only one .ply file
    files = [f for f in os.listdir(source_folder) if f.endswith('.ply')]
    
    if len(files) == 1:
        ply_file = files[0]
        print(f"Found .ply file: {ply_file}")
        
        # Overwrite out.db with the renamed .ply file
        overwrite_out_db(source_folder, destination_file, ply_file)
    else:
        print("Error: There should be exactly one .ply file in the source folder.")
