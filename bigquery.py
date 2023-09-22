def list_sql_files_in_directory(directory_path):
    sql_files = []

    for filename in os.listdir(directory_path):
        if filename.endswith(".sql"):
            sql_files.append(filename)

    return sql_files
