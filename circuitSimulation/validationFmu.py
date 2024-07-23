from fmpy import validate_fmu

fmu_path = 'Simulation.fmu'
validation_result = validate_fmu(fmu_path)

print(validation_result)
