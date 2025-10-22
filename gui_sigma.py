import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QGridLayout, QLabel, QComboBox, 
                             QSpinBox, QPushButton, QListWidget, QTextEdit,
                             QMessageBox, QGroupBox, QListWidgetItem)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QIcon  

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

import progresive_enriched_end0

class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=8, height=8, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        super(MplCanvas, self).__init__(self.fig)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.graph = progresive_enriched_end0.create_bandung_culinary_graph()
        self.locations = sorted(list(self.graph.nodes()))

        self.setWindowTitle("Perencana Tur Kuliner Bandung")
        self.setGeometry(100, 100, 1400, 800)
        self.setWindowIcon(QIcon("AppsLogo.png"))  

        main_layout = QHBoxLayout()

        controls_panel = self._create_controls_panel()
        main_layout.addWidget(controls_panel, 1)

        display_panel = self._create_display_panel()
        main_layout.addWidget(display_panel, 2) 

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        try:
            with open("styles.qss", "r") as f:
                self.setStyleSheet(f.read())
        except FileNotFoundError:
            print("Stylesheet 'styles.qss' tidak ditemukan. Menggunakan style default.")

    def _create_controls_panel(self):
        panel_widget = QWidget()
        layout = QVBoxLayout(panel_widget)
        layout.setSpacing(15)

        input_group = QGroupBox("Tentukan Rute & Anggaran")
        input_layout = QGridLayout()

        self.start_combo = QComboBox()
        self.start_combo.addItems(self.locations)
        input_layout.addWidget(QLabel("Titik Awal:"), 0, 0)
        input_layout.addWidget(self.start_combo, 0, 1)

        self.end_combo = QComboBox()
        self.end_combo.addItems(self.locations)
        self.end_combo.setCurrentIndex(1)
        input_layout.addWidget(QLabel("Tujuan Akhir:"), 1, 0)
        input_layout.addWidget(self.end_combo, 1, 1)

        self.time_budget_spin = QSpinBox()
        self.time_budget_spin.setRange(1, 48)
        self.time_budget_spin.setValue(8)
        self.time_budget_spin.setSuffix(" Jam")
        input_layout.addWidget(QLabel("Anggaran Waktu:"), 2, 0)
        input_layout.addWidget(self.time_budget_spin, 2, 1)
        
        self.money_budget_spin = QSpinBox()
        self.money_budget_spin.setRange(0, 10000000)
        self.money_budget_spin.setSingleStep(10000)
        self.money_budget_spin.setValue(300000)
        self.money_budget_spin.setPrefix("Rp ")
        input_layout.addWidget(QLabel("Anggaran Biaya:"), 3, 0)
        input_layout.addWidget(self.money_budget_spin, 3, 1)

        input_group.setLayout(input_layout)
        layout.addWidget(input_group)

        must_visit_group = QGroupBox("Pilih Lokasi Wajib Kunjung")
        must_visit_layout = QVBoxLayout()
        
        self.must_visit_list = QListWidget()
        self.must_visit_list.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        for location in self.locations:
            item = QListWidgetItem(location)
            self.must_visit_list.addItem(item)
        must_visit_layout.addWidget(self.must_visit_list)
        must_visit_group.setLayout(must_visit_layout)
        layout.addWidget(must_visit_group)

        self.run_button = QPushButton("Rencanakan Tur")
        self.run_button.setFixedHeight(40)
        self.run_button.clicked.connect(self._run_planning)
        layout.addWidget(self.run_button)
        
        results_group = QGroupBox("Hasil Analisis")
        results_layout = QVBoxLayout()
        self.results_text = QTextEdit()
        self.results_text.setReadOnly(True)
        self.results_text.setText("Selamat datang! Atur rute dan anggaran Anda, lalu klik 'Rencanakan Tur'.")
        results_layout.addWidget(self.results_text)
        results_group.setLayout(results_layout)
        layout.addWidget(results_group)

        return panel_widget

    def _create_display_panel(self):
        panel_widget = QWidget()
        layout = QVBoxLayout(panel_widget)
        
        self.canvas = MplCanvas(self, width=8, height=8, dpi=100)
        
        progresive_enriched_end0.visualize_tour(self.graph, [], "", "", 0, 0, self.canvas.axes)
        
        layout.addWidget(self.canvas)
        return panel_widget

    def _run_planning(self):
        start_point = self.start_combo.currentText()
        end_point = self.end_combo.currentText()
        time_budget = self.time_budget_spin.value() * 60 
        money_budget = self.money_budget_spin.value()
        
        selected_items = self.must_visit_list.selectedItems()
        must_visit_points = [item.text() for item in selected_items]

        if start_point == end_point:
            QMessageBox.warning(self, "Input Tidak Valid", "Titik awal dan tujuan akhir tidak boleh sama.")
            return
        
        if start_point in must_visit_points:
            must_visit_points.remove(start_point)
        if end_point in must_visit_points:
            must_visit_points.remove(end_point)

        self.results_text.setText("Menganalisis rute, mohon tunggu...")
        QApplication.processEvents() 

        tour, final_time, final_cost, log = progresive_enriched_end0.final_tour_algorithm(
            self.graph, start_point, must_visit_points, end_point, time_budget, money_budget
        )

        self._update_results_text(tour, final_time, final_cost, time_budget, money_budget, log)
        
        progresive_enriched_end0.visualize_tour(self.graph, tour, start_point, end_point, final_time, final_cost, self.canvas.axes)
        self.canvas.draw()
    
    def _update_results_text(self, tour, final_time, final_cost, time_budget, money_budget, log):
        
        log_html = "<br>".join(log)

        summary_html = "<h3>Ringkasan Hasil Tur</h3>"
        summary_html += f"<b>Rute Lengkap:</b> {' → '.join(tour)}<br>"
        summary_html += f"<b>Total Waktu Aktual:</b> {int(final_time)} menit ({final_time/60:.1f} jam)<br>"
        summary_html += f"<b>Total Biaya Aktual:</b> Rp {final_cost:,.0f}<br><br>"
        
        time_color = 'green'
        if (time_budget - final_time) < 0:
            time_color = 'red'
            
        money_color = 'green'
        if (money_budget - final_cost) < 0:
            money_color = 'red'

        summary_html += f"<b>Sisa Anggaran Waktu:</b> <font color='{time_color}'>{int(time_budget - final_time)} menit</font><br>"
        summary_html += f"<b>Sisa Anggaran Biaya:</b> <font color='{money_color}'>Rp {money_budget - final_cost:,.0f}</font>"

        self.results_text.setHtml(f"<h3>Log Perencanaan</h3>{log_html}<br><hr>{summary_html}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())