def merge_nested_dicts(a, b):
    c = {}
    
    # Merge dictionary 'a' into 'c'
    for key_a, value_a in a.items():
        if key_a in c:
            # Merge subvalue and featurename
            for subkey, subvalue in value_a.items():
                if subkey in c[key_a]:
                    c[key_a][subkey].extend(subvalue)
                else:
                    c[key_a][subkey] = subvalue
        else:
            c[key_a] = value_a
    
    # Merge dictionary 'b' into 'c'
    for key_b, value_b in b.items():
        if key_b in c:
            # Merge subvalue and featurename
            for subkey, subvalue in value_b.items():
                if subkey in c[key_b]:
                    c[key_b][subkey].extend(subvalue)
                else:
                    c[key_b][subkey] = subvalue
        else:
            c[key_b] = value_b
    
    return c

# Example dictionaries a and b
a = {
    'subvalue1': {
        'featurename1': [
            {'feature1': 'featurevalue1'},
            {'feature2': 'featurevalue2'}
        ]
    }
}

b = {
    'subvalue2': {
        'featurename2': [
            {'featurea': 'featurevaluea'},
            {'featureb': 'featurevalueb'}
        ]
    }
}

# Merge dictionaries a and b into c
c = merge_nested_dicts(a, b)
print(c)




import os
import pandas as pd
import json

# Function to convert a DataFrame to a nested JSON
def dataframe_to_nested_json(df, filename, subscriber_id_col):
    nested_json = {}
    for _, row in df.iterrows():
        subscriber_id = row[subscriber_id_col]
        subset_json = row.drop(subscriber_id_col).to_dict()
        nested_json[subscriber_id] = {filename: subset_json}
    return nested_json

# Directory containing the CSV files
csv_directory = '/path/to/csv_directory'

# Iterate through CSV files in the directory
nested_json_data = {}

for filename in os.listdir(csv_directory):
    if filename.endswith('.csv'):
        csv_path = os.path.join(csv_directory, filename)
        df = pd.read_csv(csv_path)
        if 'subscriberid' in df.columns:
            nested_json = dataframe_to_nested_json(df, filename, 'subscriberid')
            nested_json_data.update(nested_json)

# Output the nested JSON
output_json = json.dumps(nested_json_data, indent=4)

# Print or save the JSON as needed
print(output_json)

# To save the JSON to a file, you can use the following code:
# with open('output.json', 'w') as json_file:
#     json_file.write(output_json)

