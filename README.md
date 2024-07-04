# ITSquad-antyfraud
## Ogólne rozwiązanie
Nasze rozwiązanie dzieli się na dwie główne części:

## CNN (Convolutional Neural Network) - Kamil Krzemiński
Pierwszym etapem jest przetworzenie dokumentu przez model, który służy do rozpoznawania obrazów dokumentów usystematyzowanych takich jak:

- Polskie i zagraniczne prawo jazdy
- Paszporty
- Dowody rejestracyjne
- Dowody osobiste
- Tablice rejestracyjne

Jeżeli model zwróci etykietę "Nieznane", rozwiązanie przechodzi do drugiego etapu.

## Dokładny opis folderu CNN

# Popisz się :)

## NLP (Natural Language Processing) - Aleksander Majkowski
Zdjęcie nierozpoznanego dokumentu jest przekazywane do OCR (używając pytesseract), który odczytuje tekst. Następnie odczytany tekst jest przetwarzany przez przetrwnowany Duży Model Językowy (LLM) - Llama3 od MetaAI. Model służy do rozpoznania trzech rodzajów dokumentów:

- Oświadczenie kolizji
- Notatka policyjna
- Ekspertyza likwidatora
  
  Może również zwrócić etykietę "Nieznane", jeśli dokument nie pasuje do żadnego z rozpoznawanych typów. Model zwraca klasyfikacje w postaci liczb całkowitych, które reprezentują przewidywane klasy dokumentów:

| Dokument                 | Klasyfikacja |
|--------------------------|--------------|
| Notatka policyjna        | 0            |
| Oświadczenie kolizyjne   | 1            |
| Ekspertyza likwidatora   | 2            |
| Nieznany                 | 3            |

## Dokładny opis folderu NLP

Folder NLP składa się z 2 głownych folderów:
- Database_creation
- Training_model

Folder Database_creation zawiera pliki służące do tworzenia treningowej bazy danych (Klucze api w plikach są niepoprawne z oczywistych względów). Plik LLama3_finetuning_db.json zawiera baze danych treningowych dla modelu Llama3 wygenerowaną przez AI na podstawie promptów w pozostałych plikach

Folder Training_model sklada się z 2 folderów:
- Saved_model - zawiera pliki konfiguracyjne przetrenowanego modelu. Używamy tego pliku do załadowania modelu w model_testing.ipynb
- training_code - zawiera 2 pliki final_llama_training przechowujący kod treningowy oraz model_testing.ipynb w którym można korzystać z przetrenowanego modelu
Trenowanie modelu wymaga środowiska z pamięcią systemową RAM w okolicach 30 GB oraz minimum 12 GB na GPU


## Użytkowanie
Wymagania wstępne
Python 3.8 lub nowszy
pytesseract
OpenCV
Instalacja
Zainstalowanie pliku requirements.txt, jednak najprawdopodobniej rozwiązanie będzie w formie odpalonego środowiska Jupyter, więc wystarczy uruchomić komórkę instalacyjną.

## Autorzy
- Kamil Krzemiński - Model CNN
- Aleksander Majkowski - Model NLP
