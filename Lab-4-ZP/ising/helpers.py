import numpy as np

def initialize_grid(N):
    if N <= 0:
        raise ValueError('Rozmiar siatki N musi być dodatni.')
    return np.random.choice([-1, 1], size=(N, N))

def calculate_initial_energy(grid, N, J, B):
    E = 0.0
    for i in range(N):
        for j in range(N):
            top = (i - 1) % N
            bottom = (i + 1) % N
            left = (j - 1) % N
            right = (j + 1) % N
            
            sum_nn = (grid[top, j] + grid[bottom, j] + grid[i, left] + grid[i, right] +
                      grid[top, left] + grid[top, right] + grid[bottom, left] + grid[bottom, right])
            
            E += -J * grid[i, j] * sum_nn / 2.0
            E += -B * grid[i, j]
    return E