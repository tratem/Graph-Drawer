import csv
import sys
from PyQt5.QtWidgets import (QMainWindow, QWidget, QListWidget, QListWidgetItem,
                             QVBoxLayout, QHBoxLayout, QFileDialog)
from PyQt5.QtCore import QSettings, Qt
from CustomWidgets import custom_widgets as CW

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 500, 800)
        self.setWindowTitle("Graph Drawer")
        self.init_UI()

    def init_UI(self):
        main_layout = QVBoxLayout()
        file_select_layout = QHBoxLayout() # selected file and select file button
        self.axis_dependant_layout = QVBoxLayout() # content change dependant on axis_type_combo selection

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        program_name = CW.create_label("Graph Drawer", text_size=25)
        main_layout.addWidget(program_name, alignment= Qt.AlignCenter)

        selected_file_text = CW.create_label("Selected File:")
        file_select_layout.addWidget(selected_file_text)
        self.selected_file = CW.create_label("No file selected")
        file_select_layout.addWidget(self.selected_file)
        choose_file_button = CW.create_button("Choose File")
        choose_file_button.clicked.connect(self.choose_file_clicked)
        file_select_layout.addWidget(choose_file_button)

        main_layout.addLayout(file_select_layout)

        graph_title = CW.create_line_edit("Graph Title..")
        main_layout.addWidget(graph_title)

        x_axis_title = CW.create_line_edit("X axis Title...")
        main_layout.addWidget(x_axis_title)

        axis_type_combo = CW.create_combo_box(["Single y axis", "Dual y axis"])
        axis_type_combo.currentIndexChanged.connect(self.handle_axis_type_change)
        self.handle_single_axis_selection() #Set single as initial config
        main_layout.addWidget(axis_type_combo)

        main_layout.addLayout(self.axis_dependant_layout)

        plot_button = CW.create_button("PLOT", "black", "lime")
        plot_button.clicked.connect(self.handle_plot_button_click)
        main_layout.addWidget(plot_button)

    def choose_file_clicked(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Open File", "", "(*.csv)"
        )
        if file_name:
            self.selected_file.setText(f"{file_name}")
        
        
    
    def handle_axis_type_change(self, index):
        if index == 0:
            self.handle_single_axis_selection()
        else:
            self.handle_dual_axis_selection()

    def handle_single_axis_selection(self):
        '''Change layout when single axis is selected'''
        CW.clear_layout(self.axis_dependant_layout)
        self.left_y_items_list = QListWidget()
        self.left_y_axis_label_line_edit = CW.create_line_edit("Left y axis label..")
        self.axis_dependant_layout.addWidget(self.left_y_items_list)
        self.axis_dependant_layout.addWidget(self.left_y_axis_label_line_edit)

    def handle_dual_axis_selection(self):
        '''Change layout when dual axis is selected'''
        CW.clear_layout(self.axis_dependant_layout)
        dual_axis_layout = QHBoxLayout()
        left_axis_layout = QVBoxLayout()
        right_axis_layout = QVBoxLayout()

        self.left_y_items_list = QListWidget()
        self.left_y_axis_label_line_edit = CW.create_line_edit("Left y axis label..")
        left_axis_layout.addWidget(self.left_y_items_list)
        left_axis_layout.addWidget(self.left_y_axis_label_line_edit)

        
        self.right_y_items_list = QListWidget()
        self.right_y_axis_label_line_edit = CW.create_line_edit("Right y axis label..")
        right_axis_layout.addWidget(self.right_y_items_list)
        right_axis_layout.addWidget(self.right_y_axis_label_line_edit)

        dual_axis_layout.addLayout(left_axis_layout)
        dual_axis_layout.addLayout(right_axis_layout)

        self.axis_dependant_layout.addLayout(dual_axis_layout)

    def handle_plot_button_click(self):
        '''Show Figure'''
