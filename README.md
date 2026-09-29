# Praca licencjacka

Repozytorium pracy licencjackiej przygotowywanej na kierunku Fizyka dla firm na WFAIS UJ.

Temat roboczy:

> **Analiza korelacji pędów wielu elektronów w potrójnej jonizacji neonu w silnym polu laserowym**

Tytuł zostanie dopracowany po ustabilizowaniu analizy i tekstu.

## Zawartość repozytorium

- `ECBB_model/` — dane modelu i dokumentacja ich znaczenia;
- notebooki `.ipynb` — implementacja analizy i jej aktualne wyniki;
- `main.tex` — tekst pracy w LaTeX;
- `bibliography.bib` — bibliografia;
- `.agents/skills/` — wyspecjalizowane instrukcje dla agentów;
- `AGENTS.md` — router wskazujący właściwy skill dla danego zadania.

Notebooki i aktualne outputy po wykonaniu od czystego kernela są źródłem prawdy dla wyników liczbowych. Literatura służy do opisu teorii, metod i możliwej interpretacji fizycznej.

## Instrukcje dla agenta

Agent powinien najpierw przeczytać `AGENTS.md`, a następnie tylko te skille, które odpowiadają wykonywanemu zadaniu.

| Zadanie | Skill |
|---|---|
| Zmiany w repozytorium, kompilacja i kontrola spójności | `.agents/skills/manage-thesis-repository/SKILL.md` |
| Odtworzenie i audyt analizy notebooków | `.agents/skills/analyze-ionization-data/SKILL.md` |
| Interpretacja fizyczna zweryfikowanych wyników | `.agents/skills/interpret-ionization-results/SKILL.md` |
| Pisanie i redakcja pracy w LaTeX | `.agents/skills/write-physics-thesis/SKILL.md` |

Dla zadania obejmującego cały proces obowiązuje kolejność:

1. zweryfikować analizę danych;
2. oddzielić obserwacje od interpretacji fizycznej;
3. napisać lub poprawić tekst;
4. skompilować i sprawdzić spójność repozytorium.

Nie należy ładować wszystkich instrukcji przy każdej drobnej zmianie.

## Najważniejsze założenia projektu

- PCA jest punktem wyjścia do rozpoznania istotnych kierunków zmienności, lecz końcowa analiza nie utożsamia stałej bazy z osiami PC1, PC8 i PC9.
- Transformacja \((p_2,p_3,p_4)\rightarrow(Q,\xi_1,\xi_2)\) jest ortogonalną zmianą bazy, nie redukcją wymiaru.
- Etykiety elektronów opisują role w trajektorii modelowej i nie mogą być przedstawiane jako fundamentalne cechy rozróżnialnych elektronów.
- Kanały `direct` i `delayed` porównuje się tylko przy tej samej intensywności pola.
- Obserwable ILR nie należą do analizy tekstowej.
- Korelacja ani PCA same w sobie nie dowodzą mechanizmu fizycznego.

Szczegółowe definicje, kontrole i zasady formułowania wniosków znajdują się w odpowiednich skillach, zamiast być powtarzane w tym pliku.
