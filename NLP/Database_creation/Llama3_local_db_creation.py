from langchain_community.llms import Ollama
import os
import json


llm = Ollama(model="llama3")

def get_model_response(topic):
    prompt = f"""
        <|begin_of_text|><|start_header_id|>system<|end_header_id|>
        Jesteś asystentem, który pomaga w generowaniu tekstu/dokumentów o danej tematyce. Zawsze odpowiadasz po POLSKU<|eot_id|><|start_header_id|>user<|end_header_id|>
        Stwórz tekst (między 150 -300 słów) na temat \n '{topic}'\n<|eot_id|><|start_header_id|>assistant<|end_header_id|>       
        """
    response = llm.invoke(prompt)
    return response

tematy = ["Notatka ze spotkania biznesowego", "Notatka z meczu futbolowego", "Oświadczeenia zrzeknięcia się praw autorskich", "Oświadczenie majątkowe",
          "notatka z interwencjii obywatelskiej", "notatka policji z miejsca kradzieży"]

data = []

for i in range(25):
    for item in tematy:
        response = get_model_response(item)
        data.append({
            "text": response,
            "label": "Nieznane"
        })
        print(response)

file_path = r"./Llama3_finetuning_db.json"

if os.path.exists(file_path):
    with open(file_path, "r", encoding="UTF-8") as file:
        existing_data = json.load(file)
else:
    existing_data = []

existing_data.extend(data)

with open(file_path, "w", encoding="UTF-8") as file:
    json.dump(existing_data, file, ensure_ascii=False, indent=2)

