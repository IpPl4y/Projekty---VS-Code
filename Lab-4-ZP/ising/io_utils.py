import csv

def save_magnetization(magnetizations, filename):
    try:
        with open(filename, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Krok', 'Magnetyzacja'])
            for step, mag in enumerate(magnetizations):
                writer.writerow([step, mag])
    except OSError as e:
        raise OSError(f'Nie można zapisać do pliku {filename}. Szczegóły: {e}')