from OMPython import OMCSessionZMQ, ModelicaSystem
import matplotlib.pyplot as plt
import os
import shutil
import numpy as np

# Inizializza la sessione OMC
omc = OMCSessionZMQ()

# Verifica se OMC è in esecuzione
version = omc.sendExpression("getVersion()")
if not version:
    raise Exception("OpenModelica Compiler (OMC) non è in esecuzione. Assicurati che OMC sia installato e accessibile.")
else:
    print(f"OMC Version: {version}")

# Percorso al file package.mo
package_path = '/home/vncuser/circuitSimulation/Simulation/package.mo'
model_name = 'Simulation.Simulation'

# Carica il modello usando ModelicaSystem
try:
    mod = ModelicaSystem(package_path, model_name)
    print("Pacchetto caricato con successo")
except Exception as e:
    print(f"Errore nel caricamento del pacchetto: {e}")


# Elenco dei file .mo necessari per il modello
#model_files = [
#    'Simulation.mo',
#    'solenoidPropValve.mo',
#    'pwmGenerator.mo',
#    'linearGradient.mo'
#]

# Carica il modello base Modelica
#loadModelica = omc.sendExpression("loadModel(Modelica)")
#print(f"Caricamento modelica: {loadModelica}")

#load_result = omc.sendExpression(f"loadFile(\"Simulation.mo\")")
#print(f"Caricamento del file del modello : {load_result}")

#if load_result is None:
#    raise Exception(f"Errore nel caricamento del file del modello")
# Carica ciascun file .mo
#for model_file in model_files:
 #   if not os.path.exists(model_file):
  #      raise Exception(f"File del modello non trovato: {model_file}")
    
 #   load_result = omc.sendExpression(f'loadFile("{model_file}")')
  #  print(f"Caricamento del file del modello '{model_file}': {load_result}")

  #  if load_result is None:
 #       raise Exception(f"Errore nel caricamento del file del modello: {model_file}")

#model_name = 'Simulation'  
#instantiate_result = omc.sendExpression(f"instantiateModel({model_name})")
#if not instantiate_result:
#    raise Exception(f"Errore nell'istanziazione del modello: {model_name}")
#else:
 #   print(f"istanza modello: {instantiate_result}")
#mod = ModelicaSystem(model_files[0], model_name)  # Utilizza il primo file come modello principale


# Crea una directory di lavoro temporanea
#work_dir = 'simulation_output'
#if os.path.exists(work_dir):
#    shutil.rmtree(work_dir)
#os.makedirs(work_dir)

# Imposta la directory di lavoro in OMC
#omc.sendExpression(f"cd(\"{work_dir}\")")

# Istanzia il modello
#instantiate_result = omc.sendExpression(f"instantiateModel({model_name})")
#print(f"Istanziamento del modello: {instantiate_result}")

# Verifica il risultato dell'istanziamento
#if instantiate_result is None:
 #   raise Exception(f"Errore nell'istanziamento del modello: {model_name}")

# Imposta i parametri e simula
#simulate_result  = omc.sendExpression(f"simulate({model_name}, startTime=0,stopTime=10,numberOfIntervals=5000, method='dassl')")

#print(f"Risultato della simulazione: {simulate_result}")

# Verifica che il file di risultato esista
#result_file = os.path.join(work_dir, f"{model_name}_res.mat")
#if not os.path.exists(result_file):
#    raise Exception(f"File di risultato della simulazione non trovato: {result_file}")
#else:
#    print(f"File di risultato trovato: {result_file}")

# Esegui la simulazione
# Simula il modello

mod.buildModel()

# Parametri di simulazione
start_time = 0.0
stop_time = 10.0
number_of_intervals = 5000
method = 'dassl'

# Simula il modello con parametri personalizzati
#sim_flags = f"-startTime={start_time} -stopTime={stop_time} -numberOfIntervals={number_of_intervals} -method={method}"
try:
    mod.simulate()
    print("Simulazione completata con successo")
except Exception as e:
    print(f"Errore durante la simulazione: {e}")

time = []
current_feedback= []

# Ottieni i risultati della simulazione
time = mod.getSolutions("time")
 
current_feedback = mod.getSolutions("currentFeedback")  # Sostituisci 'currentFeedback' con il nome della variabile desiderata

# Stampa tutti i valori di 'time'
# Disabilita l'abbreviazione degli array
np.set_printoptions(threshold=np.inf)

    # Stampa tutti i valori di 'time'
print("Valori di 'current_feedback':")
print(current_feedback)

    # Ripristina l'impostazione predefinita
np.set_printoptions(threshold=1000)

solutions = mod.getSolutions()
#print(f"Variables: {solutions}")

# Recupera i risultati della simulazione
#time = omc.getResult(f"{model_name}.time")
#variable = omc.getResult(f"{model_name}.currentFeedback")  # Sostituisci 'variableName' con il nome della variabile che vuoi graficare
# Ottieni i nomi delle variabili e i risultati della simulazione
#variables = omc.sendExpression(f"readSimulationResultVars('{model_name}_res.mat')")
#print(f"Variables: {variables}")
#if variables is None:
 #   print("Errore: Non è stato possibile leggere le variabili dal file di risultato della simulazione.")
 #   print("Contenuto del file di risultato:")
 #   file_list = omc.sendExpression(f"list(fileName='{result_file}')")
 #   print(file_list)
#else:
    
 #   # Esempio: Estrai i dati di una specifica variabile
 #   time = omc.sendExpression(f"readSimulationResult('{model_name}_res.mat', 'time')")
  #  variable_name = 'currentFeedback'  # Sostituisci con il nome della variabile che vuoi graficare
  #  variable_data = omc.sendExpression(f"readSimulationResult('{model_name}_res.mat', '{variable_name}')")


# Plotta i risultati
plt.plot(time, current_feedback)
plt.xlabel('Time')
plt.ylabel('Variable')
plt.title('Simulation Results')
plt.grid(True)
plt.show()
