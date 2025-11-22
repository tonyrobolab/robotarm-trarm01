# --------------------------------------------------------------------------------
#   File        rc_servo_motor_control_app.py
#
#   Version     v0.1  2025.11.05  Tony Kwon
#                   Initial revision
#
#               v0.2  2025.11.07  Tony Kwon
#                   Add tick and angle setup functions
#
#               v0.3  2025.11.13  Tony Kwon
#                   Add pose and action control functions
# --------------------------------------------------------------------------------

# --------------------------------------------------------------------------------
#   Import
# --------------------------------------------------------------------------------
import sys
from PySide6.QtWidgets import (
    QApplication,
)
from rc_servo_motor_control.rc_servo_motor_control import RcServoMotorControl

# --------------------------------------------------------------------------------
#   Run
# --------------------------------------------------------------------------------
if __name__ == '__main__':
    # Set configuration data
    motor_cnt = 3
    motor_ticks = [
        #Init   Min     Max
        [244,   134,    354],
        [312,   202,    422],
        [306,   196,    416]
    ]
    motor_angles = [
        #Init   Min     Max
        [0,     -45,    45],
        [0,     -45,    45],
        [0,     -45,    45]
    ]

    # Init application
    app = QApplication(sys.argv)
    control = RcServoMotorControl(motor_cnt, motor_ticks, motor_angles)
    control.show()
    sys.exit(app.exec())
