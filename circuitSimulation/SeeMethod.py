from OMPython import ModelicaSystem

# Inizializza il sistema Modelica
mod = ModelicaSystem("/path/to/your/model.mo", "ModelName")

# Elenca tutti i metodi e attributi disponibili
methods = dir(mod)
for method in methods:
    print(method)

# Ottieni informazioni dettagliate su un metodo specifico
help(mod.simulate)
