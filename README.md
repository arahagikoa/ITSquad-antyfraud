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

## NLP (Natural Language Processing) - Aleksander Majkowski
Zdjęcie nierozpoznanego dokumentu jest przekazywane do OCR (używając pytesseract), który odczytuje tekst. Następnie odczytany tekst jest przetwarzany przez Duży Model Językowy (LLM) - Llama3 od MetaAI. Model służy do rozpoznania trzech rodzajów dokumentów:

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
