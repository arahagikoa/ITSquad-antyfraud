from openai import AzureOpenAI
import json
import os

client = AzureOpenAI(
  azure_endpoint = "https://congo-republic.openai.azure.com/",
  api_key="4dbdb70b10404317a2c395b2c4bed529", 
  api_version="2023-12-01-preview"
)

messages = [
    {"role": "system", "content": """ Jesteś asystentem zaprojektowanym do tworzenia notatki policyjnej z kolizji drogowej. Zrób wszystko,
    co w twojej mocy aby notatka wyglądała na napisaną przez policjanta. Unikaj nadmiernych komentarzy oraz rysunków. Używaj oryginalnych imion i nazwisk.
    Nie zostawiaj żadnych danych nie wprowadzanych. Generuj je losowo. Jako podpis funkcjonariusza wpisz imię i nazwisko funkcjonariusza. Używaj dat z przedziału 1990 - 2024"""},
    {"role": "user", "content": """
    Twoim zadaniem jest generowanie notatki policyjnej z kolizji samochodowej.
    Generuj tylko notatke. Nic więcej, żadnych komentarzy.
    W notatce policyjnej znajdują się przede wszystkim:

    -Miejsce zdarzenia (bardzo dokładne, ze szczegółami - typu: skrzyżowanie 2 ulic (ulica 1 ,ulica 2) na rogu ze sklepem/pocztą/restauracja itd). (To tylko przykład, wymyślaj swoje szczególy)
    -Dane uczestników zdarzenia
    -Charakter kolizji
    -Opcje świadków: (1. brak świadków, 2. świadkowie imię i nazwisko 3. świadkowie, ale niezidentyfikowani)
    -Informacje, które mogą okazać się znaczące w toku ustalenia strony winnej.
     
    Rzeczy w notatce mogą być generowanie w sposób nieustrukturyzowany.
    """}
]

data = []
total_cost = 0
iterations = 0

total_cost = 0
file_path = r"./Llama3_finetuning_db.json"

if os.path.exists(file_path):
    with open(file_path, "r", encoding="UTF-8") as file:
        existing_data = json.load(file)
else:
    existing_data = []

for i in range(100):
    response1 = client.chat.completions.create(
        model="kupilemliscie",
        messages=messages,
    )

    response2 = client.chat.completions.create(
        model="bolekilolek",
        messages=messages,
    )

    data.append({
    "text": response1.choices[0].message.content,
    "label": "Notatka policyjna"
    })

    data.append({
      "text": response2.choices[0].message.content,
      "label": "Notatka policyjna"
      })
  

    completion_tokens = response1.usage.completion_tokens
    prompt_tokens = response1.usage.prompt_tokens
    total_cost1 = (prompt_tokens * 0.0005 + completion_tokens * 0.0015) / 1000

    completion_tokens = response2.usage.completion_tokens
    prompt_tokens = response2.usage.prompt_tokens
    total_cost2 = (prompt_tokens * 0.005 + completion_tokens * 0.015) / 1000

    for_loop_total_cost = total_cost1 + total_cost2
    total_cost += for_loop_total_cost
    print("total cost = " + str(total_cost))
    iterations += 1
    print(iterations)

    existing_data.extend(data)

with open(file_path, "w", encoding="UTF-8") as file:
    json.dump(existing_data, file, ensure_ascii=False, indent=2)