from OMPython import OMCSessionZMQ, ModelicaSystem
import matplotlib.pyplot as plt
import os
import shutil
import numpy as np
from pidController import PidController


# Inizializza la sessione OMC
omc = OMCSessionZMQ()

# Percorso al file package.mo
package_path = '/home/vncuser/circuitSimulation/Simulation/package.mo'
model_name = 'Simulation.Simulation'

# Carica il modello usando ModelicaSystem
try:
    mod = ModelicaSystem(package_path, model_name)
    print("Pacchetto caricato con successo")
except Exception as e:
    print(f"Errore nel caricamento del pacchetto: {e}")

# Parametri di simulazione
start_time = 0.0
stop_time = 20
step_size = 0.02
setpoint = 400.0

# Inizializza il controllore PID
controller = PidController(fw_gain=1000,
                               p_gain=100,
                               i_gain=1000,
                               d_gain=0,
                               output_max=40000,
                               output_min=0)
duty_cycle = 0.0  # Inizializza il duty cycle


# Definisci i vettori per memorizzare i risultati
all_time = []
all_measured_value = []
all_duty_value = []

mod.buildModel()
current_time = start_time

# Variabile per tracciare l'ultimo stato del modello
last_state = None

# Funzione per ottenere le condizioni iniziali dal file di risultato
def get_initial_conditions(variables):
    initial_conditions = {}
    for var in variables:
        data = np.array(mod.getSolutions(var))
        if len(data.shape) > 1:
            data = data.flatten()
        initial_conditions[var] = data[-1]
    return initial_conditions

variableSave = ['solenoid.i_A'] 


while current_time < stop_time:


    # Simula il modello con parametri personalizzati
    #sim_flags = f"-startTime={start_time} -stopTime={stop_time} -numberOfIntervals={number_of_intervals} -method={method}"
    stopTime = current_time + step_size
    print("stop time:", stopTime)
    simflags = f"-override=startTime={current_time},stopTime={stopTime},stepSize=0.0001,method=dassl"
    
    #result_file = f"result_{current_time:.2f}.mat"

    # Aggiungi le condizioni iniziali se esistono
    if current_time > start_time:
        initial_conditions = get_initial_conditions(variableSave)
        for var, value in initial_conditions.items():
            simflags += f",{var}={value}"
    simflags += f",dutyCycle={duty_cycle}"

    mod.simulate(simflags=simflags)
    #print(f"Simulazione eseguita con simflags: {simflags}")
   
     # Ottieni il valore misurato dalla simulazione
    time = np.array(mod.getSolutions("time"))
    variable_name = 'currentFeedback'  # Sostituisci con il nome della variabile che vuoi graficare
    variable_data = np.array(mod.getSolutions(variable_name))
    dutyCycle_data = np.array(mod.getSolutions("dutyUsed"))

    # Verifica la struttura degli array
    if len(time.shape) > 1:
        #print("time è un array multidimensionale con forma:", time.shape)
        time = time.flatten()  # Appiattisci l'array se necessario
    if len(variable_data.shape) > 1:
        #print("currentFeedback è un array multidimensionale con forma:", variable_data.shape)
        variable_data = variable_data.flatten()  # Appiattisci l'array se necessario
    if len(dutyCycle_data.shape) > 1:
        #print("currentFeedback è un array multidimensionale con forma:", variable_data.shape)
        dutyCycle_data = dutyCycle_data.flatten()  # Appiattisci l'array se necessario

     # Verifica i valori minimi e massimi
    #print(f"Minimo e massimo di 'time': {time.min()}, {time.max()}")
    #print(f"Minimo e massimo di 'currentFeedback': {variable_data.min()}, {variable_data.max()}")

     # Accumula i risultati
    all_time.extend(time)
    all_measured_value.extend(variable_data)
    all_duty_value.extend(dutyCycle_data)

    current_feedback = variable_data[-1]
    controller.update(setpoint=setpoint, feedback=current_feedback, reset_hold=0, reset_val=0)
    duty_cycle = controller.output


    # Aggiorna il tempo corrente
    current_time += step_size

    # Salva l'ultimo stato del modello
    #last_state = mod.getSolutions("finalState", resultfile=result_file)
    #print(f"finalstate= {last_state}")

    # Variabili di stato da mantenere tra le simulazioni
    #state_variables = mod.getSolutions()
    
print("Simulazione completata con successo")
#print(f"Variables: {state_variables}")

    
# Plotta i risultati
plt.figure()
plt.subplot(2, 1, 1)
plt.plot(all_time, all_measured_value, label='Current Feedback')
plt.xlabel('Time (s)')
plt.ylabel('Current')
plt.legend()

plt.subplot(2, 1, 2)
plt.plot(all_time, all_duty_value, label='Duty Cycle')
plt.xlabel('Time (s)')
plt.ylabel('Duty Cycle')
plt.legend()

plt.title('Simulation Results')
plt.grid(True)
plt.show()