# Praca licencjacka — instrukcja dla agenta

> **Ten plik jest kontraktem roboczym dla każdego agenta AI pracującego w tym repozytorium.**
> Przed zmianą tekstu, kodu, wykresów, bibliografii albo struktury pracy należy przeczytać ten README w całości.
>
> Celem nie jest „wygenerowanie długiego tekstu”, tylko doprowadzenie repozytorium do stanu **spójnej, poprawnej fizycznie, reprodukowalnej i dobrze napisanej pracy licencjackiej**.

---

## 1. Kontekst pracy

Praca powstaje na:

- **Uniwersytecie Jagiellońskim**
- **Wydziale Fizyki, Astronomii i Informatyki Stosowanej (WFAIS UJ)**
- kierunku **Fizyka dla firm**, studia I stopnia
- w obszarze fizyki atomowej / oddziaływania atomów z silnymi polami laserowymi.

Temat roboczy pracy:

> **Analiza korelacji pędów wielu elektronów w potrójnej jonizacji neonu w silnym polu laserowym**

Głównym przedmiotem analizy są dane z klasycznych obliczeń trajektorii dla potrójnej jonizacji neonu. Dla każdego zdarzenia dostępne są końcowe składowe pędu:

\[
(p_{2x},p_{2y},p_{2z},
 p_{3x},p_{3y},p_{3z},
 p_{4x},p_{4y},p_{4z}).
\]

W pełnym pliku danych występuje również pęd jonu/rdzenia oznaczanego jako `p1`.

Oś polaryzacji liniowo spolaryzowanego pola laserowego to **oś \(z\)**. Dlatego podstawowa analiza korelacji dotyczy składowych podłużnych

\[
p_2 \equiv p_{2z},\qquad
p_3 \equiv p_{3z},\qquad
p_4 \equiv p_{4z}.
\]

W modelu klasycznym:

- elektron 4 jest początkowo elektronem tunelującym,
- elektrony 2 i 3 są początkowo związane.

**Nie wolno jednak przedstawiać tych etykiet jako fundamentalnie fizycznych.** Są one użytecznym oznaczeniem trajektorii w modelu klasycznym. Elektrony są kwantowo nierozróżnialne, dlatego interpretacja wyników musi wyraźnie odróżniać etykietowanie numeryczne od własności fizycznej układu.

---

## 2. Główny problem badawczy

Dla podwójnej i potrójnej jonizacji użyteczna jest reprezentacja simpleksowa / oktaedryczna, ponieważ pozwala przedstawić względny podział pędu pomiędzy trzema elektronami.

Problem pojawia się przy próbie uogólnienia takiej reprezentacji na większą liczbę elektronów:

- dla trzech składowych otrzymujemy reprezentację wygodną do pokazania na płaszczyźnie;
- dla czterech składowych naturalnym obiektem staje się bryła trójwymiarowa;
- dla jeszcze większej liczby elektronów wymiar simpleksu rośnie dalej;
- kolorowanie lub rozcinanie bryły 3D przestaje być przejrzystym narzędziem analizy.

Celem obecnej metody jest zbudowanie **bardziej skalowalnego opisu korelacji pędów**, zachowującego możliwie jasną interpretację fizyczną.

---

## 3. Skąd bierze się użyta baza współrzędnych

### 3.1. PCA jako punkt wyjścia

Notebook `05_PCA.ipynb` analizuje dziewięć składowych pędów trzech elektronów:

\[
(p_{2x},p_{2y},p_{2z},
 p_{3x},p_{3y},p_{3z},
 p_{4x},p_{4y},p_{4z}).
\]

W analizowanym zbiorze szczególnie interesujące są komponenty PCA, których loadings są praktycznie ograniczone do osi \(z\). W notatkach notebooka są to PC1, PC8 i PC9.

Dla przykładowej analizy w `05_PCA.ipynb`:

- PC1 jest zbliżony do kierunku
  \[
  p_2+p_3+p_4,
  \]
