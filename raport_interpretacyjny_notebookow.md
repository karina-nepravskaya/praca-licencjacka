# Raport interpretacyjny analizy pędów elektronów w potrójnej jonizacji neonu

## Cel i zakres

Raport odtwarza tok analizy zapisany w repozytorium `karina-nepravskaya/praca-licencjacka` i ustala, które wnioski są rzeczywiście podparte danymi. Analizę wykonano dla stanu gałęzi `main` z commitu `e7fb50ae2ce4b95fa1b5e6c9fcbe32e795bc38a7` z 16 września 2026 r.

Uwzględniono:

- `05_PCA_full.ipynb`;
- `07_analiza_3D_clean.ipynb`;
- cztery notebooki `3_momentum_described_v.3.ipynb` dla natężeń 1.0, 1.3, 1.6 i 1.7 PW/cm²;
- cztery automatyczne kopie z katalogów `.ipynb_checkpoints`;
- zapisane wyniki komórek, tabele CSV i wykresy wygenerowane przez notebooki;
- surowe pliki pędów, wykorzystane do niezależnego sprawdzenia najważniejszych statystyk i kilku zależności, których notebook nie pokazuje jawnie.

Nie analizowano ILR jako obserwabli fizycznej, zgodnie z instrukcją repozytorium. Wykresy ILR zostały jednak sprawdzone jako część audytu notebooka i opisane w sekcji o ograniczeniach.

## 1. Dane wejściowe

Każdy wiersz pliku zawiera dwanaście końcowych składowych pędu:

\[
(p_{1x},p_{1y},p_{1z},p_{2x},p_{2y},p_{2z},p_{3x},p_{3y},p_{3z},p_{4x},p_{4y},p_{4z}).
\]

W dokumentacji modelu cząstka 1 jest rdzeniem, cząstki 2 i 3 są elektronami początkowo związanymi, a cząstka 4 jest elektronem, który jako pierwszy tuneluje. Są to etykiety trajektorii w modelu, a nie fundamentalne cechy rozróżnialnych elektronów.

Dla 1.0, 1.3 i 1.6 PW/cm² impuls ma długość 25 fs i długość fali 800 nm. Zbiór 1.7 PW/cm² ma tę samą długość impulsu, ale długość fali 760 nm. Punktu 1.7 PW/cm² nie wolno więc traktować jako kolejnego punktu czystego skanu natężenia przy wszystkich pozostałych parametrach stałych.

### 1.1. Liczby zdarzeń i skład próbki `all`

| Natężenie [PW/cm²] | `all` | `direct` | `delayed` | inne zdarzenia w `all` | udział `direct` | udział `delayed` |
|---:|---:|---:|---:|---:|---:|---:|
| 1.0 | 4872 | 2042 | 2097 | 733 (15.0%) | 41.9% | 43.0% |
| 1.3 | 13769 | 6198 | 5837 | 1734 (12.6%) | 45.0% | 42.4% |
| 1.6 | 18578 | 8799 | 7560 | 2219 (11.9%) | 47.4% | 40.7% |
| 1.7 | 3873 | 1695 | 1601 | 577 (14.9%) | 43.8% | 41.3% |

Pliki `direct` i `delayed` są rozłącznymi podzbiorami odpowiadającego im pliku `all`. Zbiór `all` nie jest jednak sumą tylko tych dwóch kanałów. Zawiera od około 12% do 15% zdarzeń należących do innych ścieżek. Z tego powodu `all` nie powinien być używany jako niezależna grupa kontrolna dla `direct` i `delayed`.

Uwaga: dokumentacja zbioru 1.7 PW/cm² podaje udział `direct` równy 40.7%, natomiast liczba wierszy daje 1695/3873 = 43.8%. Udział `delayed` zgadza się z dokumentacją: 1601/3873 = 41.3%. Jest to niespójność wymagająca wyjaśnienia u autora danych.

## 2. Odtworzony tok analizy

## 2.1. Starsze notebooki simpleksowe dla poszczególnych natężeń

Notebooki `3_momentum_described_v.3.ipynb` wykonują następujące kroki:

1. Wczytują wyłącznie podłużne składowe pędów trzech elektronów: faktycznie `p2z`, `p3z`, `p4z`.
2. Dla każdego zdarzenia obliczają

   \[
   x_i=\frac{|p_{iz}|}{|p_{2z}|+|p_{3z}|+|p_{4z}|}.
   \]

3. Rozdzielają zdarzenia na osiem sektorów znakowych.
4. Przedstawiają udziały \((x_2,x_3,x_4)\) na wykresach trójkątnych.
5. Dla sektorów `+++` i `---` stosują wszystkie sześć permutacji współrzędnych. Dla sektorów mieszanych ustawiają elektron o znaku przeciwnym jako wyróżniony i zamieniają miejscami dwa elektrony o zgodnym znaku.

