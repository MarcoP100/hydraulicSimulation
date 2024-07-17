model Simulation
  // Parametri del solenoide
  parameter Real L = 0.1 "Induttanza in Henry";
  parameter Real R_rif = 3 "Resistenza in Ohm";
  parameter Real Temp_rif = 20;
  parameter Real coeff = 4.3e-3;
  
  
  // Parametri del PWM
  parameter Real Vdc = 24 "Tensione di alimentazione in Volt";
  parameter Real freq = 200 "Frequenza del PWM in Hz";
  parameter Real duty = 0.5 "Duty cycle del PWM (0-1)";
  
  // parametri rampa temperatura
  parameter Real startTime = 5 "Tempo di inizio della rampa";
  parameter Real endTime = 60 "Tempo di fine della rampa";
  parameter Real startValue = 20 "Valore iniziale della rampa";
  parameter Real endValue = 130 "Valore finale della rampa";

  // Istanze dei modelli
  solenoidPropValve solenoid(
    L = L,
    R_rif = R_rif,
    Temp_rif = Temp_rif,
    coeff = coeff
  );
  pwmGenerator pwm(
    Vdc = Vdc,
    freq = freq,
    duty = duty
  );

  linearGradient rampaTemperatura(
    startTime = startTime,
    endTime = endTime,
    startValue = startValue,
    endValue = endValue
  ); 
 
equation

  solenoid.Temp_act = rampaTemperatura.ramp;
  // Collegamento dell'uscita del PWM all'ingresso del solenoide
  solenoid.V_v = pwm.V_volt;
    
end Simulation;
