from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List

# Podstawowe klasy i interfejsy dla symulacji

@dataclass
class SimulationConfig(ABC):
    steps: int
    dt: float

@dataclass
class SimulationState(ABC):
    step: int
    time: float

@dataclass
class StepStatistics(ABC):
    pass

@dataclass
class FinalStatistics(ABC):
    pass

@dataclass
class SimulationResult:
    config: SimulationConfig
    states: List[SimulationState]
    step_stats: List[StepStatistics]
    final_stats: FinalStatistics

# Klasa odpowiedzialna za logikę kolejnego kroku symulacji
class StepRule(ABC):
    @abstractmethod
    def next_step(self, config: SimulationConfig, current_state: SimulationState) -> SimulationState:
        pass

# Klasa odpowiedzialna za analizę danych po każdym kroku
class StepAnalyzer(ABC):
    @abstractmethod
    def analyze_step(self, config: SimulationConfig, state: SimulationState) -> StepStatistics:
        pass

# Klasa odpowiedzialna za analizę danych po zakończeniu symulacji
class FinalAnalyzer(ABC):
    @abstractmethod
    def analyze_final(self, config: SimulationConfig, states: List[SimulationState], step_stats: List[StepStatistics]) -> FinalStatistics:
        pass

# Klasa odpowiedzialna za wizualizację wyników symulacji
class Visualizer(ABC):
    @abstractmethod
    def visualize(self, result: SimulationResult, filename: str) -> None:
        pass