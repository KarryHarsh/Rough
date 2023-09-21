import os
from google.cloud import bigquery

def execute_sql_file(sql_file_path, project_id, dataset_id):
    # Initialize a BigQuery client
    client = bigquery.Client(project=project_id)

    # Read the SQL query from the file
    with open(sql_file_path, "r") as sql_file:
        sql_query = sql_file.read()

    # Run the SQL query
    job_config = bigquery.QueryJobConfig()
    job_config.use_legacy_sql = False  # Use standard SQL syntax

    try:
        query_job = client.query(sql_query, job_config=job_config)
        query_job.result()  # Wait for the query to complete
        print("Query executed successfully.")
    except Exception as e:
        print(f"Error executing the query: {str(e)}")

if __name__ == "__main__":
    # Set your Google Cloud project ID
    project_id = "your-project-id"
    
    # Set the BigQuery dataset ID
    dataset_id = "your-dataset-id"

    # Specify the path to your SQL file
    sql_file_path = "path/to/your/query.sql"

    if not os.path.exists(sql_file_path):
        print("SQL file does not exist.")
    else:
        execute_sql_file(sql_file_path, project_id, dataset_id)