Jest to reprezentacja względnych wartości bezwzględnych pędu. Zachowuje informację o podziale wartości \(|p_z|\), lecz traci skalę całkowitą. Informację o znakach zachowuje dopiero osobny podział na sektory.

### Co widać na wykresach simpleksowych

- Dla zdarzeń o trzech zgodnych znakach największa gęstość leży z dala od wierzchołków, najczęściej w pobliżu części centralnej trójkąta. Oznacza to, że zdarzenia z całkowitą dominacją jednego elektronu są rzadsze niż zdarzenia, w których bezwzględny pęd dzieli kilka elektronów.
- Rozkład `direct` w części zgodnoznakowej jest bardziej skupiony w pobliżu równomiernego podziału niż rozkład `delayed`.
- W sektorach mieszanych gęstość przesuwa się ku krawędzi odpowiadającej małemu udziałowi elektronu o znaku przeciwnym. Tę obserwację należy traktować jakościowo, ponieważ wykres jest częściowo zniekształcony przez błąd permutacji opisany dalej.
- Liczby na skalach kolorów różnią się między panelami i zbiorami. Nie wolno porównywać samych kolorów jako względnych prawdopodobieństw.

Te wykresy są zgodne z późniejszymi wynikami dla \(N_{\mathrm{eff}}\), \(x_{\max}\) i sektorów znakowych, ale nie dostarczają od nich niezależnej informacji: wszystkie te wielkości powstają z tych samych trzech udziałów \(x_i\).

## 2.2. PCA dziewięciu składowych pędu

Notebook `05_PCA_full.ipynb` analizuje dziewięć składowych pędu elektronów:

\[
(p_{2x},p_{2y},p_{2z},p_{3x},p_{3y},p_{3z},p_{4x},p_{4y},p_{4z}).
\]

Dla każdego natężenia i każdej klasy zdarzeń PCA jest dopasowywana osobno. Przed PCA każda z dziewięciu zmiennych jest standaryzowana do średniej 0 i wariancji 1. Analiza dotyczy więc macierzy korelacji, a nie surowej macierzy kowariancji w jednostkach pędu.

### Najważniejszy wynik PCA

PC1 jest prawie całkowicie podłużna i ma zbliżone współczynniki przy `p2z`, `p3z`, `p4z`. Jej zgodność z kierunkiem

\[
\mathbf e_0=(1,1,1)/\sqrt 3
\]

wynosi od 0.996 do praktycznie 1.000. PC8 i PC9 są również w większości podłużne i razem rozpinają płaszczyznę względnych różnic pędów. Wyjątkiem jest PC8 dla `delayed`, 1.7 PW/cm², gdzie udział podprzestrzeni podłużnej wynosi około 90%, a więc domieszka składowych poprzecznych nie jest całkiem pomijalna.

| Klasa | Zakres udziału wariancji PC1 | Zakres łącznego udziału PC8+PC9 | Bezpośrednia obserwacja |
|---|---:|---:|---|
| `direct` | 29.65–30.03% | 3.33–3.71% | duża zmienność w kierunku kolektywnym i mała w dwóch kierunkach względnych |
| `delayed` | 19.21–20.13% | 13.21–14.65% | mniejsza dominacja kierunku kolektywnego i większa zmienność względna |
| `all` | 23.93–25.03% | 8.32–9.42% | wynik pośredni, zgodny z mieszaniną ścieżek |

PC8 i PC9 nie są stabilnymi, indywidualnymi osiami fizycznymi. Ich znaki są arbitralne, a przy zbliżonych wartościach własnych osie mogą się obracać lub zamieniać miejscami. Widać to np. dla `all` przy 1.0 PW/cm², gdzie obie osie są mieszaninami dwóch ustalonych kierunków względnych. Stabilnym wynikiem jest podprzestrzeń rozpięta przez PC8 i PC9, nie nazwa konkretnej składowej.

Standaryzacja ma znaczenie interpretacyjne. Odchylenia standardowe `p2z`, `p3z`, `p4z` różnią się w poszczególnych zbiorach nawet o około 13%. Równe współczynniki PCA odnoszą się więc do zmiennych standaryzowanych. Nie są dokładnie tym samym co równy udział surowych pędów.

### Wniosek z PCA

**Wniosek bezpośredni:** struktura korelacji w dziewięciowymiarowych danych wyróżnia jeden prawie czysto podłużny kierunek wspólny oraz dwuwymiarową, prawie podłużną podprzestrzeń ruchu względnego.

