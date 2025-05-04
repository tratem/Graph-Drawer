import csv
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
            with open(file_path, newline='', encoding='utf-8') as csvfile:
                selected_file = csv.reader(csvfile)
                self.column_names = next(selected_file)

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
        data = []

        if self.selected_file_name.text() != "No file selected":
            with open(self.selected_file_name.text(), newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                next(reader)  # Skip header
                for row in reader:
                    data.append(row)

        if not data:
            return

        # Transpose rows to columns
        columns_data = list(zip(*data))

        # Convert columns to numeric where possible
        numeric_columns = []
        for col in columns_data:
            try:
                numeric_columns.append([int(value) for value in col])
            except ValueError:
                numeric_columns.append(col)  # Keep non-numeric columns

        fig, ax1 = plt.subplots()

        x_data = list(range(1, len(numeric_columns[0]) + 1)) # x_axis data

        if self.axis_type_combo.currentText() == "Single y axis":
            selected_items = self.left_y_items_list.selectedIndexes()
            selected_columns = [item.row() for item in selected_items]

            for idx in selected_columns:
                y_data = numeric_columns[idx]

                ax1.plot(x_data, y_data, label=self.column_names[idx])

            ax1.set_ylabel(self.left_y_axis_label_line_edit.text())
            ax1.set_xlabel(self.x_axis_title.text())

        else:  # Dual y axis
            selected_left = [item.row() for item in self.left_y_items_list.selectedIndexes()]
            selected_right = [item.row() for item in self.right_y_items_list.selectedIndexes()]

            ax2 = ax1.twinx()

            for idx in selected_left:
                y_data = numeric_columns[idx]

                ax1.plot(x_data, y_data, label=self.column_names[idx])

            for idx in selected_right:
                y_data = numeric_columns[idx]

                ax2.plot(x_data, y_data, label=self.column_names[idx])

            ax1.set_ylabel(self.left_y_axis_label_line_edit.text())
            ax2.set_ylabel(self.right_y_axis_label_line_edit.text())
            ax1.set_xlabel(self.x_axis_title.text())

        fig.suptitle(self.graph_title.text())
        fig.legend()
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