- PC8 do kierunku typu
  \[
  p_3-\frac{p_2+p_4}{2},
  \]
- PC9 do kierunku typu
  \[
  p_2-p_4.
  \]

### 3.2. Bardzo ważne: PCA nie jest końcową definicją osi

Agent **nie może pisać**, że końcowe współrzędne są po prostu „PC1, PC8 i PC9”.

PCA było **motywacją**: pokazało, że w danych wyróżniają się jeden tryb kolektywny wzdłuż \(z\) i dwa niezależne kierunki opisujące względne różnice pędów.

Do dalszej analizy wybierana jest jednak **stała, ortonormalna baza Jacobiego–Helmerta**, niezależna od konkretnego zbioru danych:

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

Nowe współrzędne:

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

### 3.3. To nie jest redukcja wymiaru

Transformacja

\[
(p_2,p_3,p_4)\longrightarrow(Q,\xi_1,\xi_2)
\]

jest **ortogonalną zmianą bazy**, a nie redukcją informacji.

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

Podstawowym źródłem implementacji jest `07_analiza_3D.ipynb`.

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

### 4.8. Współrzędne ILR

Notebook zawiera także współrzędne log-ratio dla dodatnich udziałów \(x_i\):

\[
y_1=\frac{1}{\sqrt 2}\ln\frac{x_2}{x_3},
\]

\[
y_2=\frac{1}{\sqrt 6}\ln\frac{x_2x_3}{x_4^2}.
\]

Jeżeli ILR trafia do pracy, trzeba wyjaśnić:

1. po co jest używany,
2. że działa na udziałach dodatnich,
3. jak traktowane są zera,
4. że clipping ma charakter **regularyzacji numerycznej**, a nie nowej definicji fizycznej.

---

## 5. Direct i delayed

W danych występują kanały:

- `direct`,
- `delayed`,
- czasem `all`.

Agent ma porównywać `direct` i `delayed` **tylko dla tej samej intensywności pola**.

Nie wolno porównywać dwóch różnych intensywności i interpretować różnicy jako efektu mechanizmu direct/delayed.

Dla każdej prezentowanej różnicy należy podać przynajmniej:

- intensywność,
- typ kanału,
- liczbę zdarzeń,
- definicję obserwabli.

W `07_analiza_3D.ipynb` aktywnie skonfigurowane są obecnie pliki dla **1.7 PW/cm²**, natomiast wcześniejsze wartości intensywności mogą być zakomentowane. Agent ma sprawdzać aktualną wersję notebooka zamiast zakładać, że wszystkie zbiory zostały rzeczywiście uruchomione.

---

## 6. Zasady interpretacji fizycznej

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

## 7. Notebooki są źródłem prawdy dla analizy

Kluczowe pliki:

- `05_PCA.ipynb` — motywacja PCA i kierunki wyróżnione w danych;
- `07_analiza_3D.ipynb` — właściwa analiza w nowych współrzędnych i definicje obserwabli.

Przed zmianą rozdziału analitycznego agent powinien:

1. otworzyć oba notebooki;
2. sprawdzić aktywne zbiory danych;
3. sprawdzić definicje wszystkich używanych wielkości;
4. sprawdzić, czy notebook wykonuje się od czystego kernela;
5. dopiero potem aktualizować tekst i liczby w pracy.

**Nie ufać zmiennym pozostałym w pamięci Jupytera.** Wynik jest wiarygodny dopiero wtedy, gdy notebook przechodzi `Restart Kernel -> Run All` bez błędu.

Jeżeli notebook ma błąd, brakującą zmienną albo komórkę zależną od starego stanu kernela, agent ma to zaznaczyć i naprawić przed wykorzystaniem wyniku w pracy.

---

## 8. Reprodukowalność

Każda liczba lub wykres wykorzystany w pracy powinien dać się odtworzyć.

Minimalny standard:

