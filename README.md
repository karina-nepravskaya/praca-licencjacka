# Praca licencjacka — instrukcja dla agenta

> **Ten plik jest kontraktem roboczym dla każdego agenta AI pracującego w tym repozytorium.**
> Przed zmianą tekstu, kodu, wykresów, bibliografii albo struktury pracy należy przeczytać ten README w całości.
>
> Celem jest wygenerowanie pracy licencjackiej spójnej z analizą w tym repo, poprawnej fizycznie, reprodukowalnej**.

---

## 1. Kontekst pracy

Praca powstaje na:

- **Uniwersytecie Jagiellońskim**
- **Wydziale Fizyki, Astronomii i Informatyki Stosowanej (WFAIS UJ)**
- kierunku **Fizyka dla firm**, studia I stopnia

Temat roboczy pracy nie jest jeszcze ustalony ostatecznie, póki co może być:

> **Analiza korelacji pędów wielu elektronów w potrójnej jonizacji neonu w silnym polu laserowym**

możesz bardziej dopasować ją na koniec pracy nad tekstem samej pracy, możesz ją skrócić lub, ALE rób to NA KONIEC.

Głównym przedmiotem analizy są dane z foldera ECBB_model niniejszego repozytorium. 
Tam znajdują się użyteczne pliki: 
- README.md który opisuje dane na których wykonuje się analizę. Musi być przeanalizowany w tym momeńcie i przed każdym podejściem do pracy z tym repozytorium.
- PhysRevA.107.L041101.pdf użyteczna praca żeby 

Do informacji z tamtego ECBB_model/README.md dodatkowa uwaga od promotora: **Nie wolno przedstawiać tych etykiet elektronów 'tunelujący', 'związany' jako fundamentalnie fizycznych.** Są one użytecznym oznaczeniem ich roli w dynamice procesu jonizacji. Elektrony są kwantowo nierozróżnialne, dlatego interpretacja wyników musi wyraźnie odróżniać etykietowanie numeryczne od własności fizycznej układu.

---

## 2. Główny problem badawczy

Dla podwójnej i potrójnej jonizacji użyteczna jest reprezentacja simpleksowa opisywana w pliku 'Praca_licencjacka_296213 (watermarked)'.pdf. Zapoznać sięz tym również 
Pozwala przedstawić względny podział pędu pomiędzy trzema elektronami.

Problem pojawia się przy próbie uogólnienia takiej reprezentacji na większą liczbę elektronów:

- dla trzech składowych otrzymujemy reprezentację wygodną do pokazania na płaszczyźnie;
- dla czterech składowych naturalnym obiektem staje się bryła trójwymiarowa;
- dla jeszcze większej liczby elektronów wymiar simpleksu rośnie dalej;
- kolorowanie lub rozcinanie bryły 3D przestaje być przejrzystym narzędziem analizy.

Celem obecnej metody jest zbudowanie alternatywnego **bardziej skalowalnego opisu korelacji pędów**, zachowującego możliwie jasną interpretację fizyczną.

---

## 3. Metoda analizy

Kluczowe pliki .ipynb są źródłem prawdy dla analizy. Przed zmianą rozdziału analitycznego agent powinien:

1. otworzyć oba notebooki;
2. sprawdzić aktywne zbiory danych;
3. sprawdzić definicje wszystkich używanych wielkości;
4. sprawdzić, czy notebook wykonuje się od czystego kernela;
5. dopiero potem aktualizować tekst i liczby w pracy.

**Nie ufać zmiennym pozostałym w pamięci Jupytera.** Wynik jest wiarygodny dopiero wtedy, gdy notebook przechodzi `Restart Kernel -> Run All` bez błędu.

Jeżeli notebook ma błąd, brakującą zmienną albo komórkę zależną od starego stanu kernela, agent ma to zaznaczyć i naprawić przed wykorzystaniem wyniku w pracy.

--- 

