import numpy as np
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QListWidget, QLabel, QComboBox, QPushButton, QLineEdit, QMessageBox
)
from PyQt5.QtCore import QTimer
from voyager_plot import VoyagerPlot
from voyager_data import VOYAGER_EVENTS

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🚀 Voyager 1 Interactive Path Viewer")
        self.setMinimumSize(1000,600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QHBoxLayout()
        central_widget.setLayout(layout)

        #Left: plot
        self.plot_widget = VoyagerPlot(self)
        layout.addWidget(self.plot_widget, 2)

        # Right panel
        right_panel = QVBoxLayout()

        # View selector
        self.view_selector = QComboBox()
        self.view_selector.addItems(["3D View", "2D View"])
        self.view_selector.currentIndexChanged.connect(self.change_view)

        # Event list
        self.event_list = QListWidget()
        for e in VOYAGER_EVENTS:
            self.event_list.addItem(f"{e['year']} - {e['event']}")
        self.event_list.itemClicked.connect(self.event_selected)

        # Search
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Enter Year (e.g., 1990)")
        self.search_btn = QPushButton("🔍 Search Year")
        self.search_btn.clicked.connect(self.search_year)

        # Details
        self.details_label = QLabel("Voyager is moving...\nEvents update automatically.")
        self.details_label.setWordWrap(True)

        # Buttons
        self.start_btn = QPushButton("▶ Start")
        self.stop_btn = QPushButton("⏸ Pause")
        self.reset_btn = QPushButton("⏮ Reset")
        self.start_btn.clicked.connect(self.start_animation)
        self.stop_btn.clicked.connect(self.stop_animation)
        self.reset_btn.clicked.connect(self.reset_animation)

        # Layout right panel
        right_panel.addWidget(QLabel("View Mode:"))
        right_panel.addWidget(self.view_selector)
        right_panel.addWidget(QLabel("Mission Events:"))
        right_panel.addWidget(self.event_list)
        right_panel.addWidget(QLabel("Details:"))
        right_panel.addWidget(self.details_label)
        right_panel.addWidget(self.start_btn)
        right_panel.addWidget(self.stop_btn)
        right_panel.addWidget(self.reset_btn)
        right_panel.addWidget(QLabel("Search Voyager by Year:"))
        right_panel.addWidget(self.search_input)
        right_panel.addWidget(self.search_btn)
        right_panel.addStretch()
        layout.addLayout(right_panel, 1)

        # Timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.animate_voyager)
        self.timer.start(200)


