import os
import matplotlib
matplotlib.use('TkAgg')  # Usa il backend TkAgg per l'output grafico

print("DISPLAY:", os.environ.get('DISPLAY'))
os.environ['DISPLAY'] = ':1'  # Configura il display se necessario

import psutil
import pdb
import numpy as np
from fmpy import simulate_fmu, extract, read_model_description, instantiate_fmu
import matplotlib.pyplot as plt
from pidController import PidController

plt.ioff()  # Disabilita la modalità interattiva

# Funzione per monitorare l'utilizzo della memoria
def memory_usage():
    process = psutil.Process(os.getpid())
    return process.memory_info().rss

print(f"Utilizzo della memoria all'inizio: {memory_usage()} bytes")

# Callback per il logging
def log_message(instanceName, status, category, message):
    print(f"[{instanceName}] {category}: {message}")

# Parametri 
dt_control = 0.02  # 20 ms
dt_model = 0.005  # 0.1 ms

# Path al file FMU esportato da Modelica
fmu_path = 'Simulation.fmu'

unzipdir = os.path.abspath('extracted_fmu')  # Percorso assoluto
# Estrai il contenuto dell'FMU
print("Estrazione del contenuto dell'FMU...")

# Estrai il contenuto dell'FMU
extract(fmu_path, unzipdir='extracted_fmu')

# Leggi la descrizione del modello
model_description = read_model_description('extracted_fmu')

# Instanzia l'FMU
fmu_instance = instantiate_fmu(unzipdir, model_description, 'ModelExchange')


# Parametri di log
#log_level = 5  # Imposta un livello di log dettagliato

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
time_end = 0.4  # 10 secondi di simulazione

# Variabile per memorizzare lo stato del modello
model_state = None

# Lista per memorizzare gli input
input_data = []

# Apri un file di log
log_file = open('simulation_log.txt', 'w')

# Esegui la simulazione in blocchi di 1 secondo
#block_duration = 1.0
num_blocks = int(time_end / dt_control)


try:

    for block in range(num_blocks):
        start_time = block * dt_control
        end_time = start_time + dt_control
        log_file.write(f"Esecuzione della simulazione per il blocco {block + 1} da {start_time} a {end_time}\n")
        print(f"Esecuzione della simulazione per il blocco {block + 1} da {start_time} a {end_time}")

        try:
            log_file.write(f"Utilizzo della memoria prima della simulazione del blocco {block + 1}: {memory_usage()} bytes\n")
            print(f"Utilizzo della memoria prima della simulazione del blocco {block + 1}: {memory_usage()} bytes")

            # Prepara gli input
            #input_times = np.arange(start_time, end_time + dt_model, dt_model)
            #inputs = np.column_stack((input_times, np.full_like(input_times, duty_cycle)))
            #input_data.append(inputs)
            input_times = np.arange(start_time, end_time, dt_model)
            duty_cycles = np.full_like(input_times, duty_cycle)
            inputs_structured = np.zeros(input_times.shape[0], dtype=[('time', '<f8'), ('dutyCycle', '<f8')])
            inputs_structured['time'] = input_times
            inputs_structured['dutyCycle'] = duty_cycles

            # Debug: Stampa degli input
            log_file.write(f"Inputs for block {block + 1}: {inputs_structured}\n")
            print(f"Inputs for block {block + 1}: {inputs_structured}")

            model_state = simulate_fmu(fmu_path, start_time=start_time, stop_time=end_time, step_size=dt_model, input=inputs_structured, output=['currentFeedback'], fmi_type='ModelExchange')

            # Debugging con PDB
             #pdb.set_trace()
            # Debug: Stampa del risultato della simulazione
            if model_state is None:
                raise ValueError("simulate_fmu returned None")
            
            log_file.write(f"Utilizzo della memoria dopo la simulazione del blocco {block + 1}: {memory_usage()} bytes\n")
            print(f"Utilizzo della memoria dopo la simulazione del blocco {block + 1}: {memory_usage()} bytes")

            # Debug: Stampa del risultato della simulazione
            log_file.write(f"Model state for block {block + 1}: {model_state}\n")
            print(f"Model state for block {block + 1}: {model_state}")

            # Debug: Stampa dei tempi generati dal modello
            block_time = model_state['time']
            block_feedback = model_state['currentFeedback']
            log_file.write(f"Block time: {block_time}\n")
            print(f"Block time: {block_time}")

            if model_state is None:
                raise ValueError("simulate_fmu returned None")
            
        #except Exception as e:
        #    log_file.write(f"Errore durante la simulazione del blocco {block + 1}: {e}\n")
        #    print(f"Errore durante la simulazione del blocco {block + 1}: {e}")
        #    break

    
        #if model_state is not None:
        #    # Ottieni i risultati del blocco
            block_time = model_state['time'][-1]
        #    block_feedback = model_state['currentFeedback']
            feedback = model_state['currentFeedback'][-1]
            #for t, feedback in zip(block_time, block_feedback):
            #if block_time % dt_control < dt_model:
            controller.update(setpoint=400, feedback=feedback, reset_hold=0, reset_val=0)
            duty_cycle = controller.output
            time_data.append(block_time)
            current_feedback_data.append(feedback)
            duty_cycle_data.append(duty_cycle)
            log_file.write(f"Utilizzo della memoria dopo l'aggiornamento del PID: {memory_usage()} bytes\n")
            log_file.write(f"Tempo: {block_time}, Feedback: {feedback}, Duty Cycle: {duty_cycle}\n")
                        
            print(f"Utilizzo della memoria dopo l'aggiornamento del PID: {memory_usage()} bytes")
        except Exception as e:
            log_file.write(f"Errore durante la simulazione del blocco {block + 1}: {e}\n")
            print(f"Errore durante la simulazione del blocco {block + 1}: {e}")
            break
        
        # Verifica i dati raccolti finora
        log_file.write("Lunghezza dei dati raccolti finora:\n")
        log_file.write(f"Time: {len(time_data)}\n")
        log_file.write(f"Current Feedback: {len(current_feedback_data)}\n")
        log_file.write(f"Duty Cycle: {len(duty_cycle_data)}\n")
       
        print("Lunghezza dei dati raccolti finora:")
        print(f"Time: {len(time_data)}")
        print(f"Current Feedback: {len(current_feedback_data)}")
        print(f"Duty Cycle: {len(duty_cycle_data)}")
        
except Exception as e:
    log_file.write(f"An error occurred: {e}\n")
    print(f"An error occurred: {e}")    



# Verifica la raccolta dei dati
log_file.write("Lunghezza dei dati raccolti:\n")
log_file.write(f"Time: {len(time_data)}\n")
log_file.write(f"Current Feedback: {len(current_feedback_data)}\n")
log_file.write(f"Duty Cycle: {len(duty_cycle_data)}\n")
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
        log_file.write(f"Errore durante la visualizzazione dei grafici: {e}\n")
    
        print("Nessun dato da visualizzare.")
except Exception as e:
    log_file.write(f"Utilizzo della memoria alla fine: {memory_usage()} bytes\n")
    log_file.close()
    print(f"Errore durante la visualizzazione dei grafici: {e}")