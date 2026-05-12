from typing import List
from core import (
    SimulationConfig, SimulationState, StepStatistics, FinalStatistics,
    SimulationResult, StepRule, StepAnalyzer, FinalAnalyzer, Visualizer
)

class Simulation:
    def __init__(
        self, 
        config: SimulationConfig, 
        initial_state: SimulationState, 
        step_rule: StepRule, 
        step_analyzer: StepAnalyzer, 
        final_analyzer: FinalAnalyzer, 
        visualizer: Visualizer
    ):
        self.config = config
        self.current_state = initial_state
        self.step_rule = step_rule
        self.step_analyzer = step_analyzer
        self.final_analyzer = final_analyzer
        self.visualizer = visualizer

    def run(self) -> SimulationResult:
        states = [self.current_state]
        
        initial_stats = self.step_analyzer.analyze_step(self.config, self.current_state)
        step_stats = [initial_stats]

        for _ in range(self.config.steps):
            new_state = self.step_rule.next_step(self.config, self.current_state)
            current_step_stats = self.step_analyzer.analyze_step(self.config, new_state)
            
            states.append(new_state)
            step_stats.append(current_step_stats)
            self.current_state = new_state

        final_stats = self.final_analyzer.analyze_final(self.config, states, step_stats)

        return SimulationResult(
            config=self.config,
            states=states,
            step_stats=step_stats,
            final_stats=final_stats
        )