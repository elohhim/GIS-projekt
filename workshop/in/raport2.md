# SK6. Atak na sieć (II)

## Raport wstępny do projektu w ramach kursu "Grafy i Sieci" (GIS)

### Patryk Kocielnik, Jan Kumor, 5.04.2018r.

---

## Opiekun projektu
dr inż. Sebastian Kozłowski

## Opis zadania

Dane są dwie sieci: euklidesowa i losowa (ER) o mniej więcej takiej samej liczbie wierzchołków i krawędzi. Porównać prawdopodobieństwa powodzenia ataku na losowe krawędzie tych sieci (udany atak to taki, który prowadzi do rozspójnienia sieci).

## Planowane wykorzystanie narzędzi w projekcie

- Środowisko rozwiązania: stacja robocza pod kontrolą systemu GNU/Linux,
- Język implementacji rozwiązania: Python,
- Narzędzie do wizualizacji wyników i referencyjnej weryfikacji rozwiązań: ~~Graph-Tool - biblioteka dla języka Python~~ igraph - bilbioteka języka C wraz z interfejsem dla języka Python (python-igraph),


## Składniki rozwiązania

1. Moduł generacji sieci: euklidesowych oraz losowych, o zadanej liczbie wierzchołków.
   - Sposób wywołania: `graph = generate_graph(graph_type, vertex_probability)`,
   - Rezultat wywołania: `graph` jako dwuwymiarowa macierz sąsiedztwa (`int` * `int`) opisująca wygenerowany graf,
   - Podstawą komponentu będzie moduł generacji sieci z pakietu Graph-Tools [\[1\]](https://graph-tool.skewed.de/static/doc/generation.html#graph_tool.generation.random_graph).
2. Filtr usuwający z grafu losowo wybraną krawędź
   - sposób wywołania: `new_graph = break(graph)`.
   - rezultat wywołania: `new_graph` jako graf pozbawiony losowo wybranej krawędzi.
3. Analizator spójności sieci
   - Sposób wywołania: consistency\_degree(graph),
   - Rezultat wywołania: $n$ (`int`) jako liczba oznaczająca stan spójności grafu wejściowego: $0$ - niespójny, $1$ - spójny,

## Interfejs aplikacji

Interfejsem aplikacji będzie konsola tekstowa. Motywacją tego podejścia jest
łatwość łączenia aplikacji z interfejsem tekstowym w filtry, które później wyko-
rzystać można do analizy bardziej złożonych struktur.

## Przebieg eksperymentu

Liczbę iteracji $k$ ustal na wartość z przedziału od 1 do 25.
Liczbę wierzchołków $v$ ustal na należącą do zbioru $V_num$: 10, 100, 1000, 10000, 100000,
Liczbę krawędzi ustal na należącą do zbioru $E_num$: 10, 100, 1000, 10000, 100000.

1. Powtórz dla k przypadków:
  1. Wygeneruj graf o zadanym typie, liczbie wierzchołków `v` i liczbie krawędzi `e`,
  2. Usuń z grafu losowo wybraną krawędź,
  3. Sprawdź, czy nastąpiło rozspójnienie grafu.
2. Oblicz iloczyn: $rozspójnień / ataków$

## Generowanie grafów losowych

Generowanie grafu losowego będzie podzielone na dwa etapy.

Pierwszym etapem będzie przyjęcie zadanej liczby wierzchołków oraz zadanej gęstości grafu i obliczenie z nich docelowej liczby krawędzi $q_target$dla grafu wyjściowego. Drugi etap polegał będzie na wygenerowaniu grafu o n wierzchołkach połączonych losowo $q_target$ krawędziami.

Algorytm ten przyjmuje dwa argumenty: liczbę wierzchołków $n$ oraz współczynnik prawdopodobieństwa wystąpienia krawędzi $n$.

Grafy euklidesowe generowane będą poprzez weryfikację, czy dany losowo wygenerowany graf posiada własności grafu euklidesowego. Wygenerowane grafy nie spełniające tego warunku będą odrzucane.

Złożoność obliczeniowa algorytmu:

$(n * (n - 1)) / 2$

Oczekiwana liczba krawędzi:

$(n * (n - 1) * p) / 2$

Spodziewany średni stopień wierzchołka:

$(n - 1) * p$

## Weryfikacja spójności grafu

Pseudokod algorytmu DFS [\[2\]](http://eduinf.waw.pl/inf/alg/001_search/0128a.php), który zostanie wykorzystany do badania spójności grafów, przedstawiony został poniżej :

1. Utwóż tablicę `visited` o `n` elementach,
2. Tablicę `visited` wypełnij wartościami `false`,
3. Utwórz pusty stos `S`,
4. Inicjuj licznik odwiedzonych wierzchołków,
5. Rozpocznij przejście DFS od wierzchołka 0,
6. Wierzchołek oznacz jako odwiedzony,
7. Przechodź przez graf dopóki stos `S` nie jest pusty, wykonując następujące kroki:
  - Pobierz wierzchołek ze stosu,
  - Pobrany wierzchołek usuń ze stosu,
  - Zwiększ licznik odwiedzonych wierzchołków,
  - Przejrzyj kolejnych sąsiadów,
    - Szukaj do sąsiadów jeszcze nie odwiedzonych,
    - Odznacz sąsiada jeśli jeszcze nie odwiedzony,
    - Umieść sąsiada na stosie.
Jeśli wszystkie wierzchołki zostały odwiedzone, graf jest spójny. W przeciwnym wypadku, graf jest niespójny.

Złożoność czasowa algorytmu wynosi $O(E + V)$

## Schemat testów

Testy zostaną przeprowadzone w następujący sposób:

1. Z wcześniej zdefiniowanej listy zostanie przyjęty zestaw parametrów testu,
2. Wygenerowany zostanie zestaw $k$ grafów testowych o przyjętych wcześniej parametrach,
~~2. Z każdego z grafów zostanie usunięta losowo wybrana krawędź,~~
3. Dla każdego z grafów:
  3.1. Dla każdej z krawędzi badanego grafu:
    3.1.1. Krawędź ta zostanie usunięta z grafu (zostanie przeprowadzony atak na tę krawędź),
    3.1.2. Sprawdzona zostanie spójność grafu po przeprowadzeniu ataku,
    3.1.3. Jeśli graf nie jest spójny atak zakończył się powodzeniem,
  3.2. Obliczone zostanie prawdopodobieństwo powodzenia ataku na losowo wybraną krawędź z badanego grafu, zgodnie ze wzorem: $p_i = n_{sukces} / m$
4. Zgodnie ze wzorem: $p_śr = sum_{i=0}^{k} p_i / k$, zostanie obliczone średnie prawdopodobieństwo powodzenia ataku dla zestawu $k$ grafów testowych o przyjętych parametrach.
~~3. Spójność grafu zostanie sprawdzona i zapisana,~~
~~4. Obliczone zostanie prawdopodobieństwo rozspójnienia grafu $P$ jako iloraz: $rozspójnień / ataków$~~
5. Jeśli pozostały nieprzetestowane zestawy parametrów, nastąpi powrót do punktu 1.

## Model danych

Projektowane narzędzie wykorszystywać będzie implementacje grafów nieskierowanych z biblioteki _igraph_.

Graf we wspomnianej implementacji jest reprezentowany jako wielozbiór krawędzi
oraz metadane. Najważniejszymi polami zawartymi w metadanych są:

* liczba wierzchołków grafu,
* określenie czy graf jest skierowany czy nie.

Każda z krawędzi grafu nieskierowanego jest modelowana jako nieuporządkowana para (dwuelementowy
zbiór) etykiet oznaczających wierzchołki grafu. Krawędzie są etykietowane, a
etykiety przyjmują wartości od 0 do $E - 1$. Etykiety wierzchołków przyjmują
wartości od 0 do $V - 1$.

Przykładową, uproszczoną (pominięto etykiety krawędzi) strukturę grafu
nieskierowanego przedstawiono poniżej:
```
 ( wierzchołki: 6,
   skierowany: nie,
   krawędzie:
    {
     {0,2},
     {2},
     {2,3},
     {3},
     {3,4},
     {3,4},
     {4,1}
    }
  )
```

Należy nadmienić, iż implementacja ta dopuszcza istnienie w grafie pętli. Jednak
w projektowanym narzędziu grafy takie nie będą rozpatrywane.
