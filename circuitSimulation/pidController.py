class PidController:
    def __init__(   self, 
                    fw_gain,
                    p_gain,
                    i_gain,
                    d_gain,
                    output_min,
                    output_max):

       # parametri ingresso 
        self.fw_gain = fw_gain
        self.p_gain = p_gain
        self.i_gain = i_gain
        self.d_gain = d_gain
        self.output_min = output_min
        self.output_max = output_max

        # variabili uscita
        self.output = 0
        self.control_error = 0
        self.integrator = 0

        # variabili 
        

    def update(self, 
               setpoint, 
               feedback,
               reset_hold,
               reset_val):
        
        previous_error = self.control_error
        self.control_error = setpoint - feedback

        # Sum of errors for integral term 
        if reset_hold == 1:
            self.integrator = reset_val
        elif reset_hold != 2:
            self.integrator = self.integrator + (self.i_gain * self.control_error)
        
        # Calculate new output (with scaling of gains). The following formula is used:
        # out := kff * set_point + kp * error + kd * d(error) + ki * s(error)

        feed_forward_component = (self.fw_gain * setpoint) / 1000
        proportional_component = (self.p_gain * self.control_error) / 1000
        differential_component = (self.d_gain * (self.control_error - previous_error)) / 10000
        integral_component = self.integrator / 10000

        self.output = feed_forward_component + proportional_component + differential_component + integral_component

        # Limit output to min/max values 
        if self.output < self.output_min:
            if reset_hold != 2:
                self.integrator = max(self.integrator, self.integrator - (self.i_gain * self.control_error))
            self.output = self.output_min
        
        if self.output > self.output_max:
            if reset_hold != 2:
                self.integrator = min(self.integrator, self.integrator - (self.i_gain * self.control_error))
            self.output = self.output_max
        
        return self.output, self.control_error, self.integrator