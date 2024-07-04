# ITSquad-antyfraud

## Ogólne roziwązanie

###Nasze rozwiązanie dzieli się na dwie główne części:

###CNN (Convolutional Neural Network) - Kamil Krzemiński

Pierwszym etapem jest przetworzenie dokumentu przez model, który służy do rozpoznawania obrazów dokumentów usystematyzowanych takich jak:
Polskie i zagraniczne prawo jazdy
Paszporty
####Dowody rejestracyjne
####Dowody osobiste
####Tablice rejestracyjne
Jeżeli model zwróci etykietę "Nieznane", rozwiązanie przechodzi do drugiego etapu.

###NLP (Natural Language Processing) - Aleksander Majkowski

Zdjęcie nierozpoznanego dokumentu jest przekazywane do OCR (używając pytesseract), który odczytuje tekst. Następnie odczytany tekst jest przetwarzany przez Duży Model Językowy (LLM) - Llama3 od MetaAI.
Model służy do rozpoznania trzech rodzajów dokumentów:
####Oświadczenie kolizji
####Notatka policyjna
####Ekspertyza likwidatora
Może również zwrócić etykietę "Nieznane", jeśli dokument nie pasuje do żadnego z rozpoznawanych typów.
Model zwraca klasyfikacje w postaci liczb całkowitych, które reprezentują przewidywane klasy dokumentów:
Nieznany - 3
Oświadczenie kolizyjne - 1
Ekspertyza - 2
Notatka policyjna - 0

##Użytkowanie
Wymagania wstępne
Python 3.8 lub nowszy
pytesseract
OpenCV
Zainstalowanie pliku requirements.txt, jednak najprawdopodobniej rozwiązanie będzie w formie odpalonego środowiska jupyter więc wystarczy uruchomić komórkę instalacyjną