Dalej w tej części zamieszczony jest przybliżony opis metody, jakby można było coś logicznie dodać czy wyrafinować ją JEDYNIE w oparciu o literaturę naukową i dodać bardziej szczegółowe opisy i dodać referencję, to zrob to agent MUSI to zrobić!

PCA jako punkt wyjścia: Notebook `05_PCA_full.ipynb` analizuje dziewięć składowych pędów trzech elektronów:

\[
(p_{2x},p_{2y},p_{2z},
 p_{3x},p_{3y},p_{3z},
 p_{4x},p_{4y},p_{4z}).
\]

W analizowanym metodą PCA zbiorze szczególnie interesujące są wynikowe kierunki głównych składowych, których współczynniki są praktycznie ograniczone do osi \(z\). W notatkach notebooka są to PC1, PC8 i PC9.

Przeanalizuj ten cały notebook. Z kolei PCA nie definiuje wprost osi do których dalej przejdziemy z naszymi danymi. Agent **nie może pisać**, że końcowe współrzędne są po prostu „PC1, PC8 i PC9”. PCA było motywacją, bo metoda ta pokazała, że w danych wyróżniają się jeden tryb kolektywny wzdłuż \(z\) i dwa niezależne kierunki opisujące względne różnice pędów. Do dalszej analizy wybierana jest jednak **stała, ortonormalna baza**, niezależna od konkretnego zbioru danych:

\[
\mathbf e_0=
\frac{1}{\sqrt 3}
\begin{pmatrix}
1\\1\\1
\end{pmatrix},
\qquad
\mathbf e_1=
\frac{1}{\sqrt 2}
\begin{pmatrix}
1\\-1\\0
\end{pmatrix},
\qquad
\mathbf e_2=
\frac{1}{\sqrt 6}
\begin{pmatrix}
1\\1\\-2
\end{pmatrix}.
\]

Współrzędne tej nowej bazy:

\[
Q=\frac{p_2+p_3+p_4}{\sqrt 3},
\]

\[
\xi_1=\frac{p_2-p_3}{\sqrt 2},
\]

\[
\xi_2=\frac{p_2+p_3-2p_4}{\sqrt 6}.
\]

Interpretacja:

- \(Q\) — **kolektywny podłużny tryb pędowy**, proporcjonalny do całkowitego podłużnego pędu elektronów;
- \(\xi_1\) — względna różnica pędu pomiędzy elektronami 2 i 3;
- \(\xi_2\) — względna różnica pomiędzy parą 2–3 a elektronem 4;
- para \((\xi_1,\xi_2)\) opisuje dwuwymiarową przestrzeń względnego podziału pędu.

Dodatkowo:

\[
K=\sqrt{\xi_1^2+\xi_2^2}
\]

jest miarą wielkości względnej nierównowagi pędów.

Nie zachodzi redukcja wymiaru przestrzeni w którym operujemy, ponieważ transformacja

\[
(p_2,p_3,p_4)\longrightarrow(Q,\xi_1,\xi_2)
\]

jest **ortogonalną zmianą bazy**. Poszukaj jeszcze na ten temat w literatyrze matematycznej (naukowej, na poziomie wyższym) różne rzeczy oraz dodaj, jeżeli mogą wnieść coś wartościowego w ten postęp rozumowania.  

Musi zachodzić:

\[
p_2^2+p_3^2+p_4^2
=
Q^2+\xi_1^2+\xi_2^2.
\]

Odwrotna transformacja:

\[
p_2=
\frac{Q}{\sqrt 3}
+\frac{\xi_1}{\sqrt 2}
+\frac{\xi_2}{\sqrt 6},
\]

\[
p_3=
\frac{Q}{\sqrt 3}
-\frac{\xi_1}{\sqrt 2}
+\frac{\xi_2}{\sqrt 6},
\]

\[
p_4=
\frac{Q}{\sqrt 3}
-\frac{2\xi_2}{\sqrt 6}.
\]

Jeżeli tekst nazywa tę operację „redukcją wymiaru”, agent ma to poprawić albo bardzo precyzyjnie wyjaśnić, co faktycznie jest redukowane na etapie wizualizacji.

