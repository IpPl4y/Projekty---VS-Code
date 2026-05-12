import numpy as np
from engine import Simulation

from oscillator import (
    OscillatorConfig, OscillatorState, OscillatorStepRule,
    OscillatorStepAnalyzer, OscillatorFinalAnalyzer, OscillatorVisualizer
)

from sir import (
    SIRConfig, SIRState, SIRStepRule, 
    SIRStepAnalyzer, SIRFinalAnalyzer, SIRVisualizer, SIRAnimator
)

def run_oscillator():
    print("\n--- Uruchamianie symulacji oscylatora tłumionego ---")
    config = OscillatorConfig(steps=1000, dt=0.01, mass=1.0, spring_constant=5.0, damping=0.1)
    initial_state = OscillatorState(step=0, time=0.0, position=2.0, velocity=0.0)

    sim = Simulation(
        config=config, initial_state=initial_state, step_rule=OscillatorStepRule(),
        step_analyzer=OscillatorStepAnalyzer(), final_analyzer=OscillatorFinalAnalyzer(),
        visualizer=OscillatorVisualizer()
    )

    result = sim.run()
    print(f"Maksymalne wychylenie: {result.final_stats.max_displacement:.2f} m")
    print(f"Energia końcowa: {result.final_stats.final_energy:.2f} J")
    sim.visualizer.visualize(result, "oscylator_wykres.png")
    print("Zapisano wykres: oscylator_wykres.png\n")

def run_sir():
    print("\n--- Uruchamianie symulacji epidemii SIR ---")
    width, height = 50, 50
    config = SIRConfig(steps=150, dt=1.0, width=width, height=height, p_infect=0.15, p_recovery=0.05)
    
    initial_grid = np.zeros((height, width), dtype=int)
    cy, cx = height // 2, width // 2
    initial_grid[cy, cx] = initial_grid[cy+1, cx] = initial_grid[cy, cx+1] = initial_grid[cy-1, cx-1] = 1

    initial_state = SIRState(step=0, time=0.0, grid=initial_grid)

    sim = Simulation(
        config=config, initial_state=initial_state, step_rule=SIRStepRule(),
        step_analyzer=SIRStepAnalyzer(), final_analyzer=SIRFinalAnalyzer(),
        visualizer=SIRAnimator()
    )

    result = sim.run()
    stats = result.final_stats
    print(f"Szczyt zakażeń: {stats.max_infected} chorych w kroku {stats.step_of_max_infected}.")
    print(f"Całkowita liczba osób zakażonych w trakcie symulacji: {stats.total_infected_overall}.")
    sim.visualizer.visualize(result, "sir_animacja.gif")
    print("Zapisano animację: sir_animacja.gif\n")

if __name__ == "__main__":
    print("Wybierz symulację do uruchomienia:")
    print("1. Oscylator harmoniczny (tłumiony)")
    print("2. Rozprzestrzenianie się epidemii (Model SIR)")
    print("3. Uruchom obie")
    
    choice = input("Twój wybór (1/2/3): ")
    
    if choice == '1':
        run_oscillator()
    elif choice == '2':
        run_sir()
    elif choice == '3':
        run_oscillator()
        run_sir()