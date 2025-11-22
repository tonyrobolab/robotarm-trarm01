# --------------------------------------------------------------------------------
#   File        rc_servo_motor_control_model.py
#
#   Version     v0.1  2025.11.05  Tony Kwon
#                   Initial revision
#
#               v0.2  2025.11.07  Tony Kwon
#                   Add tick and angle setup functions
#
#               v0.3  2025.11.13  Tony Kwon
#                   Add set_ticks() and set_angles() functions
#                   Add convert_angle_to_tick() and convert_tick_to_angle()
#                       functions
# --------------------------------------------------------------------------------

# --------------------------------------------------------------------------------
#   Import
# --------------------------------------------------------------------------------
import numpy as np
from .serial_comm import SerialComm

# --------------------------------------------------------------------------------
#   Class - RcServoMotor
# --------------------------------------------------------------------------------
class RcServoMotor:
    def __init__(self, ticks, angles):
        self.tick = ticks[0]
        self.tick_init = ticks[0]
        self.tick_min = ticks[1]
        self.tick_max = ticks[2]
        self.tick_min_max = np.array([self.tick_min, self.tick_max])
        
        self.angle = angles[0]
        self.angle_init = angles[0]
        self.angle_min = angles[1]
        self.angle_max = angles[2]
        self.angle_min_max = np.array([self.angle_min, self.angle_max])

    def set_tick(self, tick):
        self.tick = min(max(tick, self.tick_min), self.tick_max)
        self.angle = int(np.interp(tick, self.tick_min_max, self.angle_min_max))

    def get_tick(self):
        return self.tick

    def get_tick_init(self):
        return self.tick_init

    def get_tick_min(self):
        return self.tick_min

    def get_tick_max(self):
        return self.tick_max

    def set_angle(self, angle):
        self.angle = min(max(angle, self.angle_min), self.angle_max)
        self.tick = int(np.interp(angle, self.angle_min_max, self.tick_min_max))

    def get_angle(self):
        return self.angle

    def get_angle_init(self):
        return self.angle_init

    def get_angle_min(self):
        return self.angle_min

    def get_angle_max(self):
        return self.angle_max

    def convert_angle_to_tick(self, angle):
        angle = min(max(angle, self.angle_min), self.angle_max)
        tick = int(np.interp(angle, self.angle_min_max, self.tick_min_max))
        return tick

    def convert_tick_to_angle(self, tick):
        tick = min(max(tick, self.tick_min), self.tick_max)
        angle = int(np.interp(tick, self.tick_min_max, self.angle_min_max))
        return angle        

# --------------------------------------------------------------------------------
#   Class - RcServoMotorControlModel
# --------------------------------------------------------------------------------
class RcServoMotorControlModel:
    def __init__(self):
        # Comm        
        self.comm = SerialComm()
        self.connected = False

        # Motors
        self.motors = []        

    def add_motor(self, motor):
        self.motors.append(motor)

    def get_motor_cnt(self):
        return len(self.motors)
        
    def connect(self, port, baud):
        if self.comm.init(port, baud):
            self.connected = True
        else:
            self.connected = False

    def disconnect(self):
        self.comm.deinit()
        self.connected = False

    def set_tick(self, index, tick):
        self.motors[index].set_tick(tick)
    
    def set_ticks(self, ticks):
        for index in range(len(ticks)):
            self.motors[index].set_tick(ticks[index])

    def get_tick(self, index):
        return self.motors[index].get_tick()       

    def get_tick_init(self, index):
        return self.motors[index].get_tick_init() 

    def get_tick_min(self, index):
        return self.motors[index].get_tick_min()

    def get_tick_max(self, index):
        return self.motors[index].get_tick_max()

    def set_angle(self, index, angle):
        self.motors[index].set_angle(angle)

    def set_angles(self, angles):
        for index in range(len(angles)):
            self.motors[index].set_angle(angles[index])

    def get_angle(self, index):
        return self.motors[index].get_angle()  

    def get_angle_init(self, index):
        return self.motors[index].get_angle_init() 

    def get_angle_min(self, index):
        return self.motors[index].get_angle_min()

    def get_angle_max(self, index):
        return self.motors[index].get_angle_max()

    def convert_angle_to_tick(self, index, angle):
        return self.motors[index].convert_angle_to_tick(angle)

    def convert_tick_to_angle(self, index, tick):
        return self.motors[index].convert_tick_to_angle(tick)

    def rotate(self):
        # Set comm data
        data = [0xFF, 0xFF, len(self.motors)]
        for motor in self.motors:
            data.append(0xFF & (motor.tick >> 8))
            data.append(0xFF & motor.tick)

        print(data)

        # TX comm data
        if self.connected:
            self.comm.write(data)


