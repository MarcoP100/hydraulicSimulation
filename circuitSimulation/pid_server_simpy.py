import simpy
import zmq
import json
from pidController import PidController

def pid_control(env, pid, socket):
    setpointCurrent_mA = 