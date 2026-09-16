---
name: interpret-ionization-results
description: Turn verified numerical results from this repository into cautious physical interpretations for strong-field triple ionization of neon.
---

# Interpretacja wyników fizycznych

Stosuj dopiero po zweryfikowaniu wyników notebooków. Ten skill nie służy do uruchamiania kodu ani do redakcji całych rozdziałów.

## Kontekst i granice wnioskowania

Praca dotyczy korelacji pędów elektronów w potrójnej jonizacji neonu w silnym polu laserowym na podstawie danych modelu ECBB.

Etykiety elektronów „tunelujący” i „związany” opisują role w trajektorii modelowej. Nie są fundamentalnymi cechami rozróżnialnych elektronów. Przy interpretacji sprawdzaj, czy obserwowany efekt jest niezmienniczy względem permutacji, czy zależy od przyjętego etykietowania.

Dla każdej tezy rozdziel:

1. obserwację: co dokładnie pokazuje rozkład, tabela lub statystyka;
2. interpretację: z jakim procesem wynik może być zgodny;
3. ograniczenie: czego ten wynik sam nie dowodzi;
4. oparcie w literaturze: źródło mechanizmu lub oczekiwania teoretycznego.

Nie wyprowadzaj mechanizmu z samej korelacji i nie używaj PCA jako dowodu rekolidowania.

## Używane wielkości

Rozróżniaj:

\[
P_e=p_2+p_3+p_4=\sqrt 3\,Q
\]

od znormalizowanego trybu \(Q\). Ruch względny opisują \(\xi_1,\xi_2\) oraz

\[
K=\sqrt{\xi_1^2+\xi_2^2}.
\]

Dla udziałów bezwzględnych:

\[
A=|p_2|+|p_3|+|p_4|,\qquad x_i=\frac{|p_i|}{A},
\]

\[
N_{\mathrm{eff}}=\frac{1}{x_2^2+x_3^2+x_4^2},\qquad
x_{\max}=\max(x_2,x_3,x_4).
\]

Znaki pędów przechowuj i interpretuj osobno jako sektory znakowe. `N_eff` opisuje równomierność udziałów bezwzględnego pędu, a nie liczbę „naprawdę emitowanych” elektronów. Współczynnik Pearsona jest miarą pomocniczą i nie opisuje pełnej zależności wieloelektronowej.

## Język wniosków

Używaj sformułowań proporcjonalnych do dowodów: „rozkład pokazuje”, „wynik sugeruje”, „jest zgodny z”. „Dowodzi” stosuj tylko wtedy, gdy metoda rzeczywiście wyklucza sensowne alternatywy.

Nie wymyślaj wartości, trendów, niepewności ani terminów naukowych. Jeśli wyniki są niespójne, statystycznie niewystarczające lub zależne od etykietowania, napisz to wprost.
