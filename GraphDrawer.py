import pandas as pd
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import (QMainWindow, QWidget, QListWidget, QListWidgetItem,
                             QVBoxLayout, QHBoxLayout, QFileDialog, QAbstractItemView)
from PyQt5.QtCore import QSettings, Qt
from CustomWidgets import custom_widgets as CW

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 500, 800)
        self.setWindowTitle("Graph Drawer")

        self.column_names = []
        self.configurations = QSettings("GD", "GraphDrawer")

        self.init_UI()

    def init_UI(self):
        main_layout = QVBoxLayout()
        file_select_layout = QHBoxLayout()
        self.axis_dependant_layout = QVBoxLayout()

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        program_name = CW.create_label("Graph Drawer", text_size=25)
        main_layout.addWidget(program_name, alignment=Qt.AlignCenter)

        selected_file_text = CW.create_label("Selected File:")
        file_select_layout.addWidget(selected_file_text)
        self.selected_file_name = CW.create_label("No file selected")
        file_select_layout.addWidget(self.selected_file_name)
        choose_file_button = CW.create_button("Choose File")
        choose_file_button.clicked.connect(self.choose_file_clicked)
        file_select_layout.addWidget(choose_file_button)

        main_layout.addLayout(file_select_layout)

        self.graph_title = CW.create_line_edit("Graph Title..")
        main_layout.addWidget(self.graph_title)

        self.x_axis_title = CW.create_line_edit("X axis Title...")
        main_layout.addWidget(self.x_axis_title)

        self.axis_type_combo = CW.create_combo_box(["Single y axis", "Dual y axis"])
        self.axis_type_combo.currentIndexChanged.connect(self.handle_axis_type_change)
        main_layout.addWidget(self.axis_type_combo)

        main_layout.addLayout(self.axis_dependant_layout)

        self.handle_single_axis_selection()

        plot_button = CW.create_button("PLOT", "black", "lime")
        plot_button.clicked.connect(self.handle_plot_button_click)
        main_layout.addWidget(plot_button)

    def choose_file_clicked(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open File", "", "CSV Files (*.csv)"
        )
        if file_path:
            self.selected_file_name.setText(file_path)
            selected_file = pd.read_csv(file_path, delimiter=',', decimal = '.', encoding='utf-8')
            self.column_names = list(selected_file.columns)

            self.populate_items_list()

            if self.axis_type_combo.currentIndex() == 0:
                self.load_single_axis_selection()
            else:
                self.load_dual_axis_selection()

    def handle_axis_type_change(self, index):
        if index == 0:
            self.handle_single_axis_selection()
            self.populate_items_list()
            self.load_single_axis_selection()
        else:
            self.handle_dual_axis_selection()
            self.populate_items_list()
            self.load_dual_axis_selection()

    def handle_single_axis_selection(self):
        '''Change layout when single axis is selected'''
        CW.clear_layout(self.axis_dependant_layout)
        self.left_y_items_list = QListWidget()
        self.left_y_items_list.setSelectionMode(QAbstractItemView.MultiSelection)
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
        self.left_y_items_list.setSelectionMode(QAbstractItemView.MultiSelection)
        self.left_y_axis_label_line_edit = CW.create_line_edit("Left y axis label..")
        left_axis_layout.addWidget(self.left_y_items_list)
        left_axis_layout.addWidget(self.left_y_axis_label_line_edit)

        self.right_y_items_list = QListWidget()
        self.right_y_items_list.setSelectionMode(QAbstractItemView.MultiSelection)
        self.right_y_axis_label_line_edit = CW.create_line_edit("Right y axis label..")
        right_axis_layout.addWidget(self.right_y_items_list)
        right_axis_layout.addWidget(self.right_y_axis_label_line_edit)

        dual_axis_layout.addLayout(left_axis_layout)
        dual_axis_layout.addLayout(right_axis_layout)

        self.axis_dependant_layout.addLayout(dual_axis_layout)

    def populate_items_list(self):
        self.left_y_items_list.clear()
        if hasattr(self, 'right_y_items_list'):
            self.right_y_items_list.clear()

        for header in self.column_names:
            item = QListWidgetItem(header)
            self.left_y_items_list.addItem(item)

            if "Dual" in self.axis_type_combo.currentText():
                right_item = QListWidgetItem(header)
                self.right_y_items_list.addItem(right_item)

    def handle_plot_button_click(self):
        '''Plotting feature'''
        file_data = pd.read_csv(self.selected_file_name.text(), delimiter=',', decimal= '.', encoding= 'utf-8')

        fig, ax1 = plt.subplots()
        
        # Default color list; needed so that in dual axis the colors don't reapet
        color_cycle = plt.rcParams['axes.prop_cycle'].by_key()['color']
        used_colors = []

        x_data = [x for x in range(len(file_data))] # x_axis data

        if self.axis_type_combo.currentText() == "Single y axis":
            selected_items = self.left_y_items_list.selectedIndexes()
            selected_columns = [item.data() for item in selected_items]

            for idx in selected_columns:
                y_data = file_data[idx]

                ax1.plot(x_data, y_data, label=idx)

            ax1.set_xlabel(self.x_axis_title.text())
            ax1.set_ylabel(self.left_y_axis_label_line_edit.text())
            ax1.legend(loc= 'upper left')

        else:  # Dual y axis
            selected_left = [item.data() for item in self.left_y_items_list.selectedIndexes()]
            selected_right = [item.data() for item in self.right_y_items_list.selectedIndexes()]
            ax2 = ax1.twinx()

            for i, idx in enumerate(selected_left):
                y_data = file_data[idx]
                color = color_cycle[i % len(color_cycle)]
                used_colors.append(color)

                ax1.plot(x_data, y_data, label=idx, color=color)

            # Prepare colors for right axis by skipping used ones
            unused_colors = [c for c in color_cycle if c not in used_colors]
            
            for j, idx in enumerate(selected_right):
                y_data = file_data[idx]

                # Fallback to color cycle if we run out
                color = unused_colors[j % len(unused_colors)] if j < len(unused_colors) else color_cycle[(len(used_colors) + j) % len(color_cycle)]
                
                ax2.plot(x_data, y_data, label=idx, color= color)

            ax1.set_xlabel(self.x_axis_title.text())
            ax1.set_ylabel(self.left_y_axis_label_line_edit.text())
            ax2.set_ylabel(self.right_y_axis_label_line_edit.text())
            ax1.legend(loc= 'upper left')
            ax2.legend(loc= 'upper right')

        fig.suptitle(self.graph_title.text())
        plt.show()

    def save_single_axis_selection(self):
        selected_texts = [item.text() for item in self.left_y_items_list.selectedItems()]
        self.configurations.setValue("SingleSelections", selected_texts)
        self.configurations.setValue("SingleLeftAxisLabel", self.left_y_axis_label_line_edit.text())

    def load_single_axis_selection(self):
        label_text = self.configurations.value("SingleLeftAxisLabel", "")
        self.left_y_axis_label_line_edit.setText(label_text)

        selected_texts = self.configurations.value("SingleSelections", [])
        if isinstance(selected_texts, str):
            selected_texts = [selected_texts]

        for i in range(self.left_y_items_list.count()):
            item = self.left_y_items_list.item(i)
            if item.text() in selected_texts:
                item.setSelected(True)

    def save_dual_axis_selection(self):
        left_selected = [item.text() for item in self.left_y_items_list.selectedItems()]
        right_selected = [item.text() for item in self.right_y_items_list.selectedItems()]

        self.configurations.setValue("LeftAxisSelections", left_selected)
        self.configurations.setValue("LeftAxisLabel", self.left_y_axis_label_line_edit.text())
        self.configurations.setValue("RightAxisSelections", right_selected)
        self.configurations.setValue("RightAxisLabel", self.right_y_axis_label_line_edit.text())

    def load_dual_axis_selection(self):
        left_label = self.configurations.value("LeftAxisLabel", "")
        right_label = self.configurations.value("RightAxisLabel", "")
        self.left_y_axis_label_line_edit.setText(left_label)
        self.right_y_axis_label_line_edit.setText(right_label)

        left_selected_texts = self.configurations.value("LeftAxisSelections", [])
        right_selected_texts = self.configurations.value("RightAxisSelections", [])

        if isinstance(left_selected_texts, str):
            left_selected_texts = [left_selected_texts]
        if isinstance(right_selected_texts, str):
            right_selected_texts = [right_selected_texts]

        for i in range(self.left_y_items_list.count()):
            item = self.left_y_items_list.item(i)
            if item.text() in left_selected_texts:
                item.setSelected(True)

        for i in range(self.right_y_items_list.count()):
            item = self.right_y_items_list.item(i)
            if item.text() in right_selected_texts:
                item.setSelected(True)

    def closeEvent(self, event):
        event.accept()