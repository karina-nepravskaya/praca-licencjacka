# Weryfikacja bibliografii i pochodzenia liczb

Data: 2026-09-17. Dotyczy `~/praca-licencjacka/main.tex` i `bibliography.bib`.

---

## Część 1. Czy źródła są prawdziwe?

> [!CAUTION]
> Twoja nieufność była uzasadniona. W bibliografii, którą wcześniej napisałem
> ręcznie, **dwa tytuły były zmyślone** i **jeden DOI był martwy**. Poniżej
> pełna lista tego, co było źle, i co z tym zrobiłem.

### Trzy realne błędy

| Klucz | Co było źle | Poprawka |
|---|---|---|
| `Peters2022` | Tytuł zmyślony: *„Ionization dynamics of strongly driven atoms in a three-dimensional semiclassical model"* | Prawdziwy tytuł wg wydawcy: *„General model and toolkit for the ionization of three or more electrons in strongly driven atoms using an effective Coulomb potential for the interaction between bound electrons"*, Phys. Rev. A **105**, 043102 (2022). DOI był poprawny. |
| `Katsoulis2018` | Tytuł zmyślony: *„…as a gate to ultrafast one-optical-cycle probing"* | Prawdziwy tytuł: *„Slingshot Nonsequential Double Ionization as a Gate to Anticorrelated Two-Electron Escape"*, Phys. Rev. Lett. **121**, 263203 (2018). |
| `Efimov2021` | DOI `10.1364/OE.427217` zwraca **HTTP 404** — nie istnieje | Poprawny DOI: **`10.1364/OE.431572`**, Optics Express **29**, 26526 (2021), tytuł *„Three-electron correlations in strong laser field ionization"*. Gold open access. |

### Błąd strukturalny: w PDF-ie w ogóle nie było DOI

Styl `unsrt` **po cichu pomija pole `doi`**. Skompilowana bibliografia nie
zawierała więc ani jednego linku — nikt (łącznie z Tobą) nie mógł kliknąć
i sprawdzić źródła. To jest właściwa przyczyna tego, że nie dało się
potwierdzić połowy pozycji.

Naprawione: DOI trafia teraz do pola `note` jako klikalny `\href`. W nowym
PDF-ie każda pozycja kończy się napisem `doi:10.…`.

Przy okazji poprawione: BibTeX zamieniał „Ne" → „ne", „He" → „he", „2D" → „2d"
i drukował nazwiska Simpsona i Welcha kapitalikami z bazy Crossref.

### Jak to zostało naprawione, żeby się nie powtórzyło

