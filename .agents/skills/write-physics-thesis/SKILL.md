---
name: write-physics-thesis
description: Write and revise the Polish LaTeX bachelor thesis from verified analysis results and scientific literature, with concise structure and disciplined terminology.
---

# Redakcja pracy licencjackiej

Stosuj do pisania i redakcji `main.tex`, rozdziałów, podpisów, tabel oraz `bibliography.bib`. Nie ustalaj samodzielnie wyników analizy; pobieraj je z aktualnie zweryfikowanych notebooków.

## Logika tekstu

Buduj narrację:

kontekst fizyczny → problem badawczy → dane → metoda → walidacja → wyniki → interpretacja → ograniczenia → wnioski.

Wprowadzaj pojęcie dopiero wtedy, gdy jest potrzebne. Nie zapowiadaj listy obserwabli kilka stron przed ich definicją. Wyniki grupuj według pytań fizycznych, nie według kolejności komórek notebooka.

Typowy fragment wynikowy powinien odpowiadać na ciąg:

pytanie → metoda → wynik lub rysunek → obserwacja → interpretacja → ograniczenie → krótki wniosek.

## Struktura

Użyj najmniejszej liczby rozdziałów i podrozdziałów potrzebnej do logicznego wywodu. Nie twórz podrozdziału dla jednego akapitu. Orientacyjny szkielet:

1. Wstęp i cel
2. Podstawy fizyczne potrzebne w analizie
3. Dane i metody
4. Wyniki i dyskusja
5. Wnioski
6. Dodatek techniczny, tylko gdy jest potrzebny

Dostosuj układ do materiału. Nie traktuj tego spisu jako obowiązkowego szablonu.

## Styl

Pisz po polsku, prosto, rzeczowo i technicznie. Preferuj krótkie zdania. Usuń watę typu „warto podkreślić niezwykle istotną rolę”, jeżeli nie wnosi informacji.

Każdy termin naukowy musi być rzeczywiście używany w polskiej literaturze. Nie twórz kalk językowych. Jeśli brak utrwalonego polskiego odpowiednika, użyj terminu angielskiego i objaśnij go przy pierwszym wystąpieniu.

Nie kopiuj błędów językowych z tekstów referencyjnych. Styl porównuj ze sprawozdaniem `Dlugosc_fali_Nepravskaya_Karina.pdf`, ale nie kopiuj jego zdań.

## Literatura i LaTeX

- Źródła naukowe wykorzystuj do teorii, metod i interpretacji, nie do zastępowania wyników z repozytorium.
- Cytuj tezę przy zdaniu, którego dotyczy.
- Nie dodawaj pozycji do `.bib`, której metadanych nie zweryfikowano.
- Każdy wzór, rysunek i tabela muszą zostać wprowadzone w tekście i wykorzystane w rozumowaniu.
- Zachowaj konsekwentne symbole; w szczególności nie utożsamiaj \(P_e\) z \(Q\).
- Tytuł pracy dopracuj po ustabilizowaniu treści, nie na początku.

Domyślnym rezultatem redakcji jest kompilowalny plik LaTeX i spójna bibliografia, chyba że zadanie wyraźnie dotyczy tylko szkicu lub recenzji.