- ścieżka od surowych danych do wykresu jest znana;
- transformacje są zapisane jawnie;
- jednostki są podane;
- intensywność i kanał są zapisane w podpisie lub bezpośrednio w tekście;
- kod nie zależy od ręcznie ustawionych niewidocznych zmiennych;
- wyniki nie są edytowane „na oko” po wygenerowaniu;
- eksportowane tabele i rysunki mają deterministyczne nazwy;
- przy zmianie definicji obserwabli wszystkie zależne wykresy i fragmenty tekstu są aktualizowane.

---

## 9. Styl pracy

### 9.1. Wzorzec stylistyczny

Styl ma być zbliżony do dostarczonych przez autora przykładowych prac licencjackich, przede wszystkim pod względem:

- sposobu prowadzenia narracji,
- stopniowego wprowadzania problemu,
- przechodzenia od intuicji do definicji matematycznej,
- objaśniania równań po ich wprowadzeniu,
- łączenia tekstu z rysunkami,
- unikania przesadnie „podręcznikowego” tonu.

Przykładowe prace służą **jako wzór językowy i kompozycyjny, nie jako źródło merytoryczne** dla obecnej analizy.

### 9.2. Język

Zgodnie z wcześniejszym ustaleniem:

- **docelowy tekst pracy: po angielsku**;
- komunikacja z autorem, komentarze robocze i notatki mogą być po polsku;
- polskie wersje robocze nie oznaczają automatycznie zmiany języka finalnej pracy.

Nowsze, jednoznaczne polecenie autora ma zawsze pierwszeństwo.

### 9.3. Jak pisać

Tekst pracy powinien być:

- formalny,
- naukowy,
- precyzyjny,
- logiczny,
- zwarty,
- naturalny językowo.

Preferowana struktura akapitu:

1. **problem / motywacja**,
2. **definicja lub metoda**,
3. **sens fizyczny**,
4. **co sprawdzamy na danych**,
5. **co faktycznie obserwujemy**.

Agent ma dbać o płynne przejścia między sekcjami. Rozdział nie może wyglądać jak posklejane odpowiedzi z czatu.

### 9.4. Czego unikać

W tekście pracy nie używać:

- potocznych sformułowań;
- sztucznego „lania wody”;
- wielkich deklaracji typu „rewolucyjna metoda” bez podstaw;
- metakomentarzy typu „na poniższym wykresie możemy zobaczyć, że...” powtarzanych co akapit;
- zdań bez jasnego podmiotu i odniesienia;
- przesadnie długich zdań wielokrotnie złożonych;
- list punktowanych tam, gdzie normalny wywód naukowy jest czytelniejszy;
- niespójnego mieszania terminologii polskiej i angielskiej.

---

## 10. LaTeX i Overleaf

### 10.1. Kompilator

**Wyłącznie pdfLaTeX**, chyba że autor wprost zmieni to wymaganie.

Nie wprowadzać bez zgody:

- LuaLaTeX,
- XeLaTeX,
- `fontspec`,
- `unicode-math`,
- rozwiązań wymagających zewnętrznych fontów.

### 10.2. Template

Repozytorium korzysta z układu opartego na szablonie Overleaf:

**„Wzór ISI UJ”**  
https://www.overleaf.com/latex/templates/wzor-isi-uj/ddszfvqhkwmt

To jest **wybrany przez autora wzorzec składu**, a nie dowód, że jest to oficjalny szablon WFAIS.

Agent ma zachować istniejące formatowanie szablonu, o ile nie ma konkretnego powodu technicznego, by coś zmienić.

### 10.3. Zasady edycji LaTeX

- nie przebudowywać preambuły dla samej „estetyki”;
- nie zmieniać marginesów, fontów, nagłówków i numeracji bez polecenia;
- korzystać z `\label{}` i `\ref{}` / `\eqref{}`;
- nie wpisywać ręcznie numerów rysunków, tabel ani równań;
- każdy rysunek ma mieć podpis i label;
- każda tabela ma mieć podpis i label;
- symbole definiować przy pierwszym użyciu;
- jednostki zapisywać konsekwentnie;
- utrzymywać jeden standard cytowań;
- bibliografię prowadzić w pliku `.bib`, a nie ręcznie w tekście.