---

## 4. Główne obserwable używane w analizie

Podstawowym źródłem implementacji jest `07_analiza_3D_clean.ipynb`. Przeanalizyj przebieg analizy w nim. Tam jest druga część analizy gdzie bazując się na kierunkach z PCA obliczamy różne rzeczy. Tu musisz zrozumieć sens każdej w nich, mieć dostęp do wyniku uruchomienia tego pliku, czyli wszystkich wykresów i powinienneś móc powiedzieć co na nich widać i jakie są wnioski dotycząc przeprowadzonej analizy.

### 4.1. Całkowity podłużny pęd elektronów

\[
P_e=p_2+p_3+p_4=\sqrt 3\,Q.
\]

Nie mieszać symboli \(P_e\) i \(Q\). Są proporcjonalne, ale nie są numerycznie identyczne.

### 4.2. Względna nierównowaga

\[
K=\sqrt{\xi_1^2+\xi_2^2}.
\]

Wykres \(P_e\) względem \(K\) zestawia ruch kolektywny układu z wielkością względnego rozrzutu pędów.

### 4.3. Udziały bezwzględnego pędu

Definicja:

\[
A=|p_2|+|p_3|+|p_4|,
\qquad
x_i=\frac{|p_i|}{A}.
\]

Stąd:

\[
x_2+x_3+x_4=1.
\]

Znaki pędów są przechowywane **osobno** w postaci sektorów znakowych.

### 4.4. Efektywna liczba elektronów uczestniczących w podziale pędu

\[
N_{\mathrm{eff}}=
\frac{1}{x_2^2+x_3^2+x_4^2}.
\]

Dla trzech elektronów:

\[
1\le N_{\mathrm{eff}}\le 3.
\]

Interpretacja:

- \(N_{\mathrm{eff}}\approx 1\): jeden elektron dominuje w bezwzględnym podziale pędu;
- \(N_{\mathrm{eff}}\approx 3\): pęd bezwzględny jest rozłożony względnie równomiernie pomiędzy trzy elektrony.

### 4.5. Największy udział pojedynczego elektronu

\[
x_{\max}=\max(x_2,x_3,x_4).
\]

Dla trzech elektronów:

\[
\frac13\le x_{\max}\le 1.
\]

### 4.6. Sektory znakowe

Dla każdego zdarzenia zapisujemy znaki trójki

\[
(p_2,p_3,p_4),
\]

np.

- `+++`,
- `++-`,
- `+-+`,
- `-++`,
- `+--`,
- `-+-`,
- `--+`,
- `---`.

Sektory opisują topologię emisji względem osi polaryzacji: czy elektrony mają pędy zgodne, czy część z nich porusza się w przeciwnym kierunku.

### 4.7. Korelacje par elektronów

Analizowane są m.in.:

\[
\mathrm{corr}(p_2,p_3),\qquad
\mathrm{corr}(p_2,p_4),\qquad
\mathrm{corr}(p_3,p_4),
\]

oraz różnice:

\[
d_{23}=p_2-p_3,\qquad
d_{24}=p_2-p_4,\qquad
d_{34}=p_3-p_4.
\]

Współczynnik Pearsona nie może być przedstawiany jako pełny opis zależności wieloelektronowej. Jest tylko jednym z obserwabli pomocniczych.

Ignoruj ILR obserwable, NIE POWINNY pojawiać się w analizie tekstowej.

Agent ma porównywać `direct` i `delayed` rodzaje zdarzeń **tylko dla tej samej intensywności pola**. Nie wolno porównywać dwóch różnych intensywności i interpretować różnicy jako efektu mechanizmu direct/delayed.

Dla każdej prezentowanej różnicy należy podać przynajmniej:

- intensywność,
- typ kanału,
- liczbę zdarzeń,
- definicję obserwabli.

---

## 5. Zasady interpretacji fizycznej

### Agent MA:

