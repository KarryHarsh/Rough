import pathlib
import re

def replace_strings_in_sql_files(directory_path, source_str, destination_str):
    # Create a Path object for the directory
    directory = pathlib.Path(directory_path)

    # Use a list comprehension to find all .sql files in the directory
    sql_files = [file for file in directory.glob("*.sql")]

    # Iterate through each SQL file and perform the replacement
    for sql_file in sql_files:
        with open(sql_file, "r") as file:
            sql_content = file.read()

        # Perform string replacements using regular expressions
        sql_content = re.sub(r'fs_analytics_tbls', destination_str, sql_content)
        sql_content = re.sub(r'ds_fraud_dmz', source_str, sql_content)

        # Write the modified content back to the file
        with open(sql_file, "w") as file:
            file.write(sql_content)

if __name__ == "__main__":
    directory_path = "path/to/your/sql/files"  # Replace with your directory path
    source_str = "{{source_dataset}}"
    destination_str = "{{destination_dataset}}"
    
    replace_strings_in_sql_files(directory_path, source_str, destination_str)
    print("String replacements completed.")