**Dopuszczalna interpretacja:** PCA uzasadnia dalsze osobne badanie ruchu kolektywnego i względnego wzdłuż osi polaryzacji.

**Niedopuszczalna interpretacja:** PCA nie dowodzi mechanizmu recollision ani nie identyfikuje sama z siebie kanału jonizacji.

## 2.3. Stała baza kolektywno-względna

Notebook `07_analiza_3D_clean.ipynb` przechodzi od zależnej od zbioru bazy PCA do stałej bazy ortonormalnej:

\[
Q=\frac{p_2+p_3+p_4}{\sqrt3},\qquad
\xi_1=\frac{p_2-p_3}{\sqrt2},\qquad
\xi_2=\frac{p_2+p_3-2p_4}{\sqrt6}.
\]

Tutaj \(p_i\) oznacza \(p_{iz}\). Transformacja zachowuje wymiar i normę:

\[
p_2^2+p_3^2+p_4^2=Q^2+\xi_1^2+\xi_2^2.
\]

Maksymalne błędy numeryczne zachowania normy są rzędu \(10^{-14}\), a błędy rekonstrukcji pędów rzędu \(10^{-15}\). Implementacja transformacji jest więc numerycznie poprawna w granicach precyzji zmiennoprzecinkowej.

Definiowane są następnie:

\[
P_e=p_2+p_3+p_4=\sqrt3Q,
\]

\[
K=\sqrt{\xi_1^2+\xi_2^2}.
\]

Zachodzi również użyteczna tożsamość

\[
K^2=\sum_{i=2}^4(p_i-\bar p)^2
=\frac{(p_2-p_3)^2+(p_2-p_4)^2+(p_3-p_4)^2}{3}.
\]

`K` jest zatem miarą rozrzutu **podpisanych** pędów względem ich średniej, a nie czystą miarą nierówności udziałów bezwzględnych. Przykład \((1,1,-1)\) ma równe wartości bezwzględne, czyli \(N_{\mathrm{eff}}=3\), ale niezerowe i duże \(K\). To rozróżnienie jest kluczowe dla interpretacji kanałów o różnym udziale sektorów mieszanych.

## 3. Najważniejsze wyniki

## 3.1. Ruch kolektywny: rozkład \(P_e\)

Rozkłady \(P_e\) są dwumodalne, z płatami dla dodatniego i ujemnego całkowitego pędu elektronów. Średnia \(P_e\) jest bliska zeru głównie wskutek symetrii obu płatów i nie opisuje ich szerokości ani położenia.

| Natężenie | średnie \(|P_e|\), `direct` | średnie \(|P_e|\), `delayed` | mediana \(|P_e|\), `direct` | mediana \(|P_e|\), `delayed` |
|---:|---:|---:|---:|---:|
| 1.0 | 6.47 | 4.32 | 6.52 | 4.35 |
| 1.3 | 7.06 | 4.80 | 7.25 | 4.84 |
| 1.6 | 7.32 | 4.96 | 7.60 | 5.02 |
| 1.7 | 7.16 | 4.86 | 7.42 | 4.89 |

**Dane i metoda:** podłużne pędy trzech elektronów; suma \(P_e\), wykresy \(P_e\)-\(K\) oraz niezależnie obliczone średnie i mediany \(|P_e|\).

**Efekt:** przy każdym natężeniu rozkład `direct` jest szerszy i ma płaty położone przy większym \(|P_e|\) niż `delayed`. W `direct` obszar w pobliżu \(P_e=0\) jest silniej opróżniony.

**Wniosek bezpośredni:** modelowo sklasyfikowane zdarzenia `direct` mają większy kolektywny podłużny pęd elektronów.

**Interpretacja oparta na literaturze:** artykuł opisujący model ECBB wiąże to z trzema elektronami uzyskującymi duży pęd krótko po recollision w ścieżce `direct`, podczas gdy w `delayed` duży pęd uzyskują początkowo dwa elektrony. Dane są zgodne z tym opisem, lecz sam wykres końcowych pędów nie odtwarza czasów jonizacji i nie dowodzi tej sekwencji.

**Ograniczenia:** brak przedziałów ufności na wykresach; klasy `direct` i `delayed` są nadane przez algorytm modelu, a nie wyznaczone z samych końcowych pędów; wynik dla 1.7 PW/cm² pochodzi z innej długości fali.

## 3.2. Ruch względny: \(K\)

| Natężenie | \(\langle K\rangle\), `direct` | \(\langle K\rangle\), `delayed` | różnica `direct-delayed` |
|---:|---:|---:|---:|
| 1.0 | 1.182 | 2.121 | -0.939 |
| 1.3 | 1.295 | 2.276 | -0.981 |
| 1.6 | 1.417 | 2.337 | -0.920 |
| 1.7 | 1.398 | 2.383 | -0.985 |