Bibliografia **nie jest już pisana ręcznie**. Generuje ją skrypt
[rebuild_bib.py](file:///usr/local/google/home/nepravskaya/.gemini/jetski/brain/dcc3adce-ae1f-4d51-bca8-dff7bf3d770f/scratch/rebuild_bib.py),
który dla każdego z 22 wpisów z DOI pobiera metadane **bezpośrednio z Crossref**
(czyli z tego, co zarejestrował wydawca) i z nich składa plik. Autor, tytuł,
czasopismo, tom, strony i rok nie mogą więc być wymyślone — pochodzą z API.

Cztery pozycje nie mają DOI i sprawdziłem je ręcznie:

- **`Ammosov1986`** — Sov. Phys. JETP **64**, 1191–1194 (1986); oryginał rosyjski
  Zh. Eksp. Teor. Fiz. **91**, 2008 (1986). Pełny tekst darmowy na `jetp.ras.ru`.
- **`Pedregosa2011`** — JMLR **12**, 2825–2830 (2011). JMLR nie nadaje DOI;
  otwarty dostęp na `jmlr.org`.
- **`Aitchison1986`** — książka, Chapman & Hall 1986, przedruk Blackburn Press 2003.
- **`Ojczenasz2023`** — praca licencjacka UJ, niepublikowana, dostępna tylko w APD UJ.

Stara wersja pliku leży w `weryfikacja/bibliography_przed_poprawka.bib`, gdybyś
chciała zobaczyć różnicę.

### Czy każdy ma dostęp?

| Dostępność | Liczba | Pozycje |
|---|---|---|
| **Darmowo online** | 12 | Emmanouilidou2023 (CC-BY), Peters2022 (arXiv), Katsoulis2018 (arXiv), Corkum1993, KrauszIvanov2009, Staudte2007, Rudenko2004 (arXiv), **Efimov2021 (gold OA)**, Thiede2018 (arXiv), Simpson1949, Harris2020 (CC-BY), Pedregosa2011 |
| **Za paywallem** | 12 | LHuillier1983, BeckerRottke2008, Moshammer2000, Rudenko2007, Dalitz1953, Lancaster1965, Jolliffe2002, Aitchison1986, Hill1973, Welch1947, Fisher1915, Hunter2007 |
| **Poza indeksami** | 2 | Ammosov1986 (darmowy na jetp.ras.ru), Ojczenasz2023 (tylko APD UJ) |

Paywall to standardowe APS / Wiley / Springer — **UJ ma te prenumeraty**, więc
z sieci uniwersyteckiej otworzysz je wszystkie. Recenzent też.

Pełne wyniki: `weryfikacja/bib_check_output.txt` (walidacja Crossref) i
`weryfikacja/access_output.txt` (status open access z OpenAlex).

---

## Część 2. Skąd pochodzi każda liczba w pracy

Uruchomiłem [trace_numbers.py](file:///usr/local/google/home/nepravskaya/praca-licencjacka/weryfikacja/trace_numbers.py),
który bierze wszystkie **351 unikalnych liczb** z `main.tex` i sprawdza,
w którym pliku da się je znaleźć.

| Grupa | Ile liczb | Gdzie to sprawdzisz |
|---|---|---|
| **A. Twoje notebooki** | 176 | `PCA_results/*.csv`, `momentum_sharing_results/*.csv` — otwierasz CSV i widzisz |
| **B. Dane źródłowe** | 17 | `ECBB_model/**/README.txt` |
| **C. Moja dodatkowa analiza** | 327 (w tym **158 tylko tutaj**) | `weryfikacja/verify_output.txt` |
| **Nigdzie wprost** | 8 | procenty przeliczone z ułamków, patrz niżej |

### Te 8 liczb, które nie są nigdzie zapisane wprost

Wszystkie to **ułamek pomnożony przez 100**. Sprawdziłem każdą:

| Liczba w pracy | Skąd |
|---|---|
| 43,8 % | `1695/3873` z liczby wierszy w plikach |
| 29,9 % / 19,8 % / 23,9 % / 4,9 % / 4,5 % / 8,1 % | `explained_variance_ratio` z `PCA_results/explained_variance.csv` (np. `0.2990226657730668` → 29,9 %) |
| 74,7 % | `frac(x_minority<0.15)=0.747` z `verify_output.txt` §10 |

### Czym jest grupa C i dlaczego jest duża

158 liczb istnieje **tylko** dlatego, że napisałem dodatkowy skrypt. To nie są
nowe wyniki — to **statystyka dołożona do Twoich wyników**:

- przedziały ufności 95 % dla każdej średniej,
- statystyki $t$ i wartości $p$ testu Welcha (porównania *direct* vs *delayed*),
- odniesienia zerowe z Monte Carlo ($\langle N_\text{eff}\rangle = 2{,}118$,
  $\langle x_\max\rangle = 11/18$),
- tabela ponderomotywna ($\omega$, $U_p$, $2\sqrt{U_p}$) — czysty rachunek z
  intensywności i długości fali,
- błędy walidacji ortogonalności ($3{,}3\cdot10^{-16}$ itd.),
- Dodatek A (tożsamość elektronu mniejszościowego).

> [!IMPORTANT]
> Skrypty, które je liczą, są teraz w `~/praca-licencjacka/weryfikacja/`.
> Możesz je uruchomić sama — **nie wymagają numpy ani pandas**, tylko czystego
> Pythona, i czytają bezpośrednio surowe pliki pędów z repozytorium:
>
> ```
> cd ~/praca-licencjacka/weryfikacja
> python3 verify_analysis.py        # główna re-analiza -> verify_output.txt
> python3 ponderomotive.py          # tabela U_p
> python3 simplex_reference.py      # odniesienia Monte Carlo
> ```
>
> `verify_analysis.py` nie korzysta z Twoich CSV — liczy wszystko od zera
> z plików `ECBB_model/…`. Jeśli jego wyniki zgadzają się z Twoimi notebookami
> (a zgadzają się), to jest to niezależne potwierdzenie, a nie kopia.

---

## Część 3. Stan kompilacji

| Sprawdzenie | Wynik |
|---|---|
| Błędy LaTeX | **0** |
| Niezdefiniowane `\ref` / `\cite` | **0** |
| Brakujące pliki | **0** |
| Liczba stron | 25 |
| Kontrola liczb (351 wartości vs 1643 wartości referencyjne) | wszystkie zgodne |
| Zakazane sformułowania z README (ILR, „redukcja wymiaru", „udowodniono", filler AI) | **0** |
| Folder `~/praca-licencjacka` kompiluje się samodzielnie | tak, 25 stron |

Pozostaje 10 ostrzeżeń `Overfull \hbox`. Przyczyna: lokalny TeX nie ma polskich
wzorców przenoszenia i dzieli słowa po angielsku („sprawd-zono"). **Na Overleaf
większość zniknie.**

---

## Do decyzji

Trzy pozycje są w `bibliography.bib`, ale **nigdzie w tekście ich nie cytuję**,
więc nie pojawiają się w skompilowanej bibliografii:

1. **`Efimov2021`** — *„Three-electron correlations in strong laser field ionization"*,
   Optics Express 2021. Grupa krakowska (Prauzner-Bechcicki, Zakrzewski).
   Temat: korelacje **trzech** elektronów — dokładnie Twój.
2. **`Thiede2018`** — też grupa krakowska.
3. **`Katsoulis2018`** — współautor Twojego głównego źródła danych.

Moja rekomendacja: zacytować wszystkie trzy we wstępie. Efimov2021 i Thiede2018
są prawdopodobnie z kręgu Twojego promotora, a Efimov2021 jest tematycznie
bliższy pracy niż połowa obecnego wstępu.
