import os
import matplotlib
matplotlib.use('TkAgg')  # Usa il backend TkAgg per l'output grafico

print("DISPLAY:", os.environ.get('DISPLAY'))
os.environ['DISPLAY'] = ':1'  # Configura il display se necessario

import psutil

import numpy as np
from fmpy import instantiate_fmu, extract, read_model_description
import matplotlib.pyplot as plt
from pidController import PidController

# Funzione per monitorare l'utilizzo della memoria
def memory_usage():
    process = psutil.Process(os.getpid())
    return process.memory_info().rss

plt.ion()  # Abilita la modalità interattiva

# Parametri 
dt_control = 0.02  # 20 ms
dt_model = 0.001  # 0.1 ms

# Path al file FMU esportato da Modelica
fmu_path = 'Simulation.fmu'
unzip_dir = os.path.abspath('extracted_fmu')
# Estrai il contenuto dell'FMU
print("Estrazione del contenuto dell'FMU...")

# Estrai il contenuto dell'FMU

extract(fmu_path, unzipdir='extracted_fmu')

print(f"Utilizzo della memoria dopo l'estrazione dell'FMU: {memory_usage()} bytes")

# Leggi la descrizione del modello
model_description = read_model_description(fmu_path)

# Parametri di log
log_level = 5  # Imposta un livello di log dettagliato

time_data = []
current_feedback_data  = []
duty_cycle_data  = []

# Inizializza il controllore PID
controller = PidController(fw_gain=100,
                               p_gain=1000,
                               i_gain=10000,
                               d_gain=0,
                               output_max=40000,
                               output_min=1000)
duty_cycle = 0.0  # Inizializza il duty cycle

# Simula il sistema con il controllore
current_time = 0.0
time_end = 2  # 10 secondi di simulazione

# Variabile per memorizzare lo stato del modello
model_state = None

# Lista per memorizzare gli input
input_data = []

# Inizializza l'FMU
fmu_instance = instantiate_fmu(unzip_dir, model_description, 'ModelExchange')

try:
    while current_time < time_end:
        # Aggiorna il controllore PID ogni 20 ms
        if current_time % dt_control < dt_model:
            if model_state is not None:
                # Ottieni il feedback corrente dal modello
                print(f"Tempo corrente: {current_time}")
                current_feedback = model_state['currentFeedback'][-1]

                controller.update(setpoint=400,
                                   feedback=current_feedback,
                                   reset_hold=0,
                                   reset_val=0)

                duty_cycle = controller.output

                # Aggiungi i dati raccolti
                time_data.append(current_time)
                current_feedback_data.append(current_feedback)
                duty_cycle_data.append(duty_cycle)

                # Aggiungi i dati di input
                input_data.append((current_time, duty_cycle))

        # Funzione per monitorare l'utilizzo della memoria
        def memory_usage():
            process = psutil.Process(os.getpid())
            return process.memory_info().rss

        print(f"Utilizzo della memoria all'inizio: {memory_usage()} bytes")
        
        # Esegui la simulazione del modello per il passo successivo
        print(f"Esecuzione della simulazione per il tempo {current_time}")
        model_state = fmu_instance.simulate(fmu_path, start_time=current_time, stop_time=current_time + dt_model, step_size=dt_model, input=None, output=['currentFeedback'], fmi_type='ModelExchange')

        # Avanza il tempo di simulazione
        current_time += dt_model

    # Converti input_data in un array strutturato NumPy
    input_array = np.array(input_data, dtype=[('time', np.float64), ('dutyCycle', np.float64)])

    # Esegui la simulazione finale con gli input corretti
    model_state = fmu_instance.simulate(fmu_path, start_time=0.0, stop_time=time_end, step_size=dt_model, input=input_array, output=['currentFeedback'], fmi_type='ModelExchange')

except Exception as e:
    print(f"An error occurred: {e}")    



# Verifica la raccolta dei dati
print("Lunghezza dei dati raccolti:")
print(f"Time: {len(time_data)}")
print(f"Current Feedback: {len(current_feedback_data)}")
print(f"Duty Cycle: {len(duty_cycle_data)}")

# Plot dei risultati
try:
    if time_data and current_feedback_data and duty_cycle_data:
        print("DIsegno i grafici.")
        plt.figure()
        plt.subplot(2, 1, 1)
        plt.plot(time_data, current_feedback_data, label='Current Feedback')
        plt.xlabel('Time (s)')
        plt.ylabel('Current')
        plt.legend()
        plt.savefig("current_feedback_plot.png")  # Salva il grafico come immagine

        plt.subplot(2, 1, 2)
        plt.plot(time_data, duty_cycle_data, label='Duty Cycle')
        plt.xlabel('Time (s)')
        plt.ylabel('Duty Cycle')
        plt.legend()
        plt.savefig("duty_cycle_plot.png")  # Salva il grafico come immagine

        plt.show()
    else:
        print("Nessun dato da visualizzare.")
except Exception as e:
    print(f"Errore durante la visualizzazione dei grafici: {e}")