Błędy standardowe średniej, policzone z zapisanych prób, wynoszą około 0.007–0.016 dla `direct` oraz 0.013–0.028 dla `delayed`. Różnice są więc znacznie większe od prostego błędu losowego wynikającego z liczebności próbek. Nie obejmuje to jednak błędu modelu ani niepewności systematycznej klasyfikacji ścieżek.

**Efekt:** chmura `direct` w płaszczyźnie \((\xi_1,\xi_2)\) jest bardziej skupiona wokół początku. Chmura `delayed` jest szersza. Różnica utrzymuje się dla wszystkich czterech zbiorów.

**Wniosek bezpośredni:** w `direct` podpisane pędy podłużne są do siebie bardziej zbliżone niż w `delayed`.

**Ważne ograniczenie:** część różnicy wynika z odmiennego udziału sektorów znakowych. Po ograniczeniu analizy do sektorów `+++` i `---` średnie \(K\) wynoszą odpowiednio 1.16–1.34 dla `direct` i 1.47–1.66 dla `delayed`. Różnica nadal istnieje, ale jest mniejsza niż w danych zagregowanych. Dla sektorów mieszanych wynosi około 2.19–2.22 w `direct` oraz 2.69–3.02 w `delayed`.

Nie należy więc pisać, że większe \(K\) dowodzi wyłącznie bardziej nierównego podziału wartości bezwzględnej pędu. `K` reaguje również na zmianę znaku jednego elektronu.

## 3.3. Podział wartości bezwzględnej pędu: \(N_{\mathrm{eff}}\), \(x_{\max}\) i entropia

| Natężenie | \(\langle N_{\mathrm{eff}}\rangle\), `direct` | `delayed` | \(\langle x_{\max}\rangle\), `direct` | `delayed` | entropia, `direct` | `delayed` |
|---:|---:|---:|---:|---:|---:|---:|
| 1.0 | 2.662 | 2.367 | 0.464 | 0.530 | 0.929 | 0.842 |
| 1.3 | 2.654 | 2.355 | 0.466 | 0.535 | 0.926 | 0.838 |
| 1.6 | 2.633 | 2.367 | 0.471 | 0.536 | 0.920 | 0.843 |
| 1.7 | 2.628 | 2.374 | 0.473 | 0.533 | 0.919 | 0.846 |

**Efekt zagregowany:** `direct` ma większe \(N_{\mathrm{eff}}\), mniejsze \(x_{\max}\) i większą entropię. Wszystkie trzy miary wskazują na bardziej równomierny podział wartości bezwzględnej pędu między trzy elektrony.

**Nie są to trzy niezależne dowody.** Wszystkie trzy obserwable są funkcjami tych samych udziałów \((x_2,x_3,x_4)\) i opisują ten sam aspekt rozkładu.

**Istotna zależność od sektora znakowego:**

- w sektorach zgodnoznakowych \(N_{\mathrm{eff}}\) jest większe w `direct` (około 2.67) niż w `delayed` (około 2.37–2.42);
- w sektorach mieszanych kolejność się odwraca: `direct` ma około 2.12–2.24, a `delayed` około 2.32–2.37.

Zatem zdanie „w `direct` podział jest zawsze bardziej równomierny” byłoby fałszywe. Poprawne jest zdanie: „po uśrednieniu po wszystkich sektorach zdarzenia `direct` mają bardziej równomierny podział wartości bezwzględnych pędów; wynik zależy jednak od składu sektorów znakowych”.

## 3.4. Sektory znakowe

| Natężenie | udział `+++`+`---`, `direct` | udział `+++`+`---`, `delayed` |
|---:|---:|---:|
| 1.0 | 97.36% | 46.54% |
| 1.3 | 95.29% | 48.23% |
| 1.6 | 90.83% | 48.25% |
| 1.7 | 90.50% | 45.72% |

**Efekt:** `direct` jest silnie zdominowany przez zdarzenia, w których wszystkie trzy podłużne pędy mają ten sam znak. W `delayed` sektory zgodnoznakowe i mieszane mają zbliżone łączne udziały, z niewielką przewagą sektorów mieszanych.

Sektory `+++` i `---` są w przybliżeniu symetryczne. Największa różnica występuje dla `direct`, 1.7 PW/cm²: 47.43% wobec 43.07%. Przy pozostałych zbiorach asymetria wynosi zwykle poniżej dwóch punktów procentowych.

**Wniosek bezpośredni:** klasy `direct` i `delayed` różnią się topologią znaków końcowych pędów.

