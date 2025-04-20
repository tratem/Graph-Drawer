import csv
import sys
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout
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
        self.axis_type_layout = QVBoxLayout() # content change dependant on axis_type_combo selection

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

        main_layout.addLayout(self.axis_type_layout)

        plot_button = CW.create_button("PLOT", "black", "lime")
        plot_button.clicked.connect(self.handle_plot_button_click)
        main_layout.addWidget(plot_button)

    def choose_file_clicked(self):
        pass
    
    def handle_axis_type_change(self, index):
        if index == 0:
            self.handle_single_axis_selection()
        else:
            self.handle_dual_axis_selection()

    def handle_single_axis_selection(self):
        pass

    def handle_dual_axis_selection(self):
        pass

    def handle_plot_button_click(self):
        pass