- odróżniać **obserwację numeryczną** od **interpretacji fizycznej**;
- pisać „rozkład wskazuje / sugeruje / jest zgodny z...” tam, gdzie dane nie dowodzą jednoznacznie mechanizmu;
- zawsze definiować obserwablę przed jej interpretacją;
- sprawdzać, czy symetrie oczekiwane z nierozróżnialności elektronów są zachowane lub świadomie złamane przez sposób etykietowania;
- rozdzielać ruch kolektywny (\(Q\), \(P_e\)) od ruchu względnego (\(\xi_1,\xi_2,K\));
- odróżniać PCA zależne od kowariancji konkretnego zbioru danych od stałej bazy Jacobiego–Helmerta;
- wykorzystywać zasadę zachowania pędu i pęd jonu jako test spójności, jeżeli dane na to pozwalają.

### Agent NIE MA:

- wymyślać mechanizmu fizycznego tylko dlatego, że „pasuje do wykresu”;
- nazywać korelacji przyczynowością;
- pisać, że PCA „udowodniło” mechanizm recollision;
- traktować numerów elektronów jako obserwowalnej kwantowej;
- twierdzić, że transformacja ortogonalna redukuje wymiar;
- wymyślać wartości liczbowe, liczby zdarzeń albo trendów, których nie ma w aktualnych wynikach;
- kopiować stare liczby z tekstu, jeśli notebook po zmianie danych daje inne wyniki.

---

## 6. Format pracy licencjackiej

Jako wynik pracy (jeżeli nie powiedziano zrobić coś innego) musisz wygenerować lub edytować 'main.tex' plik z tekstem pracy licencjackiej, do kompilowania w LaTeX (overleaf). Również trzymaj spis referencyjny literatury 'bibliography.bib' spójnie z 'main.tex'.

## 7. Zasady pisania pracy
### 7.1 Ogólne zasady
Napisz pracę licencjacką w języku polskim, opartą na logicznym ciągu:

kontekst fizyczny → problem badawczy → opis danych → metoda analizy → sprawdzenie metody → wyniki → interpretacja fizyczna → ograniczenia i wnioski.

Każdy rozdział ma przygotowywać czytelnika do następnego. Wprowadzaj pojęcia dopiero wtedy, gdy są potrzebne. Nie wymieniaj wcześniej obserwabli, transformacji ani parametrów, które zostaną zdefiniowane dopiero kilka rozdziałów później. Czytelnik ma zawsze rozumieć, skąd wynika kolejny krok i po co jest wykonywany.

Teorię ogranicz do informacji rzeczywiście potrzebnych w analizie. Najpierw przedstaw prostszy przypadek lub intuicję geometryczną, a następnie właściwą metodę. Dla każdej metody wyjaśnij:

jaki problem rozwiązuje;
jakie dane wykorzystuje;
na czym polega matematycznie;
jak interpretować jej wynik;
jakie informacje zachowuje, a jakie traci;
jak sprawdzono poprawność implementacji.

Wyniki organizuj według pytań fizycznych, a nie kolejności notebooków lub wykonanych wykresów. Każdy fragment analizy powinien mieć schemat:

pytanie → zastosowana metoda → rysunek lub wynik liczbowy → obserwacja → interpretacja → krótki wniosek.

Wyraźnie oddzielaj to, co bezpośrednio wynika z danych, od interpretacji fizycznej. Nie przedstawiaj przypuszczeń jako udowodnionych wniosków. Nie powtarzaj tej samej informacji w teorii, metodologii, podpisie rysunku i analizie.

### 7.2 Styl językowy

Naśladuj sposób pisania zastosowany w sprawozdaniu Dlugosc_fali_Nepravskaya_Karina.pdf: używaj prostych, konkretnych i stosunkowo krótkich zdań. Pisz rzeczowo, naturalnie i technicznie, bez ozdobników, patosu oraz sztucznego komplikowania wypowiedzi. Preferuj konstrukcje takie jak:

