# --------------------------------------------------------------------------------
#   File        rc_servo_motor_control_view.py
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
import json
import os
import ast
import time
from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QGroupBox,
    QComboBox,
    QSlider,
    QRadioButton,
    QButtonGroup,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,    
)
from PySide6.QtCore import Qt

from .rc_servo_motor_control_model import RcServoMotor, RcServoMotorControlModel
from .interp import Interp

# --------------------------------------------------------------------------------
#   Class - RcServoMotorControlView
# --------------------------------------------------------------------------------
class RcServoMotorControlView(QWidget):
    def __init__(self, model):
        super().__init__()        
        self.model = model
        self.motor_cnt = model.get_motor_cnt()
        self.interp = Interp()
        self.is_tick = True
        self.is_slider_rotate = True
        self.pose_count = 1

        self.radio_buttons = []
        self.labels = []
        self.line_edits = []
        self.plus_buttons = []
        self.minus_buttons = []
        self.ok_buttons = []
        self.sliders = []

        self.init_ui()

        # Set slider range and value
        self.is_initialized = False
        if self.is_tick is True:
            for i in range(self.motor_cnt):            
                self.line_edits[i].setText(str(self.model.get_tick(i)))
                self.sliders[i].setRange(self.model.get_tick_min(i), self.model.get_tick_max(i))
                self.sliders[i].setValue(self.model.get_tick(i))
        else:
            for i in range(self.motor_cnt):
                self.line_edits[i].setText(str(self.model.get_angle(i)))
                self.sliders[i].setRange(self.model.get_angle_min(i), self.model.get_angle_max(i))
                self.sliders[i].setValue(self.model.get_angle(i))    
        self.is_initialized = True
    
    def init_ui(self):
        # ----------------------------------------
        # Set 'Setup' and 'Motor' layout
        # ----------------------------------------
        setup_motor_layout = QVBoxLayout()
        
        # Set 'Setup' GroupBox
        setup_layout = QVBoxLayout()

        setup_port_layout = QHBoxLayout()
        setup_port_label = QLabel('Port')
        self.setup_port_combo_box = QComboBox()
        self.setup_port_combo_box.addItems(['COM' + str(i) for i in range(1, 10)])
        self.setup_port_combo_box.setCurrentText('COM5')
        setup_port_layout.addWidget(setup_port_label)
        setup_port_layout.addWidget(self.setup_port_combo_box)
        setup_layout.addLayout(setup_port_layout)

        setup_connect_disconnect_layout = QHBoxLayout()
        self.setup_connect_button = QPushButton('Connect')
        self.setup_disconnect_button = QPushButton('Disconnect')
        setup_connect_disconnect_layout.addWidget(self.setup_connect_button)
        setup_connect_disconnect_layout.addWidget(self.setup_disconnect_button)
        setup_layout.addLayout(setup_connect_disconnect_layout)        
        self.setup_connect_button.clicked.connect(self.on_setup_connect_clicked)
        self.setup_disconnect_button.clicked.connect(self.on_setup_disconnect_clicked)

        setup_init_step_layout = QHBoxLayout()
        self.setup_init_button = QPushButton('Init')
        setup_step_layout = QHBoxLayout()
        setup_step_label = QLabel('Step')
        self.action_step_size_line_edit = QLineEdit()
        self.action_step_size_line_edit.setText('2')
        self.action_step_size_line_edit.setFixedWidth(50)
        setup_step_layout.addStretch(1)
        setup_step_layout.addWidget(setup_step_label)
        setup_step_layout.addWidget(self.action_step_size_line_edit)
        setup_init_step_layout.addWidget(self.setup_init_button, 1)
        setup_init_step_layout.addLayout(setup_step_layout, 1)
        setup_layout.addLayout(setup_init_step_layout)        
        self.setup_init_button.clicked.connect(self.on_setup_init_clicked)  

        setup_motor_data_layout = QHBoxLayout()
        self.radio_buttons.append(QRadioButton('Tick'))
        self.radio_buttons.append(QRadioButton('Angle'))
        
        if self.is_tick is True:
            self.radio_buttons[0].setChecked(True)
        else:
            self.radio_buttons[1].setChecked(True)
            
        self.radio_button_group = QButtonGroup(self)
        self.radio_button_group.addButton(self.radio_buttons[0])
        self.radio_button_group.addButton(self.radio_buttons[1])
        setup_motor_data_layout.addWidget(self.radio_buttons[0])
        setup_motor_data_layout.addWidget(self.radio_buttons[1])        
        setup_layout.addLayout(setup_motor_data_layout)   
        self.radio_buttons[0].clicked.connect(lambda _, idx=0: self.on_setup_radio_clicked(idx))
        self.radio_buttons[1].clicked.connect(lambda _, idx=1: self.on_setup_radio_clicked(idx))    

        setup_group_box = QGroupBox('Setup')        
        setup_group_box.setLayout(setup_layout)
        adjusted_width = int(setup_group_box.sizeHint().width() * 2.0)
        setup_group_box.setFixedWidth(adjusted_width)
        setup_group_box.setFixedHeight(150)        
        setup_motor_layout.addWidget(setup_group_box)        

        # Set 'Motor' GroupBox
        for i in range(1, self.motor_cnt + 1):            
            motor_group_box = QGroupBox(f'Motor {i}')
            motor_group_box.setFixedWidth(adjusted_width)
            motor_group_box.setFixedHeight(100)            
            motor_layout = QVBoxLayout()

            motor_data_layout = QHBoxLayout()
            if self.is_tick is True:
                label = QLabel('Tick')
            else:
                label = QLabel('Angle')
            line_edit = QLineEdit()
            line_edit.setText('0')
            plus_button = QPushButton('▲')
            minus_button = QPushButton('▼')
            ok_button = QPushButton('OK')
            
            motor_data_layout.addWidget(label)
            motor_data_layout.addWidget(line_edit)
            motor_data_layout.addWidget(plus_button)
            motor_data_layout.addWidget(minus_button)
            motor_data_layout.addWidget(ok_button)
            
            slider = QSlider(Qt.Horizontal)
            slider.setRange(0, 0)
            slider.setValue(0)
            
            motor_layout.addLayout(motor_data_layout)
            motor_layout.addWidget(slider)

            motor_group_box.setLayout(motor_layout)
            setup_motor_layout.addWidget(motor_group_box)

            self.labels.append(label)
            self.line_edits.append(line_edit)
            self.plus_buttons.append(plus_button)
            self.minus_buttons.append(minus_button)
            self.ok_buttons.append(ok_button)
            self.sliders.append(slider)

            plus_button.clicked.connect(lambda _, idx=i-1: self.on_motor_up_clicked(idx))
            minus_button.clicked.connect(lambda _, idx=i-1: self.on_motor_down_clicked(idx))
            ok_button.clicked.connect(lambda _, idx=i-1: self.on_motor_ok_clicked(idx))            
            slider.valueChanged.connect(lambda value, idx=i-1: self.on_motor_slider_value_changed(idx, value))
        
        setup_motor_layout.addStretch(1)
        
        # ----------------------------------------
        # Set 'Pose' and 'Action' layout
        # ----------------------------------------
        pose_action_layout = QVBoxLayout()
        
        # Set 'Pose' GroupBox        
        pose_layout = QVBoxLayout()

        pose_name_layout = QHBoxLayout()
        name_label = QLabel('Name')
        self.pose_name_line_edit = QLineEdit()
        self.pose_name_line_edit.setText(f'Pose{self.pose_count}')
        self.add_pose_button = QPushButton('Add')
        pose_name_layout.addWidget(name_label)
        pose_name_layout.addWidget(self.pose_name_line_edit)
        pose_name_layout.addWidget(self.add_pose_button)        
        pose_layout.addLayout(pose_name_layout)

        self.pose_table_widget = QTableWidget()
        self.pose_table_widget.setColumnCount(2)
        self.pose_table_widget.setHorizontalHeaderLabels(['Name', 'Data'])
        self.pose_table_widget.horizontalHeader().setStretchLastSection(True)
        self.pose_table_widget.setColumnWidth(0, 100)
        pose_layout.addWidget(self.pose_table_widget)

        pose_do_add_to_action_layout = QHBoxLayout()
        self.do_button = QPushButton('Do')
        self.add_to_action_button = QPushButton('Add to Action')
        pose_do_add_to_action_layout.addWidget(self.do_button)
        pose_do_add_to_action_layout.addWidget(self.add_to_action_button)
        pose_layout.addLayout(pose_do_add_to_action_layout)
        
        pose_save_load_clear_layout = QHBoxLayout()
        self.pose_save_button = QPushButton('Save')
        self.pose_load_button = QPushButton('Load')
        self.pose_clear_button = QPushButton('Clear')
        pose_save_load_clear_layout.addWidget(self.pose_save_button)
        pose_save_load_clear_layout.addWidget(self.pose_load_button)
        pose_save_load_clear_layout.addWidget(self.pose_clear_button)
        pose_layout.addLayout(pose_save_load_clear_layout)
        
        self.pose_group_box = QGroupBox('Pose')
        self.pose_group_box.setLayout(pose_layout)
        self.pose_group_box.setFixedWidth(adjusted_width)

        self.add_pose_button.clicked.connect(self.on_pose_add_clicked)
        self.do_button.clicked.connect(self.on_pose_do_clicked)
        self.add_to_action_button.clicked.connect(self.on_pose_add_to_action_clicked)
        self.pose_save_button.clicked.connect(self.on_pose_save_clicked)
        self.pose_load_button.clicked.connect(self.on_pose_load_clicked)
        self.pose_clear_button.clicked.connect(self.on_pose_clear_clicked)

        # Set 'Action' GroupBox        
        action_layout = QVBoxLayout()
        
        action_step_interval_layout = QHBoxLayout()
        action_step_label = QLabel('Step')
        self.action_step_line_edit = QLineEdit()
        self.action_step_line_edit.setText('5')
        action_interval_label = QLabel('Interval [sec]')
        self.action_interval_line_edit = QLineEdit()
        self.action_interval_line_edit.setText('0.02')
        action_step_interval_layout.addWidget(action_step_label)
        action_step_interval_layout.addWidget(self.action_step_line_edit)
        action_step_interval_layout.addWidget(action_interval_label)
        action_step_interval_layout.addWidget(self.action_interval_line_edit)    
        action_layout.addLayout(action_step_interval_layout)
        
        self.action_table_widget = QTableWidget()
        self.action_table_widget.setColumnCount(2)
        self.action_table_widget.setHorizontalHeaderLabels(['Name', 'Data'])
        self.action_table_widget.setColumnWidth(0, 100)
        self.action_table_widget.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        action_layout.addWidget(self.action_table_widget)

        action_run_stop_layout = QHBoxLayout()
        self.action_run_button = QPushButton('Run')
        self.action_stop_button = QPushButton('Stop')
        action_run_stop_layout.addWidget(self.action_run_button)
        action_run_stop_layout.addWidget(self.action_stop_button)
        action_layout.addLayout(action_run_stop_layout)
        
        action_up_down_remove_layout = QHBoxLayout()
        self.action_up_button = QPushButton('▲')
        self.action_down_button = QPushButton('▼')
        self.action_remove_button = QPushButton('Remove')
        action_up_down_remove_layout.addWidget(self.action_up_button)
        action_up_down_remove_layout.addWidget(self.action_down_button)
        action_up_down_remove_layout.addWidget(self.action_remove_button)
        action_layout.addLayout(action_up_down_remove_layout)
        
        action_pose_save_load_clear_layout = QHBoxLayout()
        self.action_save_button = QPushButton('Save')
        self.action_load_button = QPushButton('Load')
        self.action_clear_button = QPushButton('Clear')
        action_pose_save_load_clear_layout.addWidget(self.action_save_button)
        action_pose_save_load_clear_layout.addWidget(self.action_load_button)
        action_pose_save_load_clear_layout.addWidget(self.action_clear_button)
        action_layout.addLayout(action_pose_save_load_clear_layout)
        
        self.action_group_box = QGroupBox('Action')
        self.action_group_box.setLayout(action_layout)
        self.action_group_box.setFixedWidth(adjusted_width)

        self.action_run_button.clicked.connect(self.on_action_run_clicked)
        self.action_stop_button.clicked.connect(self.on_action_stop_clicked)
        self.action_up_button.clicked.connect(self.on_action_up_clicked)
        self.action_down_button.clicked.connect(self.on_action_down_clicked)
        self.action_remove_button.clicked.connect(self.on_action_remove_clicked)
        self.action_save_button.clicked.connect(self.on_action_save_clicked)
        self.action_load_button.clicked.connect(self.on_action_load_clicked)
        self.action_clear_button.clicked.connect(self.on_action_clear_clicked)
                
        pose_action_layout.addWidget(self.pose_group_box)
        pose_action_layout.addWidget(self.action_group_box)
        pose_action_layout.addStretch(1)
  
        # ----------------------------------------
        # Set root layout
        # ----------------------------------------
        root_layout = QHBoxLayout()
        root_layout.addLayout(setup_motor_layout)
        root_layout.addLayout(pose_action_layout)
        self.setLayout(root_layout)

    # ----------------------------------------
    # 'Setup' event
    # ----------------------------------------
    def on_setup_connect_clicked(self):
        print('Connect')
        selected_port = self.setup_port_combo_box.currentText()
        self.model.connect(selected_port, 115200)  
        
    def on_setup_disconnect_clicked(self):
        print('Disconnect')
        self.model.disconnect()  

    def on_setup_init_clicked(self):
        print("Init")
        if self.is_tick is True:
            for i in range(self.motor_cnt):
                self.line_edits[i].setText(str(self.model.get_tick_init(i)))
                self.sliders[i].setValue(self.model.get_tick_init(i))
        else:
            for i in range(self.motor_cnt):
                self.line_edits[i].setText(str(self.model.get_angle_init(i)))
                self.sliders[i].setValue(self.model.get_angle_init(i))
        self.model.rotate()
        
    def on_setup_radio_clicked(self, index):    
        is_tick_pre = self.is_tick
        
        # Update current slider value 
        if self.is_tick is True:
            for i in range(self.motor_cnt):
                self.model.set_tick(i, self.sliders[i].value())
        else:
            for i in range(self.motor_cnt):
                self.model.set_angle(i, self.sliders[i].value())
        
        # Set tick/angle type
        if index == 0:
            self.is_tick = True
        else:
            self.is_tick = False

        # Set slider range and value
        self.is_initialized = False
        if self.is_tick is True:
            for i in range(self.motor_cnt):
                self.labels[i].setText('Tick')
                self.line_edits[i].setText(str(self.model.get_tick(i)))
                self.sliders[i].setRange(self.model.get_tick_min(i), self.model.get_tick_max(i))
                self.sliders[i].setValue(self.model.get_tick(i))
        else:
            for i in range(self.motor_cnt):
                self.labels[i].setText('Angle')
                self.line_edits[i].setText(str(self.model.get_angle(i)))
                self.sliders[i].setRange(self.model.get_angle_min(i), self.model.get_angle_max(i))
                self.sliders[i].setValue(self.model.get_angle(i))    
        self.is_initialized = True

        # Set 'Pose' tick/angle value
        if self.is_tick is True and is_tick_pre is False:
            for row in range(self.pose_table_widget.rowCount()):
                data = ast.literal_eval(self.pose_table_widget.item(row, 1).text())
                data_new = []
                for i in range(len(data)):
                    data_new.append(self.model.convert_angle_to_tick(i, data[i]))
                self.pose_table_widget.setItem(row, 1, QTableWidgetItem(str(data_new)))
        elif self.is_tick is False and is_tick_pre is True:
            for row in range(self.pose_table_widget.rowCount()):
                data = ast.literal_eval(self.pose_table_widget.item(row, 1).text())
                data_new = []
                for i in range(len(data)):
                    data_new.append(self.model.convert_tick_to_angle(i, data[i]))
                self.pose_table_widget.setItem(row, 1, QTableWidgetItem(str(data_new)))
        else:
            pass

        # Set 'Action' tick/angle value
        if self.is_tick is True and is_tick_pre is False:
            for row in range(self.action_table_widget.rowCount()):
                data = ast.literal_eval(self.action_table_widget.item(row, 1).text())
                data_new = []
                for i in range(len(data)):
                    data_new.append(self.model.convert_angle_to_tick(i, data[i]))
                self.action_table_widget.setItem(row, 1, QTableWidgetItem(str(data_new)))
        elif self.is_tick is False and is_tick_pre is True:
            for row in range(self.action_table_widget.rowCount()):
                data = ast.literal_eval(self.action_table_widget.item(row, 1).text())
                data_new = []
                for i in range(len(data)):
                    data_new.append(self.model.convert_tick_to_angle(i, data[i]))
                self.action_table_widget.setItem(row, 1, QTableWidgetItem(str(data_new)))
        else:
            pass
          
        # Set 'Action' step and interval value
        if self.is_tick is True:
            self.action_step_line_edit.setText('5')
        else:
            self.action_step_line_edit.setText('1')

    # ----------------------------------------
    # 'Motor' event
    # ----------------------------------------        
    def on_motor_up_clicked(self, index):
        print('Motor' + str(index + 1)  + ' Up')
        value = int(self.line_edits[index].text())
        value = value + int(self.action_step_size_line_edit.text())        
        if self.is_tick is True:            
            self.model.set_tick(index, value)
        else:
            self.model.set_angle(index, value)           
        self.line_edits[index].setText(str(value))
        self.sliders[index].setValue(value)

    def on_motor_down_clicked(self, index):
        print('Motor' + str(index + 1)  + ' Down')
        value = int(self.line_edits[index].text())
        value = value - int(self.action_step_size_line_edit.text())
        if self.is_tick is True:
            self.model.set_tick(index, value)
        else:
            self.model.set_angle(index, value)             
        self.line_edits[index].setText(str(value))
        self.sliders[index].setValue(value)

    def on_motor_ok_clicked(self, index):
        print('Motor' + str(index + 1)  + ' OK')
        value = int(self.line_edits[index].text())   
        if self.is_tick is True:
            self.model.set_tick(index, value)
        else:
            self.model.set_angle(index, value)             
        self.sliders[index].setValue(value)

    def on_motor_slider_value_changed(self, index, value):        
        if self.is_initialized is True:
            print('Motor' + str(index + 1)  + ' Slider Value = ' + str(value))         
            self.line_edits[index].setText(str(value))    
            if self.is_tick is True:
                self.model.set_tick(index, value)
            else:
                self.model.set_angle(index, value)
            
            if self.is_slider_rotate is True:
                self.model.rotate()
      
    # ----------------------------------------
    # 'Pose' event
    # ----------------------------------------
    def on_pose_add_clicked(self):
        print('Pose Add')
        pose_name = self.pose_name_line_edit.text().strip()
        if pose_name:
            value = [slider.value() for slider in self.sliders]
            pose_data = str(value)

            row = self.pose_table_widget.rowCount()
            self.pose_table_widget.insertRow(row)
            self.pose_table_widget.setItem(row, 0, QTableWidgetItem(pose_name))
            self.pose_table_widget.setItem(row, 1, QTableWidgetItem(pose_data))

            self.pose_count += 1
            self.pose_name_line_edit.setText(f"Pose{self.pose_count}")

    def on_pose_do_clicked(self):
        print('Pose Do')
        selected_items = self.pose_table_widget.selectedItems()
        if not selected_items:
            print('Pose Do - No item selected')
            return

        row = selected_items[0].row()        
        data = json.loads(self.pose_table_widget.item(row, 1).text())  
       
        self.is_slider_rotate = False
        for index, value in enumerate(data):
            self.sliders[index].setValue(value)        
        if self.is_tick is True:
            self.model.set_ticks(data)
        else:
            self.model.set_angles(data)
        self.model.rotate()
        self.is_slider_rotate = True

    def on_pose_add_to_action_clicked(self):
        print('Pose Add to Action')
        selected_items = list(set(item.row() for item in self.pose_table_widget.selectedItems()))
        if not selected_items:
            print('Pose Add to Action - No item selected')
            return

        for row in selected_items:
            name = self.pose_table_widget.item(row, 0)
            data = self.pose_table_widget.item(row, 1)
            if name and data:
                row_position = self.action_table_widget.rowCount()
                self.action_table_widget.insertRow(row_position)
                self.action_table_widget.setItem(row_position, 0, QTableWidgetItem(name.text()))
                self.action_table_widget.setItem(row_position, 1, QTableWidgetItem(data.text()))
        
    def on_pose_save_clicked(self):
        print('Pose Save')
        poses = []
        poses.append({'is_tick': self.is_tick})
        for row in range(self.pose_table_widget.rowCount()):
            name = self.pose_table_widget.item(row, 0)
            data = self.pose_table_widget.item(row, 1)
            if name and data:
                poses.append({
                    'name': name.text(),
                    'data': data.text()
                })        
        try:
            with open('Pose.json', 'w', encoding='utf-8') as f:
                json.dump(poses, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Pose Save Error - {e}")

    def on_pose_load_clicked(self):
        print('Pose Load')
        if not os.path.exists('Pose.json'):
            print('Pose.json File Not Found')
            return

        try:
            with open('Pose.json', 'r', encoding='utf-8') as f:
                poses = json.load(f)  
            if len(poses) < 2:
                print('Pose.json File Error')
                return                
            self.pose_table_widget.setRowCount(0)
            self.pose_count = 1

            if self.is_tick is True and poses[0]['is_tick'] is False:
                for pose in poses[1:]:
                    row = self.pose_table_widget.rowCount()
                    self.pose_table_widget.insertRow(row)
                    self.pose_table_widget.setItem(row, 0, QTableWidgetItem(pose['name']))                    
                    data = ast.literal_eval(pose['data'])
                    data_new = []
                    for i in range(len(data)):
                        data_new.append(self.model.convert_angle_to_tick(i, data[i]))
                    self.pose_table_widget.setItem(row, 1, QTableWidgetItem(str(data_new)))                    
                    self.pose_count = self.pose_count + 1
                self.pose_name_line_edit.setText(f"Pose{self.pose_count}")            
                
            elif self.is_tick is False and poses[0]['is_tick'] is True:
                for pose in poses[1:]:
                    row = self.pose_table_widget.rowCount()
                    self.pose_table_widget.insertRow(row)
                    self.pose_table_widget.setItem(row, 0, QTableWidgetItem(pose['name']))                    
                    data = ast.literal_eval(pose['data'])
                    data_new = []
                    for i in range(len(data)):
                        data_new.append(self.model.convert_tick_to_angle(i, data[i]))
                    self.pose_table_widget.setItem(row, 1, QTableWidgetItem(str(data_new)))                    
                    self.pose_count = self.pose_count + 1
                self.pose_name_line_edit.setText(f"Pose{self.pose_count}")  
            
            else:
                for pose in poses[1:]:
                    row = self.pose_table_widget.rowCount()
                    self.pose_table_widget.insertRow(row)
                    self.pose_table_widget.setItem(row, 0, QTableWidgetItem(pose['name']))           
                    self.pose_table_widget.setItem(row, 1, QTableWidgetItem(pose['data']))           
                    self.pose_count = self.pose_count + 1
                self.pose_name_line_edit.setText(f"Pose{self.pose_count}") 

        except Exception as e:
            print(f'Pose Load Error - {e}')
      
    def on_pose_clear_clicked(self):
        print('Pose Clear')
        self.pose_table_widget.setRowCount(0)
        self.pose_count = 1
        self.pose_name_line_edit.setText(f"Pose{self.pose_count}")        
        
    # ----------------------------------------
    # 'Action' event
    # ----------------------------------------
    def on_action_run_clicked(self):
        print('Action Run')
        if self.action_table_widget.rowCount() < 2:
            print('Action Run - At least 2 Pose need')
            return        

        step = int(self.action_step_line_edit.text())
        interval = float(self.action_interval_line_edit.text())
        
        # Set motor data
        pose_list = []
        for row in range(self.action_table_widget.rowCount()):
            data = ast.literal_eval(self.action_table_widget.item(row, 1).text())
            pose_list.append(data)        
        data_list = self.interp.get_interp_lists(pose_list, step)

        # Rotate motor
        self.is_slider_rotate = False
        for i in range(len(data_list)):
            data = data_list[i]    
            for index, value in enumerate(data):
                self.sliders[index].setValue(value)      
            if self.is_tick is True:
                self.model.set_ticks(data)
            else:
                self.model.set_angles(data)
            self.model.rotate()
            time.sleep(interval)
        self.is_slider_rotate = True

    def on_action_stop_clicked(self):
        print('Action Stop')
        
    def on_action_up_clicked(self):
        print('Action Up')
        selected_rows = sorted(list(set(item.row() for item in self.action_table_widget.selectedItems())))
        if not selected_rows:
            print('Action Up - No item selected')
            return

        for row in selected_rows:
            if row > 0:
                current_row_data = [self.action_table_widget.item(row, col).text() for col in range(self.action_table_widget.columnCount())]                
                self.action_table_widget.insertRow(row - 1)                
                for col, data in enumerate(current_row_data):
                    self.action_table_widget.setItem(row - 1, col, QTableWidgetItem(data))                
                self.action_table_widget.removeRow(row + 1)                
                self.action_table_widget.selectRow(row - 1)

    def on_action_down_clicked(self):
        print('Action Down')
        selected_rows = sorted(list(set(item.row() for item in self.action_table_widget.selectedItems())), reverse=True)
        if not selected_rows:
            print('Action Down - No item selected')
            return

        for row in selected_rows:
            if row < self.action_table_widget.rowCount() - 1:
                current_row_data = [self.action_table_widget.item(row, col).text() for col in range(self.action_table_widget.columnCount())]                
                self.action_table_widget.insertRow(row + 2)                
                for col, data in enumerate(current_row_data):
                    self.action_table_widget.setItem(row + 2, col, QTableWidgetItem(data))                
                self.action_table_widget.removeRow(row)
                self.action_table_widget.selectRow(row + 1)

    def on_action_remove_clicked(self):
        print('Action Remove')
        selected_rows = sorted(list(set(item.row() for item in self.action_table_widget.selectedItems())), reverse=True)
        if not selected_rows:
            print('Action Remove - No item selected')
            return
        
        for row in selected_rows:
            self.action_table_widget.removeRow(row)

    def on_action_save_clicked(self):
        print('Action Save')
        actions = []
        actions.append({'is_tick': self.is_tick})
        for row in range(self.action_table_widget.rowCount()):
            name = self.action_table_widget.item(row, 0)
            data = self.action_table_widget.item(row, 1)
            if name and data:
                actions.append({
                    'name': name.text(),
                    'data': data.text(),
                })

        try:
            with open('Action.json', 'w', encoding='utf-8') as f:
                json.dump(actions, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f'Action Save Error - {e}')

    def on_action_load_clicked(self):
        print('Action Load')
        if not os.path.exists('Action.json'):
            print('Action.json file not found')
            return
            
        try:
            with open('Action.json', 'r', encoding='utf-8') as f:
                actions = json.load(f)
            if len(actions) < 2:
                print('Action.json File Error')
                return                 
            self.action_table_widget.setRowCount(0)

            if self.is_tick is True and actions[0]['is_tick'] is False:
                for action in actions[1:]:
                    row = self.action_table_widget.rowCount()
                    self.action_table_widget.insertRow(row)
                    self.action_table_widget.setItem(row, 0, QTableWidgetItem(action['name']))                    
                    data = ast.literal_eval(action['data'])
                    data_new = []
                    for i in range(len(data)):
                        data_new.append(self.model.convert_angle_to_tick(i, data[i]))
                    self.action_table_widget.setItem(row, 1, QTableWidgetItem(str(data_new)))                    

            elif self.is_tick is False and actions[0]['is_tick'] is True:
                for action in actions[1:]:
                    row = self.action_table_widget.rowCount()
                    self.action_table_widget.insertRow(row)
                    self.action_table_widget.setItem(row, 0, QTableWidgetItem(action['name']))                    
                    data = ast.literal_eval(action['data'])
                    data_new = []
                    for i in range(len(data)):
                        data_new.append(self.model.convert_tick_to_angle(i, data[i]))
                    self.action_table_widget.setItem(row, 1, QTableWidgetItem(str(data_new)))                    
            else:
                for action in actions[1:]:
                    row = self.action_table_widget.rowCount()
                    self.action_table_widget.insertRow(row)
                    self.action_table_widget.setItem(row, 0, QTableWidgetItem(action['name']))
                    self.action_table_widget.setItem(row, 1, QTableWidgetItem(action['data']))                  

        except Exception as e:
            print(f'Action Load Error - {e}')
        
    def on_action_clear_clicked(self):
        print('Action Clear')
        self.action_table_widget.setRowCount(0)
        