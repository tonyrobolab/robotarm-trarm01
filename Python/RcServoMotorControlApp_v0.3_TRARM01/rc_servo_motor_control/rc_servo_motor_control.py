# --------------------------------------------------------------------------------
#   File        rc_servo_motor_control.py
#
#   Version     v0.1  2025.11.05  Tony Kwon
#                   Initial revision
#
#               v0.2  2025.11.07  Tony Kwon
#                   Add angle configurations
#               v0.3  2025.11.13  Tony Kwon
#                   Set window fixed size
# --------------------------------------------------------------------------------

# --------------------------------------------------------------------------------
#   Import
# --------------------------------------------------------------------------------
import sys
from PySide6.QtWidgets import QMainWindow

from .rc_servo_motor_control_model import RcServoMotor, RcServoMotorControlModel
from .rc_servo_motor_control_view import RcServoMotorControlView

# --------------------------------------------------------------------------------
#   Class - RcServoMotorControl
# --------------------------------------------------------------------------------
class RcServoMotorControl(QMainWindow):
    def __init__(self, motor_cnt, motor_ticks, motor_angles):     
        super().__init__()
        
        # Set model
        self.model = RcServoMotorControlModel()
        for i in range(motor_cnt):
            self.model.add_motor(RcServoMotor(motor_ticks[i], motor_angles[i]))

        # Set view
        self.view = RcServoMotorControlView(self.model)        
        
        # Set window
        self.setWindowTitle('RC Servo Motor Control')
        
        # Set main widget
        self.setCentralWidget(self.view)
        self.setFixedSize(self.view.sizeHint().width(), self.view.sizeHint().height())
        
    def get_view(self):
        return self.view

        
    