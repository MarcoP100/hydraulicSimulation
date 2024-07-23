from OMPython import OMCSessionZMQ, ModelicaSystem
import matplotlib.pyplot as plt
import os
import shutil
import numpy as np


# Inizializza la sessione OMC
omc = OMCSessionZMQ()

omc.sendExpression("setCommandLineOptions('-d=initialization')")

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
number_of_intervals = 1000
method = 'dassl'


# Simula il modello con parametri personalizzati
#sim_flags = f"-startTime={start_time} -stopTime={stop_time} -numberOfIntervals={number_of_intervals} -method={method}"
try:
    simflags = "-override=startTime=0,stopTime=10,stepSize=0.001,method=dassl"
    mod.simulate(simflags=simflags)

    print("Simulazione completata con successo")
except Exception as e:
    print(f"Errore durante la simulazione: {e}")

# Ottieni i nomi delle variabili e i risultati della simulazione
try:
    variables = mod.getSolutions()
    print(f"Variables: {variables}")
except Exception as e:
    print(f"Errore nella lettura delle variabili: {e}")

# Estrai i dati di una specifica variabile
try:
    time = np.array(mod.getSolutions("time"))
    variable_name = 'currentFeedback'  # Sostituisci con il nome della variabile che vuoi graficare
    variable_data = np.array(mod.getSolutions(variable_name))
    #print(f"Lentime: {len(time)}")
    #print(f"Lencurrent: {len(variable_data)}")
    # Verifica che gli array abbiano la stessa lunghezza
    #if len(time) != len(variable_data):
    #    raise ValueError("Gli array 'time' e 'variable_data' non hanno la stessa lunghezza.")

    #print("Valori grezzi di 'time':", time)
    #print("Valori grezzi di 'currentFeedback':", variable_data)

    # Verifica la struttura degli array
    if len(time.shape) > 1:
        print("time è un array multidimensionale con forma:", time.shape)
        time = time.flatten()  # Appiattisci l'array se necessario
    if len(variable_data.shape) > 1:
        print("currentFeedback è un array multidimensionale con forma:", variable_data.shape)
        variable_data = variable_data.flatten()  # Appiattisci l'array se necessario

    # Verifica che gli array abbiano la stessa lunghezza
    #if len(time) != len(variable_data):
    #    raise ValueError("Gli array 'time' e 'variable_data' non hanno la stessa lunghezza.")

  
    # Disabilita l'abbreviazione degli array
    #np.set_printoptions(threshold=np.inf)

    # Stampa i primi e gli ultimi 10 valori di 'time' e 'currentFeedback'
    #print("Valori di 'time' e 'currentFeedback':")
    #for t, v in zip(time, variable_data):
    #    print(f"{t}, {v} \n")
    
    # Ripristina l'impostazione predefinita
    #np.set_printoptions(threshold=1000)

     # Verifica i valori minimi e massimi
    print(f"Minimo e massimo di 'time': {time.min()}, {time.max()}")
    print(f"Minimo e massimo di 'currentFeedback': {variable_data.min()}, {variable_data.max()}")

    
    # Plotta i risultati
    plt.figure()
    plt.plot(time, variable_data)
    plt.xlabel('Time')
    plt.ylabel(variable_name)
    plt.title('Simulation Results')
    plt.grid(True)
    plt.show()
except Exception as e:
    print(f"Errore durante l'estrazione dei dati: {e}")