import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description='Symulacja Monte Carlo modelu Isinga 2D.')
    
    parser.add_argument('--N', type=int, default=100, help='Rozmiar siatki N x N (domyślnie: 100)')
    parser.add_argument('--M', type=int, default=500, help='Liczba makrokroków (domyślnie: 500)')
    parser.add_argument('--beta', type=float, default=0.4, help='Odwrotność temperatury (domyślnie: 0.4)')
    parser.add_argument('--B', type=float, default=0.0, help='Zewnętrzne pole magnetyczne (domyślnie: 0.0)')
    parser.add_argument('--J', type=float, default=1.0, help='Stała oddziaływania (domyślnie: 1.0)')
    
    parser.add_argument('--magnetization-file', type=str, help='Plik do zapisu magnetyzacji (np. mag.csv)')
    parser.add_argument('--show-animation', action='store_true', help='Uruchomienie animacji w oknie')
    parser.add_argument('--animation-file', type=str, help='Plik do zapisu animacji (np. ising.mp4)')
    parser.add_argument('--show-plots', action='store_true', help='Wyświetl wykresy magnetyzacji i energii na koniec symulacji')

    return parser.parse_args()