**Ostrożna interpretacja:** dominacja zgodnych znaków w `direct` jest zgodna z bardziej wspólnym przyspieszeniem trzech elektronów wzdłuż pola po bliskich czasach jonizacji. To pozostaje interpretacją modelową. Z końcowych znaków pędu nie można samodzielnie wyznaczyć kolejności zdarzeń w czasie.

## 3.5. Korelacje Pearsona

Notebook podaje średnią z trzech korelacji parowych:

| Natężenie | średnia korelacja par, `direct` | `delayed` |
|---:|---:|---:|
| 1.0 | 0.848 | 0.358 |
| 1.3 | 0.845 | 0.387 |
| 1.6 | 0.833 | 0.401 |
| 1.7 | 0.832 | 0.369 |

Na pierwszy rzut oka wygląda to jak bardzo silniejsza korelacja elektronów w `direct`. Taka interpretacja byłaby jednak zbyt mocna.

Rozkład `direct` składa się głównie z dwóch odległych płatów: `+++` i `---`. Sam fakt, że wszystkie trzy zmienne jednocześnie przechodzą z dodatniego do ujemnego płata, generuje wysoki dodatni Pearson. Po policzeniu korelacji osobno w `+++` i `---`, a następnie po złożeniu płatów po zmianie znaku `---`, średnia korelacja par wynosi tylko:

| Natężenie | `direct`, zgodnoznakowe po wyrównaniu znaku | `delayed`, zgodnoznakowe po wyrównaniu znaku |
|---:|---:|---:|
| 1.0 | -0.015 | -0.167 |
| 1.3 | 0.046 | -0.147 |
| 1.6 | 0.098 | -0.101 |
| 1.7 | 0.103 | -0.090 |

**Wniosek bezpośredni:** wysoki Pearson w pełnym zbiorze `direct` opisuje przede wszystkim globalną dwupłatową strukturę znaków. Nie jest miarą silnego liniowego związku fluktuacji pędów wewnątrz jednego płata.

To nie czyni korelacji „błędną”, ale zmienia jej znaczenie. W pracy należy jasno napisać, czy analizowana jest zależność między płatami, czy struktura wewnątrz płata. Bez tego łatwo sprzedać artefakt grupowania jako „silną korelację dynamiczną”.

W `delayed` korelacja `p2z-p3z` jest systematycznie niższa (0.21–0.27) niż korelacje par obejmujących `p4z` (około 0.38–0.47). Jest to rzeczywista asymetria etykietowanych ról w modelu. Może być zgodna ze szczególną rolą elektronu początkowo tunelującego, ale same współczynniki nie ustalają przyczyny.

## 3.6. Zależność od natężenia

Dla wspólnej długości fali 800 nm, czyli od 1.0 do 1.6 PW/cm²:

- średnie \(K\) rośnie w obu klasach;
- udział sektorów zgodnoznakowych w `direct` maleje z 97.4% do 90.8%;
- \(N_{\mathrm{eff}}\) w `direct` lekko maleje z 2.662 do 2.633;
- średnia korelacja par w `direct` lekko maleje, ale ten wskaźnik jest silnie zależny od struktury znaków;
- w `delayed` zmiany \(N_{\mathrm{eff}}\) są małe i niemonotoniczne.

Te trendy są opisowe. Notebook nie podaje przedziałów ufności, nie dopasowuje modelu zależności od natężenia i ma tylko trzy porównywalne punkty przy 800 nm. Nie ma podstaw do twierdzenia o określonym prawie skalowania. Punkt 1.7 PW/cm² przy 760 nm może służyć jako dodatkowy przypadek, ale nie jako czysty test kontynuacji trendu intensywności.

## 3.7. Całkowity pęd wraz z jonem

Notebook oblicza

\[
P_{\mathrm{total},z}=p_{1z}+P_e.
\]

Średnia tej wielkości leży blisko zera we wszystkich zbiorach, od około -0.022 do 0.028. Jej odchylenie standardowe wynosi jednak około 1.60–1.74. Bliska zeru średnia pokazuje brak silnego globalnego przesunięcia, ale nie jest testem zachowania pędu dla każdego zdarzenia. Bez dokładnego określenia, jaki pęd wypisuje model, w jakim momencie propagacja jest kończona i jaki wkład ma zewnętrzne pole, nie należy przedstawiać tego wyniku jako dowodu ścisłego zachowania całkowitego pędu.

## 3.8. Trzeci moment mieszany \(\kappa_{234}\)

