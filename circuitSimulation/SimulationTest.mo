model SimulationTest
//parameter Real dt_control = 0.02; // 20 ms
  //parameter Real dt_model = 0.01;  // 1 ms
  //parameter Real time_end = 5.0;    // 5 seconds of simulation
  parameter Real setpoint = 400.0;  // Setpoint for the PID controller
  parameter Real initial_duty_cycle = 0.0; // Initial duty cycle
  
  Real dutyCycle(start=initial_duty_cycle);
  Real feedback(start=0);
  //Real current_time(start=0);
  
  PIDController controller(
                            fw_gain=100,
                            p_gain=1000,
                            i_gain=10000,
                            //d_gain=0,
                            output_min=1000,
                            output_max=40000);
                            
                            
                            
   // Parametri del solenoide
  parameter Real L = 0.1 "Induttanza in Henry";
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

  //Real dutyCycle; // variabile input
  

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
    duty = dutyCycle / 65535
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
  feedback = solenoid.i_mA;  

  //when time >= next_control_time then
  controller.setpoint = setpoint;
   controller.feedback = feedback;
   // controller.reset_hold = 0;
   // controller.reset_val = 0;
    
   // next_control_time = next_control_time + dt_control;
  //end when;
    dutyCycle = controller.outputPid;
end SimulationTest;