Po zmianach dokument ma kompilować się bez:

- `Undefined reference`,
- `Citation ... undefined`,
- brakujących plików graficznych,
- błędów matematycznych LaTeX.

Ostrzeżenia typu `Overfull \hbox` powinny być sprawdzane, a nie bezmyślnie ignorowane.

---

## 11. Bibliografia i źródła

### Twarde zasady

Agent **nigdy nie wymyśla bibliografii**.

Każda pozycja musi być zweryfikowana przynajmniej przez jedno z:

- DOI,
- stronę wydawcy,
- arXiv,
- Crossref,
- Google Scholar / oficjalny rekord bibliograficzny,
- oficjalny dokument UJ.

Nie wolno generować „wiarygodnie wyglądających” autorów, tytułów, tomów ani numerów stron.

Dla twierdzeń dotyczących:

- NSDI / NSTI,
- recollision,
- modeli klasycznych,
- strong-field ionization,
- PCA,
- współrzędnych Jacobiego,
- kompozycyjnej analizy danych / ILR,

należy cytować literaturę adekwatną do konkretnego twierdzenia.

Notebook nie zastępuje źródła naukowego dla definicji standardowej metody, ale jest źródłem informacji o tym, **jak metoda została zastosowana w tej pracy**.

---

## 12. Wymagania formalne UJ / WFAIS, które agent ma respektować

### 12.1. Fizyka dla firm — informacje programu

W oficjalnym Sylabusie UJ kierunek **Fizyka dla firm** jest prowadzony na WFAIS jako studia I stopnia, a program jest skonstruowany tak, aby ostatni, szósty semestr był poświęcony przygotowaniu pracy licencjackiej.

Warunkiem ukończenia studiów jest pozytywna ocena pracy dyplomowej oraz zdanie egzaminu dyplomowego.

Źródło:
https://sylabus.uj.edu.pl/pl/8/1/2/7/191

Dla aktualnego programu:
https://sylabus.uj.edu.pl/pl/9/1/2/7/191

### 12.2. Pracownia licencjacka

Opis programu kierunku wskazuje, że student wybiera temat badań stanowiących podstawę pracy licencjackiej i przygotowuje ją pod kierunkiem nauczyciela akademickiego WFAIS. Badania mogą być realizowane w laboratorium naukowym lub u partnera przemysłowo-biznesowego w ramach Pracowni licencjackiej.

To oznacza, że praca ma być **oparta na realnym materiale badawczym i własnej analizie**, a nie tylko na kompilacji literatury.

### 12.3. Seminarium licencjackie

Oficjalny sylabus Seminarium licencjackiego podkreśla m.in.:

- prezentację własnych wyników;
- konfrontowanie własnych wyników z dostępną literaturą specjalistyczną;
- umiejętność przygotowania dłuższego wystąpienia;
- aktywny udział w dyskusji naukowej.

Źródło:
https://sylabus.uj.edu.pl/pl/document/15ee83e9-073c-4bf3-9c44-4133ac237624.pdf

W praktyce dla agenta oznacza to:

> każdy ważny wynik numeryczny powinien być nie tylko pokazany, ale również zestawiony z wiedzą fizyczną i literaturą.

### 12.4. Ogólny Regulamin Studiów UJ

Nadrzędne zasady dyplomowania wynikają z aktualnego Regulaminu Studiów UJ.

Aktualne dokumenty należy sprawdzać przed finalnym złożeniem pracy:
https://bip.uj.edu.pl/studia/regulamin

Na rok 2026 opublikowano również Uchwałę nr 30/IV/2026 Senatu UJ zmieniającą Regulamin Studiów. Aktualne akty są dostępne w serwisach UJ, m.in.:
https://sdka.cm.uj.edu.pl/pl/tok-studiow/

