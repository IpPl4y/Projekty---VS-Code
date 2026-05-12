import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import ListedColormap
from dataclasses import dataclass
from typing import List

from core import (
    SimulationConfig, SimulationState, StepStatistics, FinalStatistics,
    StepRule, StepAnalyzer, FinalAnalyzer, Visualizer, SimulationResult
)

@dataclass
class SIRConfig(SimulationConfig):
    width: int
    height: int
    p_infect: float
    p_recovery: float

@dataclass
class SIRState(SimulationState):
    grid: np.ndarray

@dataclass
class SIRStepStats(StepStatistics):
    susceptible: int
    infected: int
    recovered: int

@dataclass
class SIRFinalStats(FinalStatistics):
    max_infected: int
    step_of_max_infected: int
    total_infected_overall: int

class SIRStepRule(StepRule):
    def next_step(self, config: SIRConfig, current_state: SIRState) -> SIRState:
        old_grid = current_state.grid
        new_grid = old_grid.copy()
        w, h = config.width, config.height
        
        # Przechodzimy przez każdą komórkę siatki i aktualizujemy jej stan
        for y in range(h):
            for x in range(w):
                state = old_grid[y, x]
                if state == 0:
                    infected_neighbors = 0

                    # Sprawdzamy 8 sąsiadów - zarażenie może nastąpić z każdego kierunku, przy czym siatka jest toroidalna
                    for dy in [-1, 0, 1]:
                        for dx in [-1, 0, 1]: 
                            if dx == 0 and dy == 0:
                                continue
                            ny = (y + dy) % h
                            nx = (x + dx) % w
                            if old_grid[ny, nx] == 1:
                                infected_neighbors += 1
                                
                    if infected_neighbors > 0:
                        p_not_infected = (1 - config.p_infect) ** infected_neighbors
                        p_infection = 1 - p_not_infected
                        if np.random.random() < p_infection:
                            new_grid[y, x] = 1
                            
                elif state == 1:
                    if np.random.random() < config.p_recovery:
                        new_grid[y, x] = 2
                        
        return SIRState(step=current_state.step + 1, time=current_state.time + config.dt, grid=new_grid)

class SIRStepAnalyzer(StepAnalyzer):
    def analyze_step(self, config: SIRConfig, state: SIRState) -> SIRStepStats:
        return SIRStepStats(
            susceptible=int(np.sum(state.grid == 0)),
            infected=int(np.sum(state.grid == 1)),
            recovered=int(np.sum(state.grid == 2))
        )

class SIRFinalAnalyzer(FinalAnalyzer):
    def analyze_final(self, config: SIRConfig, states: List[SIRState], step_stats: List[SIRStepStats]) -> SIRFinalStats:
        infected_history = [stat.infected for stat in step_stats]
        max_inf = max(infected_history)
        max_inf_step = infected_history.index(max_inf)
        total_inf = step_stats[-1].infected + step_stats[-1].recovered
        return SIRFinalStats(max_infected=max_inf, step_of_max_infected=max_inf_step, total_infected_overall=total_inf)

class SIRVisualizer(Visualizer):
    def visualize(self, result: SimulationResult, filename: str) -> None:
        steps = [state.step for state in result.states]
        s_counts = [stat.susceptible for stat in result.step_stats]
        i_counts = [stat.infected for stat in result.step_stats]
        r_counts = [stat.recovered for stat in result.step_stats]

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

        ax1.plot(steps, s_counts, label = 'Podatni (S)', color = 'blue')
        ax1.plot(steps, i_counts, label = 'Zakażeni (I)', color = 'red')
        ax1.plot(steps, r_counts, label = 'Ozdrowiali (R)', color = 'green')
        ax1.set_title('Dynamika epidemii (Model SIR)')
        ax1.set_ylabel('Liczba osób')
        ax1.set_xlabel('Krok symulacji')
        ax1.legend()
        ax1.grid(True, alpha=0.5, linestyle='--')

        final_grid = result.states[-1].grid
        cmap = ListedColormap(['blue', 'red', 'green'])
        ax2.imshow(final_grid, cmap = cmap, vmin = 0, vmax = 2)
        ax2.set_title(f'Siatka końcowa (krok {steps[-1]})')
        ax2.axis('off')

        plt.tight_layout()
        plt.savefig(filename)


class SIRAnimator(Visualizer):
    def visualize(self, result: SimulationResult, filename: str) -> None:
        print('Generowanie animacji...')
        
        steps = [state.step for state in result.states]
        s_counts = [stat.susceptible for stat in result.step_stats]
        i_counts = [stat.infected for stat in result.step_stats]
        r_counts = [stat.recovered for stat in result.step_stats]

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        cmap = ListedColormap(['blue', 'red', 'green'])
        
        ax1.set_xlim(0, max(steps))
        max_y = max(s_counts[0], max(i_counts), max(r_counts))
        ax1.set_ylim(0, max_y + (max_y * 0.05))
        ax1.set_title('Dynamika epidemii (Model SIR)')
        ax1.set_ylabel('Liczba osób')
        ax1.set_xlabel('Krok symulacji')
        ax1.grid(True, alpha=0.5, linestyle='--')

        line_s, = ax1.plot([], [], label='Podatni (S)', color='blue')
        line_i, = ax1.plot([], [], label='Zakażeni (I)', color='red')
        line_r, = ax1.plot([], [], label='Ozdrowiali (R)', color='green')
        ax1.legend()

        im = ax2.imshow(result.states[0].grid, cmap=cmap, vmin=0, vmax=2)
        title = ax2.set_title('Epidemia SIR - Krok 0')
        ax2.axis('off')

        def update(frame):
            current_steps = steps[:frame+1]
            line_s.set_data(current_steps, s_counts[:frame+1])
            line_i.set_data(current_steps, i_counts[:frame+1])
            line_r.set_data(current_steps, r_counts[:frame+1])

            im.set_data(result.states[frame].grid)
            title.set_text(f'Epidemia SIR - Krok {result.states[frame].step}')
            
            return [line_s, line_i, line_r, im, title]

        anim = animation.FuncAnimation(
            fig, 
            update, 
            frames=len(result.states), 
            interval=100,
            blit=True
        )
        
        # Zapis animacji do pliku GIF
        anim.save(filename, writer = 'pillow', fps=10)
        print(f"Animacja zapisana do pliku: {filename}")