from dataclasses import dataclass
from typing import List
import matplotlib.pyplot as plt

from core import (
    SimulationConfig, SimulationState, StepStatistics, FinalStatistics,
    StepRule, StepAnalyzer, FinalAnalyzer, Visualizer, SimulationResult
)

@dataclass
class OscillatorConfig(SimulationConfig):
    mass: float
    spring_constant: float
    damping: float

@dataclass
class OscillatorState(SimulationState):
    position: float
    velocity: float

@dataclass
class OscillatorStepStats(StepStatistics):
    kinetic_energy: float
    potential_energy: float
    total_energy: float

@dataclass
class OscillatorFinalStats(FinalStatistics):
    max_displacement: float
    final_energy: float

class OscillatorStepRule(StepRule):
    def next_step(self, config: OscillatorConfig, current_state: OscillatorState) -> OscillatorState:
        force_spring = -config.spring_constant * current_state.position # F = -kx
        force_damping = -config.damping * current_state.velocity # F = -bv
        acceleration = (force_spring + force_damping) / config.mass # a = F/m
        
        new_velocity = current_state.velocity + acceleration * config.dt
        new_position = current_state.position + new_velocity * config.dt
        
        # Zwracamy nowy stan zaktualizowany o nowe położenie i prędkość
        return OscillatorState(
            step=current_state.step + 1,
            time=current_state.time + config.dt,
            position=new_position,
            velocity=new_velocity
        )

class OscillatorStepAnalyzer(StepAnalyzer):
    def analyze_step(self, config: OscillatorConfig, state: OscillatorState) -> OscillatorStepStats:
        kinetic = 0.5 * config.mass * (state.velocity ** 2) # E_k = 1/2 * m * v^2
        potential = 0.5 * config.spring_constant * (state.position ** 2) # E_p = 1/2 * k * x^2

        # Zwracamy statystyki dla konkrenego kroku
        return OscillatorStepStats(
            kinetic_energy=kinetic,
            potential_energy=potential,
            total_energy=kinetic + potential
        )

class OscillatorFinalAnalyzer(FinalAnalyzer):
    def analyze_final(self, config: OscillatorConfig, states: List[OscillatorState], step_stats: List[OscillatorStepStats]) -> OscillatorFinalStats:
        max_disp = max(abs(state.position) for state in states)
        final_en = step_stats[-1].total_energy
        return OscillatorFinalStats(max_displacement=max_disp, final_energy=final_en)

class OscillatorVisualizer(Visualizer):
    def visualize(self, result: SimulationResult, filename: str) -> None:
        times = [state.time for state in result.states]
        positions = [state.position for state in result.states]
        velocities = [state.velocity for state in result.states]
        kin_energies = [stat.kinetic_energy for stat in result.step_stats]
        pot_energies = [stat.potential_energy for stat in result.step_stats]
        tot_energies = [stat.total_energy for stat in result.step_stats]

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

        ax1.plot(times, positions, label = 'Położenie (x)', color = 'blue')
        ax1.plot(times, velocities, label = 'Prędkość (v)', color = 'orange', linestyle = '--')
        ax1.set_title('Zależność położenia i prędkości od czasu')
        ax1.set_xlabel('Czas [s]')
        ax1.set_ylabel('Położenie [m] / prędkość [m/s]')
        ax1.legend()
        ax1.grid(True, alpha = 0.5, linestyle = '--')

        ax2.plot(times, kin_energies, label = 'Energia kinetyczna', color = 'red')
        ax2.plot(times, pot_energies, label = 'Energia potencjalna', color = 'green')
        ax2.plot(times, tot_energies, label = 'Energia całkowita', color = 'black', linewidth = 2)
        ax2.set_title('Stosunek energii kinetycznej, potencjalnej i całkowitej w czasie')
        ax2.set_xlabel('Czas [s]')
        ax2.set_ylabel('Energia [J]')
        ax2.legend()
        ax2.grid(True, alpha = 0.5, linestyle = '--')

        plt.tight_layout()
        plt.savefig(filename)