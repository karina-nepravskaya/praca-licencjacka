---
name: manage-thesis-repository
description: Safely modify and verify this thesis repository, including LaTeX, notebooks, figures, bibliography, file organization, and consistency checks.
---

# Zarządzanie repozytorium pracy

Stosuj ten skill przy zmianach w plikach lub strukturze repozytorium oraz przy końcowej weryfikacji pracy.

## Przed zmianą

1. Sprawdź stan i strukturę repozytorium.
2. Przeczytaj `AGENTS.md` oraz pliki bezpośrednio związane z zadaniem.
3. Wyszukaj istniejące definicje symboli, etykiety rysunków i cytowania, aby ich nie dublować.
4. Nie traktuj zapisanych outputów notebooka jako aktualnych bez sprawdzenia danych i kolejności wykonania.

## Zasady zmian

- Zachowuj ręczne zmiany autora, chyba że są błędne lub sprzeczne z zadaniem.
- Twórz małe, logiczne diffy.
- Nie łącz bez potrzeby zmian fizyki, stylu tekstu i infrastruktury LaTeX.
- Po zmianie nazwy pliku, rysunku lub labela popraw wszystkie odwołania.
- Nie przenoś treści między plikami tylko dla estetyki, jeżeli nie poprawia to struktury pracy.
- Nie zapisuj sekretów, danych dostępowych ani lokalnych ścieżek użytkownika.

## Weryfikacja

Dobierz testy do zakresu zmiany:

- LaTeX: skompiluj dokument, sprawdź błędy, ostrzeżenia, odwołania i cytowania.
- Notebook: uruchom od czystego kernela przez `Restart Kernel → Run All`.
- Analiza: porównaj liczby w tekście z aktualnymi outputami.
- Bibliografia: sprawdź, czy każde cytowanie istnieje w `.bib`, a każda kluczowa teza ma właściwe źródło.

Na końcu podaj krótko: co zmieniono, dlaczego oraz czego nie udało się zweryfikować.
