model Simulation
  import Modelica_DeviceDrivers.Communication.TCPIPSocketClient;
  import Modelica.Blocks.Interfaces.RealOutput;
  import Modelica.Blocks.Sources.CombiTimeTable;
  
  parameter Integer port = 5555;
  parameter String ip = "127.0.0.1";
  
  Real feedback;
  Real control_output;
  Real updatedControlOutput(start=0);
  
  // Configurazione del client TCP/IP
  TCPIPClient tcpClient(port=port, ip=ip);
    
  // Parametri del solenoide
  parameter Real L = 0.075 "Induttanza in Henry";
  parameter Real R_rif = 3 "Resistenza in Ohm";
  parameter Real Temp_rif = 20;
  parameter Real coeff = 4.3e-3;
  
  
  // Parametri del PWM
  parameter Real Vdc = 24 "Tensione di alimentazione in Volt";
  parameter Real freq = 200 "Frequenza del PWM in Hz";
    
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
    freq = freq
  );

  linearGradient rampaTemperatura(
    startTime = startTime,
    endTime = endTime,
    startValue = startValue,
    endValue = endValue
  ); 
 
equation
  pwmGenerator.duty = control_output;
  solenoid.Temp_act = rampaTemperatura.ramp;
  // Collegamento dell'uscita del PWM all'ingresso del solenoide
  solenoid.V_v = pwm.V_volt;
    
end Simulation;
