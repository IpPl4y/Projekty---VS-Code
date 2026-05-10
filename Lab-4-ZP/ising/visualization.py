import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def plot_results(magnetizations, energies, M):
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # Wykres 1 - magnetyzacja
    axes[0].plot(range(M), magnetizations, label='Magnetyzacja', color='deepskyblue')
    axes[0].set_xlabel('Kolejny krok symulacji')
    axes[0].set_ylabel('Magnetyzacja m(t)')
    axes[0].set_title('Magnetyzacja w funkcji czasu')
    axes[0].grid(True, linestyle='--', alpha=0.5)

    # Wykres 2 - energia
    axes[1].plot(range(M), energies, label='Energia', color='darkorange')
    axes[1].set_xlabel('Kolejny krok symulacji')
    axes[1].set_ylabel('Całkowita Energia H(t)')
    axes[1].set_title('Energia w funkcji czasu')
    axes[1].grid(True, linestyle='--', alpha=0.5)

    plt.tight_layout()
    plt.show()

def handle_animation(grids_history, beta, show_animation=False, animation_file=None):
    fig, ax = plt.subplots()
    img = ax.imshow(grids_history[0], cmap='winter', vmin=-1, vmax=1)
    ax.set_title(f'Symulacja modelu Isinga (T = {round(1/beta, 4) if beta > 0 else 'inf'})')
    ax.axis('off')

    def update(frame):
        img.set_data(grids_history[frame])
        return img,

    anim = FuncAnimation(fig, update, frames=len(grids_history), interval=50, blit=True)

    if animation_file:
        try:
            anim.save(animation_file, fps=20, extra_args=['-vcodec', 'libx264'])
        except Exception as e:
            raise RuntimeError(f'Błąd zapisu animacji. Szczegóły: {e}')

    if show_animation:
        plt.show()