import csv

# Path to your CSV file
csv_file_path = r'E:\Projekty\for_work\db-data\ITSquad-antyfraud\excel\relation-incident-asset.csv'

# Read data from CSV
updates = []
with open(csv_file_path, mode='r', newline='') as file:
    reader = csv.DictReader(file, delimiter=';')  # Adjust delimiter if necessary
    for row in reader:
        updates.append((
            row['victim'].strip()
        ))

# Template for the SQL update statement
sql_template = """
UPDATE public.relation_incident_asset
SET 
    system_asset_category_id = 'ca262f44-8af6-4074-aeae-6b68a2a4bb58'

WHERE system_asset_category_id IN ({incident_ids});
"""

# Helper function to create CASE statements
def create_case_statements(updates, column_index):
    return " ".join([f"WHEN '{record[0]}' THEN '{record[column_index]}'::uuid" for record in updates])

# Creating the SQL update statement
#incydent_type_id_cases = create_case_statements(updates, 1)
#location_id_cases = create_case_statements(updates, 2)
incident_ids = ", ".join([f"'{record}'::uuid" for record in updates])

# Format the SQL template with the case statements and incident ids
sql_update_statement = sql_template.format(
    incident_ids=incident_ids
)
# Print the SQL update statement
with open('./update_query_assets_relation.txt', 'w', encoding='utf-8') as f:
    f.write(sql_update_statement)

