model solenoidPropValve
  // Parametri del solenoide
  input Real L "Induttanza in Henry";
  input Real R_rif "Resistenza in Ohm alla temp di riferimento";
  input Real Temp_rif " temperatura di riferimento in °C";
  input Real V_v "Tensione applicata (volt)";
  input Real coeff "coefficiente termico ";
  input Real Temp_act "temperatura attuale in °C";
  
  output Real i_mA "Corrente attraverso il solenoide (mA)";
   
  Real R_act "resistenza alla temperatura attuale in ohm ";
  Real i_A;
equation
  // calcolo resistenza 
  R_act = R_rif * (1 + coeff * (Temp_act - Temp_rif));
   
  // Equazione differenziale del circuito RL
  L * der(i_A) + R_act * i_A = V_v;
  
  i_mA = i_A * 1000;

end solenoidPropValve;