**Agent ma sprawdzić aktualny regulamin ponownie przed etapem final submission.**

### 12.5. Zasady używania AI

Na UJ obowiązuje Zarządzenie nr 115 Rektora UJ z 27 listopada 2025 r. dotyczące wykorzystywania narzędzi opartych na sztucznej inteligencji w dydaktyce.

Nie znaleziono w publicznie dostępnych materiałach jednoznacznego, szczegółowego dokumentu WFAIS określającego w tym kontekście zasady użycia AI konkretnie przy tej pracy licencjackiej.

Dlatego agent:

1. **nie może twierdzić**, że użycie AI w pracy jest automatycznie dozwolone albo zakazane w określonym zakresie;
2. ma respektować aktualny sylabus przedmiotu, regulacje UJ i instrukcje promotora;
3. ma traktować autora pracy jako osobę odpowiedzialną za merytoryczną weryfikację i ostateczne brzmienie tekstu;
4. nie może fałszować źródeł, wyników ani autorstwa analiz;
5. jeśli przepisy wymagają ujawnienia zakresu wykorzystania AI, należy przygotować takie oświadczenie zgodnie z aktualnymi zasadami.

### 12.6. Czego NIE udało się potwierdzić jako obowiązku WFAIS

W publicznie dostępnych materiałach nie znaleziono wiarygodnego, ogólnowydziałowego wymogu WFAIS narzucającego dla kierunku Fizyka dla firm np.:

- minimalną lub maksymalną liczbę stron;
- konkretny font;
- konkretny rozmiar fontu;
- konkretną interlinię;
- konkretne marginesy;
- obowiązek użycia konkretnego szablonu LaTeX.

Dlatego **nie wolno wymyślać takich wymagań**.

Dopóki promotor lub WFAIS nie wskaże inaczej, formatowanie repozytorium wynika z wybranego przez autora template'u oraz dobrych praktyk składu pracy naukowej.

---

## 13. Definicja „dobrej” sekcji analitycznej

Każda większa sekcja analizy powinna odpowiedzieć kolejno na pytania:

1. **Jaki problem próbujemy rozwiązać?**
2. **Dlaczego dotychczasowa reprezentacja jest niewystarczająca?**
3. **Jaką wielkość definiujemy?**
4. **Dlaczego ta definicja ma sens matematyczny?**
5. **Jaki jest jej sens fizyczny?**
6. **Jak obliczamy ją z danych?**
7. **Jak wygląda rozkład?**
8. **Co rzeczywiście można z niego wywnioskować?**
9. **Czego nie można z niego wywnioskować?**
10. **Jak wynik ma się do pozostałych obserwabli / kanałów / intensywności / literatury?**

Jeżeli sekcja jest tylko opisem wykresu bez odpowiedzi na te pytania, wymaga poprawy.

---

## 14. Kolejność logiczna rozdziału o metodzie

Preferowany ciąg narracyjny:

1. problem wizualizacji korelacji wieloelektronowych;
2. wcześniejsza reprezentacja simpleksowa i jej zalety;
3. ograniczenie skalowalności dla większej liczby elektronów;
4. pełne dane pędowe;
5. znaczenie osi polaryzacji \(z\);
6. PCA jako analiza eksploracyjna;
7. identyfikacja kolektywnego i względnych kierunków podłużnych;
8. przejście do stałej ortonormalnej bazy Jacobiego–Helmerta;
9. definicja \(Q,\xi_1,\xi_2\);
10. dowód zachowania informacji / rekonstrukcja;
11. definicja \(K\);
12. obserwable podziału pędu: \(x_i,N_{\mathrm{eff}},x_{\max}\);
13. sektory znakowe;
14. korelacje par i ewentualnie ILR;
15. porównanie direct/delayed;
16. porównanie intensywności;
17. interpretacja fizyczna;
18. ograniczenia metody i możliwe rozszerzenie na większą liczbę elektronów.

Nie przestawiać tej kolejności bez konkretnego powodu.

---

## 15. Rozszerzenie na większą liczbę elektronów

