from openai import AzureOpenAI
import json
import os

client = AzureOpenAI(
  azure_endpoint = "https://congo-republic.openai.azure.com/",
  api_key="4dbdb70b104ed529", 
  api_version="2023-12-01-preview"
)

messages = [
    {"role": "system", "content": """ Jesteś asystentem zaprojektowanym do tworzenia ekspertyzy z wypadku samochodowego rzeczoznawcy samochodowego. Zrób wszystko,
    co w twojej mocy aby notatka wyglądała na napisaną przez człowieka. 
    Nie zostawiaj żadnych danych nie wprowadzanych. Generuj je losowo. Jako podpis likwidatora wpisz imię i nazwisko likwidatora. Używaj dat z przedziału 1990 - 2024"""},
    {"role": "user", "content": """
    Twoim zadaniem jest generowanie ekspertyzy rzeczoznawcy z kolizji samochodowej. 
    Generuj tylko ekspertyze. Nic więcej. Żadnych dodatkowych komentarzy.
    Ekspertyza powinna zawierać dane rzeczoznawcy, dane zleceniodawcy, miejsce zdarzenia (bardzo dokładne, ze szczegółami - typu: skrzyżowanie 2 ulic (ulica 1 ,ulica 2) na rogu ze sklepem/pocztą/restauracja itd). 
    (To tylko przykład, wymyślaj swoje szczególy), dane pojazdów, któtki opis zdarzenia. Opis uszkodzeń oraz ich kosztorys. 
    Ekspertyza nie musi być ustrukturyzowana, kolejność może być losowa.
    """}
]

data = []
total_cost = 0
iterations = 0

for i in range(100):

  response1 = client.chat.completions.create(
      model="bolekilolek",
      messages=messages,
  )

  response2 = client.chat.completions.create(
      model="kupilemliscie",
      messages=messages,
  )

  completion_tokens = response1.usage.completion_tokens
  prompt_tokens = response1.usage.prompt_tokens
  total_cost1 = (prompt_tokens*0.005 + completion_tokens*0.015)/1000

  completion_tokens = response2.usage.completion_tokens
  prompt_tokens = response2.usage.prompt_tokens
  total_cost2 = (prompt_tokens*0.0005 + completion_tokens*0.0015)/1000

  for_loop_total_Cost = total_cost1 + total_cost2
  total_cost += for_loop_total_Cost
  iterations += 1
  print(iterations)
  print("total cost = " + str(total_cost))

  data.append({
    "text": response1.choices[0].message.content,
    "label": "Ekspertyza likwidatora"
    })

  data.append({
    "text": response2.choices[0].message.content,
    "label": "Ekspertyza likwidatora"
    })
  
file_path = r"./Llama3_finetuning_db.json"

if os.path.exists(file_path):
    with open(file_path, "r", encoding="UTF-8") as file:
        existing_data = json.load(file)
else:
    existing_data = []

existing_data.extend(data)

with open(file_path, "w", encoding="UTF-8") as file:
    json.dump(existing_data, file, ensure_ascii=False, indent=2)


