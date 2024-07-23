model SimFmu
  
   
   Real Output_mA;
  solenoidValveSim_me_FMU solenoidValveSim_me_FMU1 annotation(
    Placement(transformation(origin = {-22, 2}, extent = {{-10, -10}, {10, 10}})));
equation
  // Imposta un duty cycle fisso
  solenoidValveSim_me_FMU1.dutyCycle = 20000;
  Output_mA = solenoidValveSim_me_FMU1.currentFeedback;
end SimFmu;