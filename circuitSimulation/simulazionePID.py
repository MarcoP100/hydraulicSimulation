import simpy
import matplotlib.pyplot as plt
import mplcursors
from pidController import PidController
import zmq
import json

tempi = []
outputPid = []
current = []

def pidSimulation(env,
                  controller: PidController,
                  socket):
    
    
    while True:
        #riceve feedback da modelica
        message = socket.recv_json()
        feedbackCurrent = message['feedback']

        controller.update(setpoint=400,
                          feedback=feedbackCurrent,
                          reset_hold=0,
                          reset_val=0)
        
        # Invia l'output del pid a modelica
        socket.send_json({'control_output': controller.output})

        tempi.append(env.now)
        outputPid.append(controller.output)
        current.append(feedbackCurrent)

        yield env.timeout(sampleTime)


if __name__ == '__main__':

    sampleTime = 0.02
    simulationSec = 1000

    #configura  ZeroMQ
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5555")
    

    env = simpy.Environment()

    #inizilizzo controllore
    controller = PidController(fw_gain=100,
                               p_gain=1000,
                               i_gain=10000,
                               d_gain=0,
                               output_max=40000,
                               output_min=1000)
    
    env.process(pidSimulation(env, controller=controller))

    #avvio simulazione
    env.run(until=simulationSec)

    # Debug: stampa i dati raccolti
    formatted_tempi = ", ".join([f"{p:.1f}" if p is not None else "None" for p in tempi])
    print("Tempi:", formatted_tempi)
    
    formatted_output = ", ".join([f"{p:.1f}" if p is not None else "None" for p in outputPid])
    print("outputPid:", formatted_output)

    formatted_current = ", ".join([f"{p:.1f}" if p is not None else "None" for p in current])
    print("feedback current_mA:", formatted_current)


    # Plot dei risultati
    fig, axs = plt.subplots(2, 1, figsize=(12, 6), sharex=True)  # due subplot verticali

    axs[0].plot(tempi, outputPid, label='uscita pid', linestyle='-', color='b', marker='.')
    axs[0].set_xlabel('Tempo')
    axs[0].set_ylabel('duty cycle')
    axs[0].legend()
    punti_handle0 = axs[0].scatter(tempi, outputPid, color='red', marker='.', label='Punti specifici')
    mplcursors.cursor(punti_handle0, hover=True).connect("add", lambda sel: sel.annotation.set_text(f'({sel.target[0]:.2f}, {sel.target[1]:.2f})'))
    
    axs[1].plot(tempi, current, label='Feedback current', linestyle='-', color='g', marker='.')
    axs[1].set_xlabel('Tempo')
    axs[1].set_ylabel('current')
    axs[1].legend()
    punti_handle1 = axs[1].scatter(tempi, current, color='red', marker='.', label='Punti specifici')
    mplcursors.cursor(punti_handle0, hover=True).connect("add", lambda sel: sel.annotation.set_text(f'({sel.target[0]:.2f}, {sel.target[1]:.2f})'))


    plt.tight_layout()
    plt.grid(True)
    plt.show()