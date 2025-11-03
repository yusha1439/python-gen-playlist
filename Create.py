import subprocess

#Rename file
file1_rename = r"V:\Playlist Creation\Create-Playlist\Py\rename-db.py"

# Path to the first Python file gets the next path
#file1_path = r"C:\Users\domain\Videos\new5.py" 
#file1_path = r"B:\Create-Playlist\Py\nextpath.py"

#Create next table
file1_path = r"V:\Playlist Creation\Create-Playlist\Py\create-next-table.py"

#Update next item from next table
file_Next_path = r"V:\Playlist Creation\Create-Playlist\Py\find-using-next-table.py"

#Renames
file11_path = r"V:\Playlist Creation\Create-Playlist\Py\update-nextpath.py"

#Copy path
copy_path = r"V:\Playlist Creation\Create-Playlist\Py\copy_path1.py"

# Path to the second Python file Removes Last two coloms nexth path and next duration
file2_path = r"V:\Playlist Creation\Create-Playlist\Py\remoecol.py"

# Path to the Third Python file Removes Fix Start
file3_path = r"V:\Playlist Creation\Create-Playlist\Py\remove-fix-start.py"

# Path to the Third Python file Removes Fix Start from ply_start
#file33_path = r"V:\Playlist Creation\Create-Playlist\Py\remove-fix-start2.py"

# Path to the Third Python file adds one day to the ply_start
file4_path = r"V:\Playlist Creation\Create-Playlist\Py\addoneday.py"

# Path to the Third Python file copies name
file5_path = r"V:\Playlist Creation\Create-Playlist\Py\copyname.py"

# Run the first Python file
subprocess.run(["python", file1_rename])

subprocess.run(["python", file1_path])

subprocess.run(["python", file_Next_path])

subprocess.run(["python", file11_path])

subprocess.run(["python", copy_path])

# Run the second Python file
subprocess.run(["python", file2_path])

# Run the second Python file
subprocess.run(["python", file3_path])

# Run the second Python file
#subprocess.run(["python", file33_path])

# Run the second Python file
subprocess.run(["python", file4_path])

# Run the second Python file
subprocess.run(["python", file5_path])

print("Both scripts have been executed successfully.")
