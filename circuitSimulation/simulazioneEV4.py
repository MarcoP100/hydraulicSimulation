import os
import matplotlib
matplotlib.use('TkAgg')  # Usa il backend TkAgg per l'output grafico
import numpy as np
from fmpy import simulate_fmu, extract, read_model_description
from fmpy.fmi2 import FMU2Slave
import matplotlib.pyplot as plt
from pidController import PidController

plt.ioff()  # Disabilita la modalità interattiva

# Parametri 
start_time = 0.0
dt_control = 0.02  # 20 ms
dt_model = 0.000005  # 0.1 ms

# Path al file FMU esportato da Modelica
fmu_path = 'Simulation.fmu'

unzipdir = os.path.abspath('extracted_fmu')  # Percorso assoluto

# Estrai il contenuto dell'FMU
extract(fmu_path, unzipdir=unzipdir)

# Leggi la descrizione del modello
model_description = read_model_description(unzipdir)

# Instanzia l'FMU
fmu_instance = FMU2Slave(guid=model_description.guid,
                    unzipDirectory=unzipdir,
                    modelIdentifier=model_description.coSimulation.modelIdentifier,
                    instanceName='instance1'
                    )


# Abilita il logging dettagliato
fmu_instance.instantiate(loggingOn=False)
fmu_instance.setupExperiment(startTime=start_time)
fmu_instance.enterInitializationMode()
fmu_instance.exitInitializationMode()

# Log per la simulazione
fmu_instance.setDebugLogging(False, categories=['logAll'])

# Trova il valueReference per le variabili specifiche
def get_value_reference(variable_name):
    for variable in model_description.modelVariables:
        if variable.name == variable_name:
            return variable.valueReference
    raise ValueError(f"Variable '{variable_name}' not found in the model description.")

# Ottieni i riferimenti delle variabili
current_feedback_ref = get_value_reference('currentFeedback')
duty_cycle_ref = get_value_reference('dutyCycle')

Lout_ref = get_value_reference('Lout')
Rout_ref = get_value_reference('Rout')
Tempout_ref = get_value_reference('Tempout')
Vout_ref = get_value_reference('Vout')
freqOut_ref = get_value_reference('freqOut')
dutyUsed_ref = get_value_reference('dutyUsed')



time_data = []
current_feedback_data  = []
duty_cycle_data  = []

#Lout_data = []
#Rout_data = []
#Tempout_data = []
#Vout_data = []
#freqOut_data = []
#dutyUsed_data = []

# Inizializza il controllore PID
controller = PidController(fw_gain=1000,
                               p_gain=100,
                               i_gain=1000,
                               d_gain=0,
                               output_max=40000,
                               output_min=0)
duty_cycle = 0.0  # Inizializza il duty cycle

# Simula il sistema con il controllore
current_time = start_time
time_end = 30  # 10 secondi di simulazione

# Apri un file di log
log_file = open('simulation_log.txt', 'w')

while current_time < time_end:
    if current_time % dt_control < dt_model:
        if current_time > 0:
            current_feedback = fmu_instance.getReal([current_feedback_ref])[0]
            #print(f"DEBUG: Current feedback at time {current_time}: {current_feedback}")
            #log_file.write(f"DEBUG: Current feedback at time {current_time}: {current_feedback}\n")
       
        else:
            current_feedback = 0.0
        
        controller.update(setpoint=400, feedback=current_feedback, reset_hold=0, reset_val=0)
        duty_cycle = controller.output
        
        #time_data.append(current_time)
        #current_feedback_data.append(current_feedback)
        #duty_cycle_data.append(duty_cycle)
        
        #log_file.write(f"Time: {current_time}, Feedback: {current_feedback}, Duty Cycle: {duty_cycle}\n")
        #print(f"Time: {current_time}, Feedback: {current_feedback}, Duty Cycle: {duty_cycle}")

    fmu_instance.setReal([duty_cycle_ref], [duty_cycle])
    fmu_instance.doStep(currentCommunicationPoint=current_time, communicationStepSize=dt_model)
    current_feedback_value = fmu_instance.getReal([current_feedback_ref])
    #Lout = fmu_instance.getReal([Lout_ref])
    #Rout = fmu_instance.getReal([Rout_ref])
    #Tempout = fmu_instance.getReal([Tempout_ref])
    #Vout = fmu_instance.getReal([Vout_ref])
    #freqOut = fmu_instance.getReal([freqOut_ref])
    #dutyUsed = fmu_instance.getReal([dutyUsed_ref])
    # Salva i dati
    time_data.append(current_time)
    current_feedback_data.append(current_feedback_value)
    duty_cycle_data.append(duty_cycle)
    #Lout_data.append(Lout)
    #Rout_data.append(Rout)
    #Tempout_data.append(Tempout)
    #Vout_data.append(Vout)
    #freqOut_data.append(freqOut)
    #dutyUsed_data.append(dutyUsed)

    #duty_cycle_data.append(duty_cycle)  # Se vuoi graficare anche il duty cycle

    # Debugging: stampa dei valori attuali
    #print(f"Time: {current_time}, Lout_data: {Lout}")
    
    current_time += dt_model

# Cleanup
fmu_instance.terminate()
fmu_instance.freeInstance()

# Verifica la raccolta dei dati
#log_file.write("Lunghezza dei dati raccolti:\n")
#log_file.write(f"Time: {len(time_data)}\n")
#log_file.write(f"Current Feedback: {len(current_feedback_data)}\n")
#log_file.write(f"Duty Cycle: {len(duty_cycle_data)}\n")

# Plot dei risultati
#try:
#if time_data and current_feedback_data:
plt.figure()
plt.subplot(2, 1, 1)
plt.plot(time_data, current_feedback_data, label='Current Feedback')
plt.xlabel('Time (s)')
plt.ylabel('Current')
plt.legend()

plt.subplot(2, 1, 2)
plt.plot(time_data, duty_cycle_data, label='Duty Cycle')
plt.xlabel('Time (s)')
plt.ylabel('Duty Cycle')
plt.legend()
#plt.savefig("duty_cycle_plot.png")  # Salva il grafico come immagine

#plt.subplot(3, 1, 3)
#plt.plot(time_data, Vout_data, label='Vout_data')
#plt.xlabel('Time (s)')
#plt.ylabel('Vout_data')

plt.legend()

#plt.savefig("current_feedback_plot.png")  # Salva il grafico come immagine

       # plt.subplot(2, 1, 2)
       # plt.plot(time_data, duty_cycle_data, label='Duty Cycle')
       # plt.xlabel('Time (s)')
       # plt.ylabel('Duty Cycle')
       # plt.legend()
       # plt.savefig("duty_cycle_plot.png")  # Salva il grafico come immagine

plt.show()
    #else:
    #    log_file.write(f"Errore durante la visualizzazione dei grafici: {e}\n")
    
#except Exception as e:
 #   log_file.write(f"Utilizzo della memoria alla fine: {memory_usage()} bytes\n")
 #   log_file.close()
    