Jednym z argumentów za obecną metodą ma być skalowalność.

Dla \(N\) elektronów naturalnie można rozdzielić:

- jeden kierunek kolektywny
  \[
  Q_N\propto\sum_{i=1}^N p_i,
  \]
- oraz \(N-1\) ortogonalnych współrzędnych względnych.

W tekście można wspominać o uogólnieniu przez bazę Helmerta/Jacobiego, ale **nie należy udawać, że analiza dla \(N>3\) została empirycznie wykonana**, jeżeli repozytorium nie zawiera takich wyników.

---

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

---

## 17. Checklist przed uznaniem fragmentu za gotowy

### Merytoryka

- [ ] Wszystkie symbole są zdefiniowane.
- [ ] Nie pomylono \(Q\) z \(P_e\).
- [ ] Nie nazwano zmiany bazy redukcją wymiaru.
- [ ] Rozdzielono ruch kolektywny i względny.
- [ ] Uwzględniono nierozróżnialność elektronów.
- [ ] Nie wyciągnięto mechanizmu przyczynowego tylko z korelacji.
- [ ] Direct i delayed porównano przy tej samej intensywności.
- [ ] Wszystkie liczby pochodzą z aktualnego uruchomienia analizy.

### Matematyka / kod

- [ ] Transformacja jest ortonormalna.
- [ ] Sprawdzono rekonstrukcję \(p_2,p_3,p_4\).
- [ ] Sprawdzono zachowanie normy.
- [ ] Notebook przechodzi `Restart Kernel -> Run All`.
- [ ] Nie ma zależności od starego stanu pamięci Jupytera.
- [ ] Zera / NaN / clipping są traktowane jawnie.

### Tekst

- [ ] Sekcja ma jasny cel.
- [ ] Każde równanie jest objaśnione.
- [ ] Każdy rysunek jest omówiony w tekście.
- [ ] Podpis rysunku mówi, jaki dataset pokazano.
- [ ] Wnioski są proporcjonalne do danych.
- [ ] Nie ma „lania wody”.
- [ ] Nie ma sztucznego stylu generowanego przez LLM.
- [ ] Terminologia jest konsekwentna.

### Źródła

- [ ] Każde ważne twierdzenie teoretyczne ma źródło.
- [ ] Każda pozycja bibliograficzna istnieje.
- [ ] DOI / dane bibliograficzne zostały zweryfikowane.
- [ ] Nie skopiowano twierdzenia ze starej pracy jako faktu bez sprawdzenia.

### LaTeX

- [ ] Kompilator: pdfLaTeX.
- [ ] Brak undefined references.
- [ ] Brak undefined citations.
- [ ] Brak brakujących grafik.
- [ ] Numeracja jest automatyczna.
- [ ] Template nie został niepotrzebnie przebudowany.

---

## 18. Priorytety agenta

Jeżeli wymagania wchodzą ze sobą w konflikt, stosuj następującą kolejność:

1. **poprawność fizyczna i brak fałszywych wyników;**
2. **aktualne polecenie autora;**
3. **aktualne wymagania UJ/WFAIS i promotora;**
4. **reprodukowalność analizy;**
5. **spójność całej pracy;**
6. **styl naukowy;**
7. **estetyka LaTeX.**

Ładny PDF z błędną fizyką nadal jest błędną pracą. Niestety typografia nie ma jeszcze zdolności naprawiania mechaniki wielociałowej.

---

## 19. Najważniejsza zasada

> **Nie zgaduj. Sprawdzaj repozytorium, notebooki, dane i źródła.**
>
> Jeżeli czegoś nie da się uzasadnić na podstawie aktualnych wyników albo literatury, agent ma to powiedzieć zamiast produkować pewnie brzmiącą bzdurę.

Praca ma być napisana tak, aby czytelnik mógł przejść od problemu fizycznego przez definicję metody aż do wyników i wniosków bez zgadywania, skąd wziął się którykolwiek krok.