„Celem analizy jest…”
„Dla każdego zestawu danych wyznaczono…”
„Z otrzymanych punktów sporządzono wykres…”
„Na rysunku przedstawiono…”
„Z porównania wynika, że…”
„Można to wyjaśnić przez…”
„Wartość ta jest zgodna z…”

Nie używaj typowego tekstu generowanego przez AI, w szczególności pustych sformułowań typu „warto podkreślić niezwykle istotną rolę”, „w kontekście niniejszych rozważań”, „stanowi fundamentalny aspekt” albo „otwiera nowe perspektywy”, jeśli nie przekazują konkretnej informacji.

Każdy zastosowany termin naukowy musi być rzeczywiście istniejącym i powszechnie używanym terminem w polskiej literaturze naukowej. Nie twórz polskich nazw przez dosłowne tłumaczenie angielskich terminów ani przez dopisywanie polskich końcówek do anglicyzmów. Jeśli poprawny polski odpowiednik nie jest pewny, sprawdź go w wiarygodnych polskojęzycznych publikacjach naukowych. Gdy nie istnieje utrwalony odpowiednik, podaj termin angielski i krótko wyjaśnij jego znaczenie zamiast wymyślać nową nazwę.

Zachowaj poprawność naukową, ale nie kopiuj błędów językowych lub redakcyjnych z tekstów referencyjnych. Nie dopisuj informacji, których nie potwierdzają dane, kod albo literatura. Każdy wzór, rysunek i tabela muszą zostać wprowadzone w tekście oraz wykorzystane w dalszym rozumowaniu.

### 7.3 Ogólny model spisu treści

1. Wstęp
   1.1. Główna metoda lub podejście
   1.2. Metoda porównawcza albo sposób weryfikacji

2. Przeprowadzenie analizy
   2.1. Pierwszy pełny przypadek lub etap
   2.2. Drugi pełny przypadek lub etap
   2.3. Kolejne przypadki tylko wtedy, gdy mają własne wyniki

3. Analiza i dyskusja wyników
   3.1. Najważniejsze zależności
   3.2. Porównanie przypadków lub metod
   3.3. Ograniczenia analizy

4. Wnioski i podsumowanie

A. Dodatek techniczny
B. Dodatkowe wyprowadzenia lub kod
Bibliografia

Nie trzeba na siłę zachowywać wszystkich podpunktów. Jeśli „ograniczenia” zajmują jeden akapit, należy je włączyć do dyskusji. Jeśli dwie metody wymagają pełnego wyprowadzenia, dostają osobne podrozdziały. 

## 16. Git / sposób pracy agenta

Przed zmianą:

1. sprawdź stan repozytorium;
2. przeczytaj ten README;
3. przeczytaj aktualny `main.tex` i pliki rozdziałów;
4. przeczytaj odpowiednie notebooki;
5. sprawdź `.bib`;
6. znajdź istniejące definicje symboli, żeby ich nie dublować.

Podczas zmiany:

- nie usuwaj ręcznych zmian autora bez powodu;
- rób możliwie małe i logiczne diffy;
- nie przebudowuj całej struktury repozytorium przy drobnej korekcie;
- nie zmieniaj nazw rysunków i labeli bez aktualizacji wszystkich odwołań;
- nie zmieniaj jednocześnie fizyki, stylu i infrastruktury LaTeX, jeśli nie jest to konieczne.

Po zmianie:

1. skompiluj dokument przez pdfLaTeX;
2. sprawdź log kompilacji;
3. sprawdź referencje i cytowania;
4. jeżeli zmieniono analizę — uruchom notebook od czystego kernela;
5. sprawdź, czy liczby w tekście zgadzają się z aktualnym outputem;
6. opisz krótko, **co zmieniono i dlaczego**.

Nie zgadywać. Sprawdzać repozytorium, notebooki, dane i źródła. Jeżeli czegoś nie da się uzasadnić na podstawie aktualnych wyników albo literatury, agent ma to powiedzieć zamiast produkować pewnie brzmiącą bzdurę.