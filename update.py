import csv

# Path to your CSV file
csv_file_path = r'E:\Projekty\for_work\db-data\ITSquad-antyfraud\excel\final.csv'

# Read data from CSV
updates = []
with open(csv_file_path, mode='r', newline='') as file:
    reader = csv.DictReader(file, delimiter=';')  # Adjust delimiter if necessary
    for row in reader:
        updates.append((
            row['incident_id'].strip(),  # Ensure no leading/trailing spaces
            row['incident_type_id'].strip(),  # Ensure no leading/trailing spaces
            row['location_id'].strip()  # Ensure no leading/trailing spaces
        ))

# Template for the SQL update statement
sql_template = """
UPDATE public.incident
SET 
    incident_type_id = CASE id 
        {incydent_status_id_cases}
    END,
    location_id = CASE id 
        {location_id_cases}
    END
WHERE id IN ({incident_ids});
"""

# Helper function to create CASE statements
def create_case_statements(updates, column_index):
    return " ".join([f"WHEN '{record[0]}' THEN '{record[column_index]}'::uuid" for record in updates])

# Creating the SQL update statement
incydent_type_id_cases = create_case_statements(updates, 1)
location_id_cases = create_case_statements(updates, 2)
incident_ids = ", ".join([f"'{record[0]}'::uuid" for record in updates])

# Format the SQL template with the case statements and incident ids
sql_update_statement = sql_template.format(
    incydent_status_id_cases=incydent_type_id_cases,
    location_id_cases=location_id_cases,
    incident_ids=incident_ids
)
# Print the SQL update statement
with open('./update_query.txt', 'w', encoding='utf-8') as f:
    f.write(sql_update_statement)

