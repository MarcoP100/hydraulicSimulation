import h5py
import numpy as np
import matplotlib.pyplot as plt

# Percorso del file di risultato
result_file = '/home/vncuser/circuitSimulation/simulation_output/Simulation_res.mat'

# Verifica che il file esista
if not os.path.exists(result_file):
    raise Exception(f"File di risultato della simulazione non trovato: {result_file}")
else:
    print(f"File di risultato trovato: {result_file}")

# Funzione per leggere il file .mat con h5py
def read_mat_file(file_path):
    with h5py.File(file_path, 'r') as f:
        data = {}
        for key in f.keys():
            data[key] = np.array(f[key])
        return data

# Leggi il file .mat
try:
    mat_data = read_mat_file(result_file)
    print("Contenuto del file .mat:")
    for key in mat_data:
        print(f"{key}: {mat_data[key].shape}")

    # Estrarre variabili principali
    variable_names = mat_data.get('name', None)
    data_2 = mat_data.get('data_2', None)
    
    if variable_names is not None and data_2 is not None:
        # Converti i nomi delle variabili da array di byte a stringhe
        variable_names = [''.join(chr(x) for x in var).strip() for var in variable_names.T]
        
        # Stampa l'associazione tra nomi delle variabili e i loro indici
        for i, var_name in enumerate(variable_names):
            print(f"Variabile {i}: {var_name}")

        # Supponiamo che il tempo sia la prima riga di data_2
        time = data_2[0, :]

        # Plotta i risultati per ogni variabile
        for i in range(1, data_2.shape[0]):
            plt.figure()
            plt.plot(time, data_2[i, :], label=variable_names[i])
            plt.xlabel('Time')
            plt.ylabel(variable_names[i])
            plt.title(f'Simulation Results: {variable_names[i]}')
            plt.legend()
            plt.grid(True)
            plt.show()
    else:
        print("Variabili principali non trovate nel file .mat")
except Exception as e:
    print(f"Errore nella lettura del file .mat: {e}")


