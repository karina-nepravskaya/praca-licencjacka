---
name: analyze-ionization-data
description: Reproduce and audit the ionization analysis in this repository from Jupyter notebooks, data files, tables, and plots without inventing results.
---

# Analiza danych jonizacyjnych

Stosuj ten skill do notebooków, kodu, danych, tabel, wykresów i wyników liczbowych. Celem jest odtworzenie rzeczywistego toku analizy, nie napisanie narracji pracy.

## Źródła prawdy

Najpierw przeczytaj \`ECBB_model/README.md\`, następnie notebooki istotne dla zadania. Dla głównego toku analizy są to przede wszystkim:

- \`05_PCA_full.ipynb\` — PCA dziewięciu składowych pędu;
- \`07_analiza_3D_clean.ipynb\` — analiza w stałej bazie i obserwable.

Sprawdź faktyczne nazwy i dostępność plików. Jeśli repozytorium zawiera nowszy odpowiednik, uzasadnij jego wybór.

## Procedura

1. Ustal aktywne pliki danych, intensywność pola, kanał (\`direct\`, \`delayed\`, \`all\`) i liczbę zdarzeń.
2. Prześledź definicje zmiennych oraz jednostki od wczytania danych do wyniku.
3. Uruchom notebook od czystego kernela. Stary stan pamięci nie jest dowodem reprodukowalności.
4. Sprawdź błędy, brakujące zmienne, nadpisania, filtrowanie, wartości NaN i zależność od kolejności komórek.
5. Dla każdego ważnego wyniku zapisz: użyte dane; metodę i definicję obserwabli; wynik liczbowy lub cechę wykresu; niepewność lub ograniczenie; test spójności.
6. Oddziel wynik bezpośrednio widoczny w danych od późniejszej interpretacji fizycznej.

## Kontrole obowiązkowe

Dla transformacji podłużnych pędów sprawdź numerycznie:

\[
Q=\frac{p_2+p_3+p_4}{\sqrt 3},\quad
\xi_1=\frac{p_2-p_3}{\sqrt 2},\quad
\xi_2=\frac{p_2+p_3-2p_4}{\sqrt 6},
\]

oraz zachowanie normy:

\[
p_2^2+p_3^2+p_4^2=Q^2+\xi_1^2+\xi_2^2.
\]

To jest ortogonalna zmiana bazy, a nie redukcja wymiaru.

Nie utożsamiaj końcowych współrzędnych z PC1, PC8 i PC9. PCA motywuje rozdzielenie trybu kolektywnego i względnego, lecz dalsza analiza używa stałej bazy.

Porównuj \`direct\` i \`delayed\` wyłącznie dla tej samej intensywności. Dla każdej różnicy podaj intensywność, kanał, liczbę zdarzeń i definicję obserwabli.

Nie analizuj ani nie opisuj obserwabli ILR.
