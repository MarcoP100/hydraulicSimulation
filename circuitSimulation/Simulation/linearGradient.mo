within Simulation;
model linearGradient
  input Real startTime "Tempo di inizio della rampa";
  input Real endTime "Tempo di fine della rampa";
  input Real startValue "Valore iniziale della rampa";
  input Real endValue "Valore finale della rampa";
  
  output Real ramp "Segnale rampa";
  
equation
  // Definizione della rampa
  ramp = if time < startTime then startValue 
         else if time > endTime then endValue 
         else startValue + (endValue - startValue) * (time - startTime) / (endTime - startTime);
  
end linearGradient;
