model PIDController

  parameter Real fw_gain;
  parameter Real p_gain;
  parameter Real i_gain;
  //parameter Real d_gain;
  parameter Real output_min;
  parameter Real output_max;

  // Variabili di stato
  output Real outputPid(start=0);
  output Real control_error(start=0);
  Real integrator(start=0);

  // Ingressi
  input Real setpoint;
  input Real feedback;
  //input Integer reset_hold;
  //input Real reset_val;

protected
  //Real previous_error(start=0);
  Real feed_forward_component(start=0);
  Real proportional_component(start=0);
  //Real differential_component(start=0);
  Real integral_component(start=0);
  

equation 
  //previous_error = control_error;
  control_error = setpoint - feedback;

  // Somma degli errori per il termine integrale
  /*when reset_hold == 1 then
    integrator = reset_val;
  end when
  when reset_hold <> 2 then*/
  integrator = integrator + (i_gain * control_error);
  //end if;*/
  
  feed_forward_component = (fw_gain * setpoint) / 1000;
   proportional_component = (p_gain * control_error) / 1000;
   //differential_component := (d_gain * (control_error - previous_error)) / 10000;
   // integral_component = integrator / 10000;

        //outputPid = feed_forward_component + proportional_component + integral_component;*/

  outputPid = feed_forward_component + proportional_component;

  // Limita l'uscita ai valori min/max
/*  if outputPid < output_min then
    if reset_hold <> 2 then
      integrator := myMax(integrator, integrator - (i_gain * control_error));
    end if;
    outputPid := output_min;
  end if;
  
  if outputPid > output_max then
    if reset_hold <> 2 then
      integrator := myMin(integrator, integrator - (i_gain * control_error));
    end if;
    outputPid := output_max;
  end if;*/
end PIDController;