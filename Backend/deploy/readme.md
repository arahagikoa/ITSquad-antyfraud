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