Notebook oblicza nieznormalizowany centralny moment \(\langle\delta p_2\delta p_3\delta p_4\rangle\). Jego znak i wartość zmieniają się nieregularnie. Po podzieleniu przez iloczyn odchyleń standardowych otrzymuje się wartości bezwymiarowe od około -0.052 do 0.034. Brak oszacowania niepewności, a wskaźnik jest wrażliwy na ogony rozkładu. Obecne wyniki nie uzasadniają fizycznego wniosku o trójcząstkowej asymetrii wyższego rzędu.

## 4. Zestawienie wyników w wymaganym schemacie

| Wynik | Użyte dane | Metoda | Obserwowany efekt | Możliwa interpretacja fizyczna | Ograniczenia |
|---|---|---|---|---|---|
| Kierunek kolektywny PCA | 9 składowych pędu, 12 zbiorów | standaryzacja i osobna PCA | PC1 prawie równoległa do \((p_{2z}+p_{3z}+p_{4z})\) | dominujący wspólny tryb podłużny | PCA na macierzy korelacji; osie zależne od zbioru; nie dowodzi mechanizmu |
| Podprzestrzeń względna PCA | te same dane | PC8 i PC9 | prawie podłużna dwuwymiarowa podprzestrzeń różnic | uzasadnia użycie stałej bazy względnej | indywidualne PC8/PC9 obracają się i zamieniają; liczy się podprzestrzeń |
| Szerokość \(P_e\) | `p2z,p3z,p4z` | suma i rozkład 2D z \(K\) | `direct` ma większe \(|P_e|\) | zgodne z trzema elektronami uzyskującymi duży pęd w ścieżce bezpośredniej | końcowe pędy nie odtwarzają czasów jonizacji; klasy pochodzą z modelu |
| Względny rozrzut \(K\) | podłużne pędy | ortogonalna baza i promień względny | `delayed` ma większe \(K\) | większe różnice podpisanych pędów | silna zależność od sektorów znakowych; nie jest miarą tylko wartości bezwzględnych |
| Udział wartości bezwzględnych | \(|p_{iz}|\) | \(N_{\mathrm{eff}},x_{\max}\), entropia | zagregowane `direct` jest bardziej równomierne | zgodne z bardziej wspólnym udziałem trzech elektronów | trzy miary są redundantne; wynik odwraca się dla części sektorów mieszanych |
| Znaki pędów | `sign(p2z,p3z,p4z)` | częstości ośmiu sektorów | `direct`: 90–97% zgodnoznakowych; `delayed`: 46–48% | zgodne ze wspólnym kierunkiem przyspieszenia w `direct` | znak końcowy nie ustala historii czasowej |
| Pearson | podłużne pędy | korelacje parowe | pełne `direct`: około 0.83–0.85 | opis globalnej dwupłatowej struktury | po rozdzieleniu płatów korelacja jest bliska zeru; nie interpretować przyczynowo |
| Trend z natężeniem | 1.0, 1.3, 1.6, 1.7 PW/cm² | porównanie średnich | kilka łagodnych trendów | możliwa zmiana podziału pędu z polem | tylko 3 porównywalne punkty przy 800 nm; 1.7 ma 760 nm; brak niepewności systematycznych |

## 5. Niespójności i błędy w notebookach

### 5.1. Starsze notebooki simpleksowe

1. **Aktywny plik różni się między notebookiem głównym i checkpointem.** Główne notebooki dla 1.0, 1.3 i 1.6 PW/cm² mają `file=f1` (`all`), a notebook 1.7 ma `file=f3` (`direct`). Checkpointy zawierają inne wybory: dla 1.0 `direct`, dla 1.3 i 1.6 `delayed`, dla 1.7 `all`. Zapisane wykresy nie tworzą jednego spójnego uruchomienia.

2. **Checkpoint 1.0 ma niezgodny separator.** Używa `sep=' '`, podczas gdy aktualne pliki są rozdzielone przecinkami. Nie powinien przejść od czystego kernela na obecnych danych.

3. **Błąd etykiet osi.** Kod wczytuje `p2z,p3z,p4z`, ale na wykresach podpisuje je jako `p1z,p2z,p3z`. Rdzeń nie jest na tych wykresach, więc podpisy są przesunięte o jeden numer.

4. **Błąd permutacji dla sektora `+--`.** Wywołanie `add_with_two_permutations(side,r,1)` wskazuje drugi elektron jako ten o przeciwnym znaku. W sektorze `+--` przeciwny znak ma pierwsza z trzech wczytanych współrzędnych, więc powinno być `different=0`. Błąd zniekształca zagregowany trójkąt sektorów mieszanych.

