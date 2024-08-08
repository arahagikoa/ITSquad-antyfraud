import os
import json

data = []
for i in range(200):
    data.append(
        {
            "text": "",
            "label": "Nieznane"
        }
    )

#print(data)

file_path = r"C:\Users\olekm\OneDrive\Pulpit\ICFraud_github\ITSquad-antyfraud\NLP\Database_creation\Llama3_finetuning_db.json"

if os.path.exists(file_path):
    with open(file_path, "r", encoding="UTF-8") as file:
        existing_data = json.load(file)
else:
    existing_data = []

existing_data.extend(data)

with open(file_path, "w", encoding="UTF-8") as file:
    json.dump(existing_data, file, ensure_ascii=False, indent=2)
