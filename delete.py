import csv

# Path to your CSV file
csv_file_path = r'E:\Projekty\for_work\db-data\ITSquad-antyfraud\excel\relation-incident-asset.csv'

# Read data from CSV
delete_conditions = []
with open(csv_file_path, mode='r', newline='') as file:
    reader = csv.DictReader(file, delimiter=';')  # Adjust delimiter if necessary
    for row in reader:
        delete_conditions.append(row['id_system_asset_extension'].strip())

# Template for the SQL delete statement
sql_template = """
DELETE FROM public.system_asset_extension
WHERE id IN ({condition_ids});
"""

# Creating the SQL delete statement
condition_ids = ", ".join([f"'{condition}'::uuid" for condition in delete_conditions])

# Format the SQL template with the condition ids
sql_delete_statement = sql_template.format(condition_ids=condition_ids)

# Print the SQL delete statement
with open('./delete_query_assets_relation.txt', 'w', encoding='utf-8') as f:
    f.write(sql_delete_statement)