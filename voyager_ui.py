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

# === Controls ===
    def start_animation(self): self.timer.start(200)
    def stop_animation(self): self.timer.stop()
    def reset_animation(self):
        self.plot_widget.current_index = 0
        self.plot_widget.plot_trajectory()

    def animate_voyager(self):
        self.plot_widget.move_forward()
        x, y, z = self.plot_widget.get_current_position()
        for e in VOYAGER_EVENTS:
            ex, ey, ez = e["coords"]
            dist = np.sqrt((x-ex)**2 + (y-ey)**2 + (z-ez)**2)
            if dist < 1e9:
                self.details_label.setText(
                    f"Year: {e['year']}\nEvent: {e['event']}\nPosition: ({x:.2e}, {y:.2e}, {z:.2e}) km"
                )
                return
        self.details_label.setText(f"Voyager position:\n({x:.2e}, {y:.2e}, {z:.2e}) km")


# === Search ===
    def search_year(self):
        year_text = self.search_input.text().strip()
        if not year_text.isdigit():
            QMessageBox.warning(self, "Invalid Input", "Please enter a valid year (numbers only).")
            return
        year = int(year_text)
        sorted_events = sorted(VOYAGER_EVENTS, key=lambda e: e["year"])
        years = [e["year"] for e in sorted_events]
        if year < years[0] or year > years[-1]:
            QMessageBox.information(self, "No Data", f"No data available for year {year}.")
            return

        for i in range(len(sorted_events)-1):
            y0, y1 = sorted_events[i]["year"], sorted_events[i+1]["year"]
            if y0 <= year <= y1:
                coords0 = np.array(sorted_events[i]["coords"])
                coords1 = np.array(sorted_events[i+1]["coords"])
                t = (year - y0)/(y1 - y0)
                pos = coords0 + t*(coords1 - coords0)
                event_before = sorted_events[i]["event"]
                event_after = sorted_events[i+1]["event"]
                break

        self.plot_widget.show_event(pos)
        QMessageBox.information(
            self,
            f"Voyager Position - {year}",
            f"Approximate Position for {year}:\n"
            f"X: {pos[0]:.2e} km\n"
            f"Y: {pos[1]:.2e} km\n"
            f"Z: {pos[2]:.2e} km\n\n"
            f"Between events:\n- {y0}: {event_before}\n- {y1}: {event_after}"
        )

    # === Event click ===
    def event_selected(self, item):
        text = item.text()
        year = int(text.split(" - ")[0])
        for e in VOYAGER_EVENTS:
            if e["year"] == year:
                self.plot_widget.show_event(e["coords"])
                self.details_label.setText(
                    f"Year: {e['year']}\nEvent: {e['event']}\nPosition: {e['coords']}"
                )
                break

    # === View change ===
    def change_view(self):
        mode = "3D" if self.view_selector.currentText()=="3D View" else "2D"
        self.plot_widget.set_mode(mode)