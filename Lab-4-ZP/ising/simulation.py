import numpy as np
import time
from numba import njit
from .helpers import initialize_grid, calculate_initial_energy

def macrostep_python(grid, N, J, B, beta, current_energy):
    for _ in range(N**2):
        i = np.random.randint(0, N)
        j = np.random.randint(0, N)

        top = (i - 1) % N
        bottom = (i + 1) % N
        left = (j - 1) % N
        right = (j + 1) % N

        sum_nn = (grid[top, j] + grid[bottom, j] + grid[i, left] + grid[i, right] +
                  grid[top, left] + grid[top, right] + grid[bottom, left] + grid[bottom, right])
        
        dE = 2.0 * grid[i, j] * (J * sum_nn + B)

        if dE < 0 or np.random.rand() < np.exp(-beta * dE):
            grid[i, j] *= -1
            current_energy += dE
            
    return current_energy

@njit
def macrostep_numba(grid, N, J, B, beta, current_energy):
    for _ in range(N**2):
        i = np.random.randint(0, N)
        j = np.random.randint(0, N)
        
        top = (i - 1) % N
        bottom = (i + 1) % N
        left = (j - 1) % N
        right = (j + 1) % N
        
        sum_nn = (grid[top, j] + grid[bottom, j] + grid[i, left] + grid[i, right] +
                  grid[top, left] + grid[top, right] + grid[bottom, left] + grid[bottom, right])
        
        dE = 2.0 * grid[i, j] * (J * sum_nn + B)
        
        if dE < 0 or np.random.rand() < np.exp(-beta * dE):
            grid[i, j] *= -1
            current_energy += dE
            
    return current_energy

def run_simulation(N, J, B, beta, M, use_numba=True):
    if beta < 0:
        raise ValueError('Parametr beta (odwrotność temperatury) nie może być ujemny.')
    if M <= 0:
        raise ValueError('Liczba makrokroków M musi być dodatnia.')

    grid = initialize_grid(N)
    energy = calculate_initial_energy(grid, N, J, B)

    magnetizations = []
    energies = []
    grids_history = []

    step_func = macrostep_numba if use_numba else macrostep_python
    
    start_time = time.time()
    for step in range(M):
        grids_history.append(grid.copy())
        magnetizations.append(np.sum(grid) / (N * N))
        energies.append(energy)
        
        energy = step_func(grid, N, J, B, beta, energy)
        
    end_time = time.time()
    
    return grids_history, magnetizations, energies, end_time - start_time