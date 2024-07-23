within Simulation;
model Simulation
  // Parametri del solenoide
  parameter Real L = 0.1 "Induttanza in Henry";
  parameter Real R_rif = 3 "Resistenza in Ohm";
  parameter Real Temp_rif = 20;
  parameter Real coeff = 4.3e-3;
  
  
  // Parametri del PWM
  parameter Real Vdc = 24 "Tensione di alimentazione in Volt";
  parameter Real freq = 200 "Frequenza del PWM in Hz";
    
  // parametri rampa temperatura
  parameter Real startSecond = 5 "Tempo di inizio della rampa";
  parameter Real endSecond = 60 "Tempo di fine della rampa";
  parameter Real startValue = 20 "Valore iniziale della rampa";
  parameter Real endValue = 130 "Valore finale della rampa";

  input Real dutyCycle; // variabile input
  output Real currentFeedback;  

  output Real Lout;
  output Real Rout;
  output Real Tempout;
  output Real Vout;
  output Real freqOut;
  output Real dutyUsed;

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
    duty = dutyCycle / 65535.0
  );

  linearGradient rampaTemperatura(
    startTime = startSecond,
    endTime = endSecond,
    startValue = startValue,
    endValue = endValue
  ); 
 
equation

  solenoid.Temp_act = rampaTemperatura.ramp;
  // Collegamento dell'uscita del PWM all'ingresso del solenoide
  solenoid.V_v = pwm.V_volt;
  currentFeedback = solenoid.i_mA;
  Lout = solenoid.L;
  Rout = solenoid.R_act;
  Tempout = solenoid.Temp_act;
  Vout = solenoid.V_v;
  freqOut = pwm.freq;
  dutyUsed = pwm.duty;
    
end Simulation;
