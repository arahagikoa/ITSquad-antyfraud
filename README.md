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

## użycie modelu

By użyć już wytrenowanego modelu należy:
- wypakować plik z rozszerzeniem .zip w folderze model i umieścić go w tym samym folderze, nie zmieniając nazwy
- wybrać serie modelu do uzycia z folderu model
- podać ścieżkę do modelu w pliku predict.py w model_dir
- podać ścieżkę do zdjęcia, które chcemy zaklasyfikować pod zmienną: pred_img
- (opcjonalnie) podać prawidłowy label pod zmienną: true_label
- uruchomić plik predict.py 
- po krótkiej chwili wyświetli się, użyte zdjęcie wraz z przewidywaniem modelu

## Wymagania sprzętowe
Poza środowiskiem Python na kompuetrze, należy zainstalować dodatkowe biblioteki, zostały one zebrane, włącznie z kompatybilnymi wersjami, w pliku requirements.txt. Ptrzetrenowany model wymaga około 20 GB przestrzeni dyskowej na komputerze użytkownika.

## Licencje

Wszystkie użyte biblioteki jak i sam model jest na licencji wspierającej komercyjny użytek :)


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



# Image Classification API

API zostało stworzone w celu wystawienia aplikacji rozpoznawania oraz wyciągania danych z dokumentów, jako rozwiązanie stand-alone.

## Endpoints

### 1. Predict Images

**Endpoint:** `/API/predict`
**Method:** POST

Ten endpoint przyjmuje wiele zdjęć dokumentów oraz zwraca rozpoznane labele (wraz z danymi, które zostały odczytane)

#### Request

- **Content-Type:** `multipart/form-data`
- **Body:** 
  - `images`: Multiple image files

#### Response

- **Success Response:**
  - **Code:** 200
  - **Content:** 
    ```json
    {
      "message": "Successfully predicted labels for given images",
      "labels": [lista słowników JSON]
    }
    ```

- **Error Response:**
  - **Code:** 500
  - **Content:** 
    ```json
    {
      "error": "Error message"
    }
    ```

### 2. Get Records

**Endpoint:** `/API/get_records`
**Method:** GET

By nie przeprowadzać rozpoznawania jeszcze raz, możemy uzyskać dane z poprzedniej operacji, które zostaną zwrócone w takim samym formacie.

#### Response

- **Success Response:**
  - **Code:** 200
  - **Content:** 
    ```json
    {
      "message": "Got records from last prediction",
      "records": [lista słowników JSON]
    }
    ```

- **No Content Response:**
  - **Code:** 204
  - **Content:** 
    ```json
    {
      "message": "No records to obtain"
    }
    ```

## Usage Instructions

1. Na chwilę obecną aplikacja nie jest nigdzie wystawiona i była testowana na lokalnym środowisku.

2. By przeprowadzić analizę dokumentów:
   - Przygotowujemy request POST wycelowany w `/API/predict`
   - Załączamy zdjęcia potrzebne do analizy
   - Cieszymy się wynikiem

3. By uzyskać dane z poprzedniej predykcji:
   - Wysyłamy zapytanie GET na endpoint `/API/get_records`
   - Cieszymy się wynikiem


## Requirements

Aplikacja ze względu na użycie różnych modeli musi być wystawiona na środowisku z pythonem 3.8.x (preferowanie 3.8.19).
Lista potrzebnych bibliotek została zawarta poniżej:
 - tensorflow==2.4.0
 - keras==2.13.1
 - torch==1.13.1
 - torhvision==0.14.1
 - numpy==1.19.5
 - matplotlib==3.3.4
 - pytesseract==0.3.10
 - scipy==1.10.1
 - cython==3.0.10
 - scikit-image==0.19.3
 - opencv-python==4.10.0.84
 - h5py==2.10.0
 - imgaug==0.4.0
 - IPython==8.12.3
 - huggingface_hub==0.22.2
 - transformers==4.40.0
 - peft==0.10.0
 - Flask==2.3.3
 - flask_httpauth==4.8.0
 - flask_cors==4.0.0
 - langedetect==1.0.9

## Użytkowanie
Wymagania wstępne:
- Python 3.8 lub nowszy
- pytesseract
- OpenCV
- Zainstalowanie pliku requirements.txt, jednak najprawdopodobniej rozwiązanie będzie w formie odpalonego środowiska Jupyter, więc wystarczy uruchomić komórkę instalacyjną.

## Autorzy
- Kamil Krzemiński - Model CNN
- Aleksander Majkowski - Model NLP
