model pwmGenerator
  input Real Vdc "Tensione di alimentazione in Volt";
  input Real freq "Frequenza del PWM in Hz";
  input Real duty "Duty cycle del PWM (0-1)";
  
  output Real V_volt "Tensione generata";
  
  Real pwm_rif;
equation
  // Generazione del segnale PWM
  pwm_rif = if mod(time, 1/freq) < duty*(1/freq) then 1 else 0;
  V_volt = pwm_rif * Vdc;
  
end pwmGenerator;