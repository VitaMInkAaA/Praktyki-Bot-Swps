# Automatyczny Wypełniacz Dziennika Praktyk (Wersja z Podłączeniem)

## Opis

Ta wersja skryptu w języku Python podłącza się do Twojej już otwartej przeglądarki Chrome, zamiast tworzyć nową. Pozwala to na wygodniejszą pracę, ponieważ nie musisz logować się za każdym razem. Skrypt jest uruchamiany po wciśnięciu klawisza `Enter` w terminalu.

## Kluczowe Funkcje

- **Podłączenie do Istniejącej Sesji**: Nie otwiera nowego okna, lecz kontroluje już otwartą przeglądarkę.
- **Prosta obsługa**: Uruchom skrypt, a następnie wciśnij `Enter`, gdy będziesz gotowy.
- **Wczytywanie z CSV**: Wszystkie dane do wprowadzenia są pobierane z pliku `PraktykiCSV.csv`.
- **Inteligentne Zaokrąglanie Czasu**: Godzina rozpoczęcia jest zaokrąglana w dół, a godzina zakończenia w górę do najbliższego kwadransa.

## Konfiguracja i Uruchomienie

### 1. Wirtualne Środowisko i Pakiety

#### Krok 1: Utwórz i aktywuj wirtualne środowisko

Jeśli jeszcze go nie masz, wykonaj:

```bash
python -m venv venv
```

**Aktywacja:**

**Dla macOS/Linux:**

```bash
source venv/bin/activate
```

**Dla Windows:**

```bash
.\venv\Scripts\activate
```

Po aktywacji, na początku wiersza poleceń powinna pojawić się nazwa `(venv)`.

#### Krok 2: Zainstaluj Wymagane Pakiety

Masz dwie opcje instalacji. Użyj Metody 1, jeśli masz plik `requirements.txt`.

**Metoda 1: Instalacja z pliku **

W aktywnym wirtualnym środowisku wykonaj jedną komendę, aby automatycznie zainstalować wszystkie potrzebne pakiety:

```bash
pip install -r requirements.txt
```

**Metoda 2: Instalacja ręczna**

Jeśli nie masz pliku `requirements.txt` lub chcesz zainstalować pakiety pojedynczo, wykonaj następujące komendy:

```bash
pip install pandas
pip install selenium
```

### 2. Uruchom Chrome w Trybie Debugowania (Najważniejszy Krok)

Aby skrypt mógł się podłączyć do Twojej przeglądarki, musisz ją uruchomić w specjalny sposób.

1. **Zamknij wszystkie otwarte okna przeglądarki Chrome.**
2. Otwórz terminal (macOS/Linux) lub Wiersz polecenia (Windows).
3. Wklej i wykonaj komendę odpowiednią dla Twojego systemu:

**Dla macOS:**

```bash
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222 --user-data-dir=~/ChromeDevSession
```

**Dla Windows:**

```bash
"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\ChromeDevSession"
```

**Dla Linux:**

```bash
google-chrome --remote-debugging-port=9222 --user-data-dir=~/ChromeDevSession
```

⚠️ **Ważne**: Po wykonaniu komendy otworzy się nowe okno Chrome. **Nie zamykaj tego okna ani terminala**, z którego je uruchomiłeś! Możesz je zminimalizować.

### 3. Przygotowanie Pliku z Danymi

1. Upewnij się, że plik `PraktykiCSV.csv` znajduje się w folderze projektu.
2. Plik musi używać przecinka (`,`) jako separatora.
3. **Krytycznie ważne**: Pierwszy wiersz (nagłówek) pliku musi zawierać dokładnie następujące nazwy kolumn: `data,start,end,opis`.

**Przykład poprawnego pliku CSV:**

```csv
data,start,end,opis,przepracowane godizny
01.10.2025,08:05,16:10,Programowanie modułu X,08:05
02.10.2025,09:00,17:20,Testowanie nowej funkcji,08:20
```

## Jak Używać Skryptu

### Krok po kroku:

1. **Uruchom Chrome w trybie debugowania** (zgodnie z krokiem 2 powyżej).

2. **W tej przeglądarce** zaloguj się na swoje konto i przejdź do strony z dziennikiem praktyk, gdzie widoczny jest przycisk "Utwórz wpis w dzienniku praktyki".

3. **W osobnym oknie terminala**, z aktywowanym środowiskiem `(venv)`, uruchom skrypt Pythona:

```bash
python practice_log_filler.py
```

4. Skrypt poinformuje Cię o dalszych krokach i poczeka. **Wróć do tego okna terminala i naciśnij `Enter`**.

5. Skrypt podłączy się do przeglądarki i rozpocznie automatyczne wypełnianie. **Nie używaj myszki ani klawiatury w tym czasie**.

## Rozwiązywanie Problemów

### Błąd: `ERROR: Could not connect to Chrome on port 9222`

Ten błąd oznacza, że skrypt nie mógł znaleźć przeglądarki Chrome uruchomionej w trybie debugowania. Upewnij się, że:

1. **Wszystkie inne okna Chrome zostały zamknięte** przed uruchomieniem komendy z kroku 2.
2. **Komenda do uruchomienia Chrome** została wklejona dokładnie tak, jak podano w instrukcji.
3. **Nie zamknąłeś** ani okna przeglądarki, ani terminala, w którym została uruchomiona.

**Test połączenia:**

Aby sprawdzić, czy Chrome działa poprawnie w trybie debugowania:

- Otwórz inną przeglądarkę (np. Safari, Firefox, Edge)
- Wejdź na adres: `http://127.0.0.1:9222`
- Jeśli zobaczysz stronę z listą zakładek lub tekstem JSON, wszystko jest w porządku
- Jeśli strona się nie ładuje, powtórz krok 2

### Inne problemy

- **Błąd odczytu CSV**: Sprawdź, czy plik ma prawidłową nazwę `PraktykiCSV.csv` i znajduje się w tym samym folderze co skrypt.
- **Skrypt nie znajduje elementów na stronie**: Upewnij się, że jesteś na właściwej stronie z widocznym przyciskiem "Utwórz wpis w dzienniku praktyki" przed naciśnięciem Enter.

## Wymagania Systemowe

- Python 3.7 lub nowszy
- System operacyjny: Windows, macOS lub Linux
- Przeglądarka Google Chrome zainstalowana w systemie
- Dostęp do internetu

## Zalety tej wersji

✅ Nie musisz logować się za każdym razem  
✅ Prostsza obsługa - tylko Enter zamiast skrótów klawiszowych  
✅ Możesz przeglądać strony w tej samej sesji przed uruchomieniem skryptu  
✅ Zachowuje wszystkie twoje rozszerzenia i ustawienia Chrome

## Uwagi Bezpieczeństwa

- Zawsze sprawdzaj, czy jesteś na właściwej stronie przed naciśnięciem Enter.
