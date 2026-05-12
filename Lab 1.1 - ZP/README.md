# Mini-framework do symulacji numerycznych

Projekt ten implementuje modułowe, obiektowe środowisko do uruchamiania symulacji numerycznych w języku Python. Framework został zaprojektowany, oddzielając logikę sterującą od reguł wyliczania kroków, analizy oraz wizualizacji

## Zaimplementowane modele
W ramach frameworka zaimplementowano dwa modele:
1. Oscylator tłumiony - jednowymiarowy model fizyczny punktu materialnego na sprężynie z tłumieniem (rozwiązywany numerycznie metodą Eulera-Cromera)
2. Model SIR na siatce 2D - rozprzestrzeniania się epidemii na siatce dwuwymiarowej, korzystający z sąsiedztwa Moore'a (osiem najbliższych komórek), periodycznych warunków brzegowych i dynamiki synchronicznej

## Generowane wykesy i obrazy
W ramach obecnie zaimplementowanych modeli generowane są:
1. Wykres położenia i prędkości w czasie, jak i wykres całkowitej energii z podzieleniem jej na kinetyczną i potencjalną
2. Animację dynamiki symulowanej epidemii i zmiany liczby chorych, zdrowych i wyzdrowiałych w czasie, jak i animowaną siatkę 2D społeczności

## Architektura i Klasy
- `Simulation` - główny koordynator pętli
- Klasy abstrakcyjne: `StepRule`, `StepAnalyzer`, `FinalAnalyzer`, `Visualizer`
- Klasy `dataclass`: Przechowują konfigurację, stany i statystyki. Podzielono je na wstępną konfigurację (`SimulationConfig`), stan w konkretnym kroku symulacji (`SimulationState`) oraz przetrzymywanie wyników

## Wymagania
- Python 3.14
- Wymagane biblioteki: `numpy`, `matplotlib`, `pillow` (bilbioteka do zapisywania symulacji do pliku gif)

## Uruchomienie
Aby uruchomić symulacje, należy wywołać w konsoli główny plik programu:
```bash
python main.py