5. **Błędne nazwy plików wyjściowych.** Komentarz twierdzi, że `file[-9:-4]` zwraca natężenie, lecz dla nazw `momenta_*_events.txt` zwraca `vents`. Powstają pliki typu `oktants vents.png`, a kolejne uruchomienia dla `all`, `direct` i `delayed` mogą je nadpisywać.

6. **Brak ochrony przed \(A=0\).** Dzielenie przez `t=|p2z|+|p3z|+|p4z|` nie jest zabezpieczone. W aktualnych danych nie znaleziono takich wierszy, ale kod nie jest ogólnie bezpieczny.

7. **Niezależne skale kolorów.** Każdy panel ma własną skalę liczby zdarzeń. Kolorów między sektorami i klasami nie można porównywać ilościowo.

Wniosek: stare notebooki są użyteczne do zrozumienia geometrii simpleksu, ale w obecnym stanie nie powinny być źródłem liczb ani finalnych rysunków do pracy.

### 5.2. `05_PCA_full.ipynb`

Notebook ma spójne, kolejne numery wykonań i wyniki odpowiadają zapisanym CSV. Główne ograniczenia są metodologiczne:

- osobne dopasowanie PCA utrudnia porównywanie nazw osi między zbiorami;
- znak składowej PCA jest arbitralny;
- PC8 i PC9 mogą obracać się w prawie zdegenerowanej podprzestrzeni;
- standaryzacja zmienia fizyczną metrykę przestrzeni pędów;
- brak analizy stabilności loadings, np. bootstrapu;
- wykres trendu PC1 nie ma przedziałów niepewności i łączy punkt 760 nm z punktami 800 nm.

### 5.3. `07_analiza_3D_clean.ipynb`

Wyniki tabel są wewnętrznie spójne i najważniejsze wartości zostały niezależnie odtworzone z surowych plików. Są jednak problemy:

1. Komórka sprawdzająca ortonormalność ma zapisany output, ale `execution_count=null`. Notebook nie dokumentuje więc jednoznacznie pełnego `Restart Kernel -> Run All`, mimo że dalsze wyniki są spójne.
2. Brakuje przedziałów ufności, bootstrapu lub innej oceny niepewności.
3. Pearson jest liczony na pełnej mieszaninie płatów i sektorów; jego interpretacja bez stratyfikacji jest myląca.
4. `K`, \(N_{\mathrm{eff}}\) i sektory są analizowane osobno, mimo że ich różnice między kanałami są częściowo współzależne.
5. Histogramy 2D mają wspólne zakresy osi w obrębie natężenia, ale niezależną normalizację kolorów dla każdego panelu. Pozwala to porównywać kształt, lecz nie bezpośrednio gęstość.
6. Wykresy ILR są generowane mimo instrukcji, by nie używać tej obserwabli. Dodatkowo zera są zastępowane przez epsilon maszynowy, co może tworzyć ekstremalne wartości logarytmów.
7. `kappa_234` jest nieznormalizowany i nie ma oszacowania niepewności; obecnie nie nadaje się do dyskusji fizycznej.
8. Średnia `P_total_z` bliska zeru nie stanowi pełnego testu zachowania pędu; potrzebne byłoby wyjaśnienie oczekiwanej wielkości dla pojedynczych trajektorii.

## 6. Co można uczciwie napisać w rozdziale „Wyniki”

1. Transformacja do \((Q,\xi_1,\xi_2)\) jest ortogonalna i numerycznie odwracalna. Rozdziela wspólny podłużny pęd od dwóch niezależnych współrzędnych względnych, ale nie redukuje wymiaru.
2. We wszystkich badanych zbiorach `direct` ma większą szerokość i większe typowe \(|P_e|\) niż `delayed`.
3. `direct` ma mniejsze \(K\), czyli mniejszy rozrzut podpisanych pędów wokół ich średniej.
4. `direct` jest silnie zdominowany przez sektory `+++` i `---`, podczas gdy w `delayed` około połowy zdarzeń leży w sektorach mieszanych.
5. Po uśrednieniu po sektorach `direct` ma bardziej równomierny podział wartości bezwzględnego pędu. Wniosek nie jest jednak uniwersalny po rozdzieleniu sektorów.
6. PCA jest zgodna z tym obrazem: `direct` ma większy udział wariancji kierunku kolektywnego i mniejszy udział dwóch kierunków względnych.
7. Surowa korelacja Pearsona jest wysoka w `direct`, ale głównie z powodu dwóch odległych płatów zgodnoznakowych. Nie może być przedstawiona jako bezpośrednia miara siły oddziaływania lub synchronizacji wewnątrz jednego płata.

## 7. Co można napisać w „Dyskusji” tylko jako hipotezę zgodną z literaturą

