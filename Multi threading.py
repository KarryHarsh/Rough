folder_path = "path/to/your/folder"

# Check if the folder exists
if os.path.exists(folder_path) and os.path.isdir(folder_path):
    # Delete the folder
    os.rmdir(folder_path)
    print(f"Folder '{folder_path}' deleted successfully.")
else:
    print(f"Folder '{folder_path}' does not exist.")
