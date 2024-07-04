# ITSquad-antyfraud
## Ogólne rozwiązanie
Nasze rozwiązanie dzieli się na dwie główne części:

## CNN (Convolutional Neural Network) - Kamil Krzemiński
Pierwszym etapem jest przetworzenie dokumentu przez model, który służy do rozpoznawania obrazów dokumentów usystematyzowanych takich jak:

- Polskie i zagraniczne prawo jazdy
- Paszporty (rozdzelenie na polskie i zgraniaczne)
- Dowody osobiste (rozdzelenie na polskie i zgraniaczne)

Jeżeli model zwróci etykietę "inne", rozwiązanie przechodzi do drugiego etapu.
## Użyty model --- DiT-base

Po researchu zdecydowałem się użyć modelu DiT-base (Document Image Transformer). Jest to model przetrenowany przez Microsoft, na datasecie składającym się z 42 milionów zdjęć dokumentów. Wybrałem ten model, ponieważ jest on stworzony w celu rozwiązywania zadań typu: klasyfikacja dokumentów, analizy rozmieszczenia elementów w dokumencie, renoma firmy Mocrosoft również zadziałał na korzyść tego rozwiązania :)
## Dokładny opis folderu CNN

Całe rozwiązanie jest rozpiety na 3 folderach: dataset, model oraz test. Dodatkowo w celu uruchomienia i trenowania modeu potrzebujemy plików model-micr_dit-base-all.ipynb oraz predict.py. 

### dataset
tutaj znajduje się cały dataset użyty podczas trenowania oraz walidacji modelu. podfoldery train i validation są podzielone na foldery klasowe, w których znajdują się zdjęcia odpowiadające poszczególnym klasom.

### model
Znajdują się w nim kolejne 'edycje' modelu numerowane jako serie. Każdy z tych folderów jest osobnym, wytrenowanym na innych parametrach i różnych wariacjach datasecie. 
W pliku results.txt znajdują się logi z osiągów poszczególnych serii modelu.

### test
jest to folder z zawierający foldery odpowiadające klasom, powstał by umożliwić szybkie przetestowanie modelu na zdjęciach których model jeszcze nie "widział".

### model-micr_dit-base-all.ipynb

Najważniejszy plik projektu. Służy on do rozpoczęcia treningu modelu.

### predict.py
Ten skrypt Pythona umożliwia przetestowanie modelu. Zmieniając ścieżkę pod zmienną model_dir możemy przełączać się między kolejnymi wersjami modelu. Uruchomienie pliku spowoduje wykonania predykcji przez model, oraz zwrócenie zdjęcia wsadowego wraz z przewidzianą przez model klasą. W celu zmiany zdjęcia, należy podmienić ścieżke pod zmienną pred_img. 

### użycie modelu


### Wymagania sprzętowe
Poza środowiskiem Python na kompuetrze, który ma obsługiwać ten model należy zainstalować dodatkowe biblioteki, zostały one zebrane, włącznie z kompatybilnymi wersjami w pliku requirements.txt. 

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

Folder Database_creation zawiera pliki służące do tworzenia treningowej bazy danych (Klucze api w plikach są niepoprawne z oczywistych względów). 
- Plik LLama3_finetuning_db.json zawiera baze danych treningowych dla modelu Llama3 wygenerowaną przez AI na podstawie promptów w pozostałych plikach

Folder Training_model sklada się z 2 folderów:
- Saved_model - zawiera pliki konfiguracyjne przetrenowanego modelu. Używamy tego pliku do załadowania modelu w model_testing.ipynb
- training_code - zawiera 2 pliki final_llama_training przechowujący kod treningowy oraz model_testing.ipynb w którym można korzystać z przetrenowanego modelu.

Trenowanie modelu wymaga środowiska z pamięcią systemową RAM w okolicach 30 GB oraz minimum 12 GB na GPU

## Backend

Folder Backend będzie zawierał Backend :)

## Użytkowanie
Wymagania wstępne:
- Python 3.8 lub nowszy
- pytesseract
- OpenCV
- Zainstalowanie pliku requirements.txt, jednak najprawdopodobniej rozwiązanie będzie w formie odpalonego środowiska Jupyter, więc wystarczy uruchomić komórkę instalacyjną.

## Autorzy
- Kamil Krzemiński - Model CNN
- Aleksander Majkowski - Model NLP
