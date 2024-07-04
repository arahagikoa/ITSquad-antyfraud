from openai import AzureOpenAI
import json
import os

client = AzureOpenAI(
  azure_endpoint = "https://congo-republic.openai.azure.com/",
  api_key="4dbdb70b10404317a2c395b2c4bed529", 
  api_version="2023-12-01-preview"
)

messages = [
    {"role": "system", "content": """ Jesteś asystentem zaprojektowanym do tworzenia oświadczeń z kolizji drogowej. Zrób wszystko,
    co w twojej mocy aby oświadczenie wyglądało na napisane przez człowieka. Unikaj komentarzy oraz rysunków. Używaj nieoczywistych imion i nazwisk. Używaj dat z przedziału 1990 - 2024
    Zwracaj tylko oświadczenie. Nic więcej. Żadnych komentarzy."""},
    {"role": "user", "content": """
    Twoim zadaniem jest generowanie oświadczenia z kolizji samochodowej.
    Nie pisz komentarzy do żadnych danych.
    Oświadczenie zawierać powinno (w losowej kolejności, nie musi być ustrukturyzowane):
    – dane osobowe kierowców oraz właścicieli pojazdów. Zanotować należy imię, nazwisko, miejsce zamieszkania, numer serii dowodu osobistego i kategorię posiadanych praw jazdy osób kierujących pojazdami uczestniczącymi w kolizji. W przypadku, gdy kierowca któregoś z nich nie jest właścicielem pojazdu, trzeba podać również dane właściciela samochodu,
    – dane identyfikujące pojazdy, czyli numery rejestracyjne aut,
    – nazwę zakładu ubezpieczeniowego, w którym pojazd jest ubezpieczony, a także okres ważności i numery polis,
    – dokładną datę i dokładne miejsce zdarzenia,
    – opis zdarzenia i uszkodzenia pojazdów,
    – informację o przyznaniu się do winy przez sprawcę,
    – podpisy poszkodowanego oraz sprawcy kolizji. // W miejsce podpisu wpisz imię i nazwisko.
    Spisując oświadczenie kolizyjne dbaj o szczegóły. Aby zaoszczędzić sobie kłopotów przy likwidacji szkody, ważne jest, aby sporządzić dokładny opis okoliczności zdarzenia.  
    Ważny jest także dokładny opis tego, co zostało uszkodzone ze wskazaniem konkretnych elementów.
    """}
]

messages_bad = [
    {"role": "system", "content": """ Jesteś asystentem zaprojektowanym do tworzenia oświadczeń z kolizji drogowej. Zrób wszystko,
    co w twojej mocy aby oświadczenie wyglądało na napisane przez człowieka. Używaj nieoczywistych imion i nazwisk. Używaj dat z przedziału 1990 - 2024.
    Spraw aby notatka była niespójna oraz napisana źle. Chodzi o to abyś wygenerował przykład niepoprawnie napisanej notatki, mając instrukcje jak napisać poprawną.
    Zwracaj tylko oświadczenie. Nic więcej. Żadnych komentarzy"""},
    {"role": "user", "content": """
    Twoim zadaniem jest generowanie niepoprawnego oświadczenia z kolizji samochodowej.
    Nie wypisuj wszystkich rzeczy z poprawnie napisanego oświadczenia. Czasami używaj nieformalnego języka
    Oświadczenie zawierać powinno (w losowej kolejnośći, oraz nieustrukturyzowane):
    – dane osobowe kierowców oraz właścicieli pojazdów. Zanotować należy imię, nazwisko, miejsce zamieszkania, numer serii dowodu osobistego i kategorię posiadanych praw jazdy osób kierujących pojazdami uczestniczącymi w kolizji. W przypadku, gdy kierowca któregoś z nich nie jest właścicielem pojazdu, trzeba podać również dane właściciela samochodu,
    – dane identyfikujące pojazdy, czyli numery rejestracyjne aut,
    – nazwę zakładu ubezpieczeniowego, w którym pojazd jest ubezpieczony, a także okres ważności i numery polis,
    – dokładną datę i dokładne miejsce zdarzenia,
    – opis zdarzenia i uszkodzenia pojazdów,
    – informację o przyznaniu się do winy przez sprawcę,
    – podpisy poszkodowanego oraz sprawcy kolizji. // W miejsce podpisu wpisz imię i nazwisko.
    Spisując oświadczenie kolizyjne dbaj o szczegóły. Aby zaoszczędzić sobie kłopotów przy likwidacji szkody, ważne jest, aby sporządzić dokładny opis okoliczności zdarzenia.  
    Ważny jest także dokładny opis tego, co zostało uszkodzone ze wskazaniem konkretnych elementów.
    """}
]

data = []
total_cost = 0
iterations = 0

for i in range(50):
    response = client.chat.completions.create(
    model="kupilemliscie",
    messages=messages,
    )

    response2 = client.chat.completions.create(
    model="bolekilolek",
    messages=messages,
    )

    response3 = client.chat.completions.create(
    model="kupilemliscie",
    messages=messages_bad,
    )

    response4 = client.chat.completions.create(
    model="bolekilolek",
    messages=messages_bad,
    )

    completion_tokens = response.usage.completion_tokens
    prompt_tokens = response.usage.prompt_tokens
    total_cost1 = (prompt_tokens*0.0005 + completion_tokens*0.0015)/1000

    completion_tokens = response2.usage.completion_tokens
    prompt_tokens = response2.usage.prompt_tokens
    total_cost2 = (prompt_tokens*0.005 + completion_tokens*0.015)/1000

    completion_tokens = response3.usage.completion_tokens
    prompt_tokens = response3.usage.prompt_tokens
    total_cost3 = (prompt_tokens*0.0005 + completion_tokens*0.0015)/1000

    completion_tokens = response4.usage.completion_tokens
    prompt_tokens = response4.usage.prompt_tokens
    total_cost4 = (prompt_tokens*0.005 + completion_tokens*0.015)/1000

    for_loop_total_cost = total_cost1 + total_cost2 + total_cost3 + total_cost4
    total_cost += for_loop_total_cost

    data.append({
    "text": response.choices[0].message.content,
    "label": "Oświadczenie kolizji"
    })

    data.append({
    "text": response2.choices[0].message.content,
    "label": "Oświadczenie kolizji"
    })

    data.append({
    "text": response3.choices[0].message.content,
    "label": "Oświadczenie kolizji"
    })

    data.append({
    "text": response4.choices[0].message.content,
    "label": "Oświadczenie kolizji"
    })
    iterations += 1
    print(iterations)

file_path = r"./Llama3_finetuning_db.json"

if os.path.exists(file_path):
    with open(file_path, "r", encoding="UTF-8") as file:
        existing_data = json.load(file)
else:
    existing_data = []

existing_data.extend(data)

with open(file_path, "w", encoding="UTF-8") as file:
    json.dump(existing_data, file, ensure_ascii=False, indent=2)

print("total cost = " + str(total_cost))