Artykuł źródłowy modelu ECBB definiuje `direct (e,3e)` jako ścieżkę, w której wszystkie trzy elektrony jonizują krótko po recollision, a `delayed (e,2e)` jako ścieżkę, w której dwa elektrony jonizują szybko, natomiast trzeci z opóźnieniem. Autorzy wiążą większy zakres sumy pędów w `direct` z trzema elektronami uzyskującymi duży pęd, a mniejszy zakres w `delayed` z dwoma takimi elektronami.

Na tej podstawie można napisać, że:

- większe \(|P_e|\), dominacja sektorów zgodnoznakowych i mniejsze \(K\) w `direct` są **zgodne** z bliskimi czasami uwolnienia trzech elektronów i ich podobnym przyspieszeniem przez pole;
- większe \(K\), większy udział sektorów mieszanych i mniejsze zagregowane \(N_{\mathrm{eff}}\) w `delayed` są **zgodne** z mniej jednoczesnym uwolnieniem i odmienną historią przyspieszenia jednego elektronu;
- asymetria korelacji par w `delayed` może być związana z rolą elektronu początkowo tunelującego, ale sama analiza końcowych pędów nie rozstrzyga tego mechanizmu.

Nie można na podstawie tych notebooków stwierdzić, że wymienione obserwable dowodzą recollision, transferu określonej ilości energii lub konkretnej kolejności jonizacji. Te informacje pochodzą z definicji ścieżek i analizy czasowej modelu w artykule, a nie z samego zestawu końcowych pędów.

## 8. Zalecenia przed pisaniem finalnych rozdziałów

1. Oprzeć liczby na `05_PCA_full.ipynb`, `07_analiza_3D_clean.ipynb` i eksportowanych CSV. Starsze notebooki simpleksowe potraktować jako prototyp i nie cytować ich wykresów przed naprawą.
2. Uruchomić oba czyste notebooki od pustego kernela i zapisać pełny stan wykonania.
3. Dodać bootstrapowe 95-procentowe przedziały ufności dla średnich, median, udziałów sektorów i różnic `direct-delayed`.
4. Dla \(P_e\) raportować szerokość, \(|P_e|\) lub położenie płatów, a nie samą średnią bliską zeru.
5. Rozdzielić analizę na sektory zgodnoznakowe i mieszane. Bez tej stratyfikacji \(K\), \(N_{\mathrm{eff}}\) i Pearson mieszają dwa różne efekty.
6. Zastąpić surowy Pearson co najmniej dwiema analizami: korelacją pełnego rozkładu oraz korelacją wewnątrz płatów `+++` i `---` po wyrównaniu znaku.
7. Pokazywać 1.7 PW/cm² jako osobny przypadek 760 nm. Trend natężenia omawiać przede wszystkim dla 1.0–1.6 PW/cm² przy 800 nm.
8. Naprawić etykiety `p2z,p3z,p4z`, błąd sektora `+--`, nazwy plików i wspólne skale kolorów w wykresach simpleksowych.
9. Nie przedstawiać \(N_{\mathrm{eff}}\), \(x_{\max}\) i entropii jako trzech niezależnych potwierdzeń. Wybrać jedną główną miarę, a pozostałe użyć jako kontrolę.
10. Usunąć ILR z finalnego toku narracji, chyba że zostanie osobno uzasadnione pytaniem badawczym i poprawną obsługą zer.

## 9. Konkluzja

Najmocniejszy wynik analizy nie polega na jednym współczynniku, lecz na spójnym obrazie geometrii końcowych pędów. W zdarzeniach `direct` suma podłużnych pędów ma większy moduł, trzy pędy znacznie częściej mają wspólny znak, a rozrzut w podprzestrzeni względnej jest mniejszy. W `delayed` częstsze są sektory mieszane i większe różnice podpisanych pędów. PCA odtwarza ten sam podział jako silniejszy tryb kolektywny i słabszą zmienność względną w `direct`.

Najważniejsza korekta interpretacyjna brzmi: część pozornie silnych „korelacji elektron-elektron” wynika z mieszania dwóch płatów `+++` i `---`. Po rozdzieleniu płatów korelacje liniowe są małe. Dlatego bezpieczna dyskusja powinna opierać się przede wszystkim na geometrii rozkładów, udziałach sektorów, \(P_e\), \(K\) i warunkowej analizie podziału pędu, a nie na jednym globalnym współczynniku Pearsona.

## Źródło interpretacji modelowej

A. Emmanouilidou, M. B. Peters, G. P. Katsoulis, „Singularity in electron-core potential as a gateway to accurate multi-electron ionization spectra in strongly driven atoms”, *Physical Review A* 107, L041101 (2023), wersja otwarta: https://arxiv.org/abs/2302.03777.
