import sys

from ising.cli import parse_arguments
from ising.simulation import run_simulation
from ising.io_utils import save_magnetization
from ising.visualization import handle_animation, plot_results

def main():
    args = parse_arguments()

    try:
        print(f'Uruchamianie symulacji o parametrach: (N = {args.N}, M = {args.M}, beta = {args.beta})')
        
        # Symulacja główna
        grids_history, magnetizations, energies, sim_time = run_simulation(
            N=args.N, J=args.J, B=args.B, beta=args.beta, M=args.M, use_numba=True
        )
        print(f'Czas wykonania: {sim_time:.4f} s')

        # Zapis wyników
        if args.magnetization_file:
            save_magnetization(magnetizations, args.magnetization_file)
            print(f'Zapisano dane magnetyzacji do pliku: {args.magnetization_file}')

        # Wykresy
        if args.show_plots:
            plot_results(magnetizations, energies, args.M)

        # Wizualizacja
        if args.show_animation or args.animation_file:
            handle_animation(grids_history, args.beta, args.show_animation, args.animation_file)
            if args.animation_file:
                print(f'Zapisano animację do pliku: {args.animation_file}')

    except ValueError as e:
        print(f'Błąd wartości: {e}', file=sys.stderr) # file=sys.stderr zapewnia, że komunikat o błędzie trafi do konsoli, nie do pliku
        sys.exit(1)
    except OSError as e:
        print(f'Błąd systemu plików: {e}', file=sys.stderr)
        sys.exit(1)
    except RuntimeError as e:
        print(f'Błąd wykonania: {e}', file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f'Nieoczekiwany błąd: {e}', file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()