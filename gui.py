import sys
import json
import io
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib
import heapq
import textwrap

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QGridLayout, QGroupBox, QLabel, QDoubleSpinBox, QSpinBox,
    QComboBox, QListWidget, QPushButton, QProgressBar, QTextEdit,
    QFileDialog, QMessageBox
)
from PyQt6.QtCore import Qt, QThread, QObject, pyqtSignal, pyqtSlot
from PyQt6.QtGui import QIcon, QFont

# --- Matplotlib Backend Setup ---
matplotlib.use('QtAgg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

# ==============================================================================
# [REFAKTOR] TAHAP 1: MENGIMPOR LOGIKA BACKEND
# Semua logika inti sekarang diimpor dari file .py terpisah.
# Pastikan 'progresive_enriched_end0.py' ada di folder yang sama.
# ==============================================================================
try:
    import progresive_enriched_end0 as backend
except ImportError:
    print("FATAL ERROR: File 'progresive_enriched_end0.py' tidak ditemukan.")
    print("Pastikan file tersebut berada di direktori yang sama dengan 'gui.py'.")
    sys.exit(1)


# ==============================================================================
# TAHAP 2: KELAS-KELAS HELPER UNTUK GUI (THREADING & LOGGING)
# (Tidak ada perubahan di Stream, perubahan kecil di AlgorithmWorker)
# ==============================================================================

class Stream(QObject):
    """
    Objek untuk me-redirect stdout (print) ke GUI.
    """
    textWritten = pyqtSignal(str)

    def write(self, text):
        self.textWritten.emit(str(text))

    def flush(self):
        pass  # Diperlukan untuk interface file-like

class AlgorithmWorker(QObject):
    """
    Menjalankan algoritma di thread terpisah untuk mencegah GUI freeze.
    """
    finished = pyqtSignal(object)  # Mengirimkan hasil (tuple) saat selesai
    progress = pyqtSignal(int)      # Mengirimkan update progress

    def __init__(self, graph, start, must_visit, end, time_budget, money_budget):
        super().__init__()
        self.graph = graph
        self.start = start
        self.must_visit = must_visit
        self.end = end
        self.time_budget = time_budget
        self.money_budget = money_budget

    @pyqtSlot()
    def run(self):
        """
        Fungsi ini dieksekusi saat thread dimulai.
        """
        try:
            self.progress.emit(10) # Menandakan proses dimulai
            
            # [REFAKTOR] Memanggil fungsi backend yang diimpor
            # Fungsi ini mengembalikan 4 nilai: (tour, time, cost, log_messages)
            result_tuple = backend.final_tour_algorithm(
                self.graph, self.start, self.must_visit, self.end,
                self.time_budget, self.money_budget
            )
            
            self.progress.emit(90) # Selesai algoritma, proses log

            if result_tuple:
                # [REFAKTOR] Ambil log_messages dan 'print' ke GUI
                log_messages = result_tuple[3]
                for msg in log_messages:
                    print(msg) # Ini akan ditangkap oleh 'Stream'
                
                # [REFAKTOR] Kirim hanya data plot (tour, time, cost) ke sinyal 'finished'
                plot_data = result_tuple[:3]
                self.finished.emit(plot_data)
            else:
                raise Exception("Algoritma tidak mengembalikan hasil.")

            self.progress.emit(100) # Selesai
            
        except Exception as e:
            print(f"\n❌ TERJADI ERROR PADA ALGORITMA:\n{e}")
            import traceback
            print(traceback.format_exc()) # Cetak traceback untuk debug
            self.progress.emit(0)
            self.finished.emit(None) # Kirim None jika gagal


# ==============================================================================
# TAHAP 3: JENDELA UTAMA GUI (MAIN APPLICATION WINDOW)
# ==============================================================================

class TourApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.G = None
        self.locations_pos = None
        self.location_list = []
        self.thread = None
        self.worker = None

        self.init_data()
        self.init_ui()
        self.connect_signals()
        self.populate_lists()
        
        # Alihkan stdout (print) ke GUI
        sys.stdout = Stream(textWritten=self.update_log)

    def init_data(self):
        """
        Memuat data graf saat aplikasi dimulai.
        """
        # [REFAKTOR] Memanggil fungsi backend yang diimpor
        self.G = backend.create_bandung_culinary_graph()
        
        # [REFAKTOR] Ekstrak 'pos' dari node graf, karena fungsi backend baru
        # tidak mengembalikannya secara terpisah.
        self.locations_pos = nx.get_node_attributes(self.G, 'pos')
        self.location_list = sorted(list(self.G.nodes()))

    def init_ui(self):
        """
        Membangun semua komponen User Interface.
        (Tidak ada perubahan di sini)
        """
        self.setWindowTitle("🗺️ Sistem Rekomendasi Tur Kuliner Bandung (Budget-Aware)")
        self.setGeometry(100, 100, 1600, 900)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        main_layout = QHBoxLayout(main_widget)

        # --- Panel Kiri (Kontrol) ---
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_panel.setMinimumWidth(400)
        left_panel.setMaximumWidth(500)

        # 1. Grup Anggaran
        budget_group = QGroupBox("💰 Anggaran")
        budget_layout = QGridLayout()
        self.time_budget_input = QDoubleSpinBox()
        self.time_budget_input.setRange(1.0, 48.0)
        self.time_budget_input.setValue(8.0)
        self.time_budget_input.setSuffix(" Jam")
        self.money_budget_input = QSpinBox()
        self.money_budget_input.setRange(0, 10000000)
        self.money_budget_input.setValue(500000) # [EDIT] Budget default dinaikkan
        self.money_budget_input.setSingleStep(50000)
        self.money_budget_input.setPrefix("Rp ")
        budget_layout.addWidget(QLabel("Waktu:"), 0, 0)
        budget_layout.addWidget(self.time_budget_input, 0, 1)
        budget_layout.addWidget(QLabel("Biaya:"), 1, 0)
        budget_layout.addWidget(self.money_budget_input, 1, 1)
        budget_group.setLayout(budget_layout)

        # 2. Grup Lokasi
        location_group = QGroupBox("📍 Lokasi")
        location_layout = QGridLayout()
        self.start_combo = QComboBox()
        self.end_combo = QComboBox()
        self.must_visit_list = QListWidget()
        self.must_visit_list.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        self.must_visit_list.setMinimumHeight(150)
        location_layout.addWidget(QLabel("Titik Awal:"), 0, 0)
        location_layout.addWidget(self.start_combo, 0, 1)
        location_layout.addWidget(QLabel("Tujuan Akhir:"), 1, 0)
        location_layout.addWidget(self.end_combo, 1, 1)
        location_layout.addWidget(QLabel("Wajib Kunjung:"), 2, 0, Qt.AlignmentFlag.AlignTop)
        location_layout.addWidget(self.must_visit_list, 2, 1)
        location_group.setLayout(location_layout)

        # 3. Grup Info (UX Improvement)
        info_group = QGroupBox("ℹ️ Info Lokasi")
        info_layout = QVBoxLayout()
        self.info_display = QTextEdit()
        self.info_display.setReadOnly(True)
        self.info_display.setPlaceholderText("Klik lokasi di atas untuk melihat detail...")
        self.info_display.setMinimumHeight(60)
        info_layout.addWidget(self.info_display)
        info_group.setLayout(info_layout)

        # 4. Grup Aksi
        action_group = QGroupBox("🚀 Aksi")
        action_layout = QGridLayout()
        self.run_button = QPushButton("Jalankan Algoritma Tur")
        self.run_button.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        self.save_preset_button = QPushButton("Simpan Preset")
        self.load_preset_button = QPushButton("Muat Preset")
        self.progress_bar = QProgressBar()
        action_layout.addWidget(self.run_button, 0, 0, 1, 2)
        action_layout.addWidget(self.progress_bar, 1, 0, 1, 2)
        action_layout.addWidget(self.save_preset_button, 2, 0)
        action_layout.addWidget(self.load_preset_button, 2, 1)
        action_group.setLayout(action_layout)

        left_layout.addWidget(budget_group)
        left_layout.addWidget(location_group)
        left_layout.addWidget(info_group)
        left_layout.addWidget(action_group)
        left_layout.addStretch()

        # --- Panel Kanan (Output) ---
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)

        # 1. Output Visualisasi (Embedded Matplotlib)
        plot_group = QGroupBox("📊 Visualisasi Rute")
        plot_layout = QVBoxLayout()
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        plot_layout.addWidget(self.toolbar)
        plot_layout.addWidget(self.canvas)
        plot_group.setLayout(plot_layout)

        # 2. Output Log
        log_group = QGroupBox("📝 Log Proses")
        log_layout = QVBoxLayout()
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setFont(QFont("Courier New", 9))
        self.log_output.setMinimumHeight(150)
        log_layout.addWidget(self.log_output)
        log_group.setLayout(log_layout)

        right_layout.addWidget(plot_group)
        right_layout.addWidget(log_group)
        
        right_layout.setStretchFactor(plot_group, 4)
        right_layout.setStretchFactor(log_group, 1)

        main_layout.addWidget(left_panel)
        main_layout.addWidget(right_panel)
        main_layout.setStretchFactor(left_panel, 1)
        main_layout.setStretchFactor(right_panel, 3)
        
        self.set_stylesheet()

    def set_stylesheet(self):
        """
        Menerapkan QSS (Qt Style Sheet) untuk tema 'eyes-friendly' (dark).
        (Tidak ada perubahan di sini)
        """
        self.setStyleSheet("""
            QMainWindow, QWidget {
                background-color: #2E2E2E;
                color: #E0E0E0;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QGroupBox {
                background-color: #3C3C3C;
                border: 1px solid #555555;
                border-radius: 8px;
                margin-top: 10px;
                font-size: 11pt;
                font-weight: bold;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 5px 0 5px;
                left: 10px;
            }
            QLabel {
                font-size: 10pt;
            }
            QDoubleSpinBox, QSpinBox, QComboBox, QTextEdit, QListWidget {
                background-color: #4A4A4A;
                color: #FFFFFF;
                border: 1px solid #555555;
                border-radius: 5px;
                padding: 5px;
                font-size: 10pt;
            }
            QSpinBox::up-button, QDoubleSpinBox::up-button, QComboBox::down-arrow {
                border: 1px solid #555;
                background-color: #5A5A5A;
            }
            QSpinBox::down-button, QDoubleSpinBox::down-button {
                border: 1px solid #555;
                background-color: #5A5A5A;
            }
            QListWidget::item:selected {
                background-color: #007ACC; /* Biru cerah untuk item terpilih */
            }
            QPushButton {
                background-color: #007ACC;
                color: white;
                font-weight: bold;
                border: none;
                border-radius: 5px;
                padding: 8px 15px;
                font-size: 10pt;
            }
            QPushButton:hover {
                background-color: #008CFF;
            }
            QPushButton:disabled {
                background-color: #555555;
                color: #AAAAAA;
            }
            QProgressBar {
                border: 1px solid #555555;
                border-radius: 5px;
                text-align: center;
                color: white;
            }
            QProgressBar::chunk {
                background-color: #007ACC;
                border-radius: 5px;
            }
            #qt_toolbar_navigation {
                background-color: #3C3C3C;
            }
        """)

    def populate_lists(self):
        """
        Mengisi QComboBox dan QListWidget dengan data lokasi.
        """
        self.start_combo.addItems(self.location_list)
        self.end_combo.addItems(self.location_list)
        self.must_visit_list.addItems(self.location_list)
        
        # [EDIT] Set default baru berdasarkan data graf yang baru
        self.start_combo.setCurrentText("Stasiun Bandung")
        self.end_combo.setCurrentText("Harmony Dimsum")

    def connect_signals(self):
        """
        Menghubungkan sinyal (cth: klik tombol) ke slot (fungsi).
        (Tidak ada perubahan di sini)
        """
        self.run_button.clicked.connect(self.start_algorithm)
        self.save_preset_button.clicked.connect(self.save_preset)
        self.load_preset_button.clicked.connect(self.load_preset)
        
        self.start_combo.currentTextChanged.connect(self.update_info_panel)
        self.end_combo.currentTextChanged.connect(self.update_info_panel)
        self.must_visit_list.itemClicked.connect(
            lambda item: self.update_info_panel(item.text())
        )

    # --- FUNGSI SLOT (HANDLER) ---

    @pyqtSlot(str)
    def update_log(self, text):
        """
        Menambahkan teks dari 'print' ke log output.
        (Tidak ada perubahan di sini)
        """
        self.log_output.moveCursor(self.log_output.textCursor().MoveOperation.End)
        self.log_output.insertPlainText(text)

    @pyqtSlot(str)
    def update_info_panel(self, location_name):
        """
        Menampilkan detail lokasi di Info Panel.
        (Tidak ada perubahan di sini)
        """
        if not location_name or location_name not in self.G.nodes:
            self.info_display.clear()
            return
            
        try:
            data = self.G.nodes[location_name]
            waktu = data.get('waktu_layanan', 0)
            biaya = data.get('biaya', 0)
            
            info_text = (
                f"Nama: {location_name}\n"
                f"Estimasi Waktu Layanan: {waktu} menit\n"
                f"Estimasi Biaya Masuk/Makan: Rp {biaya:,.0f}"
            )
            self.info_display.setText(info_text)
        except Exception as e:
            self.info_display.setText(f"Error mengambil data untuk {location_name}: {e}")

    @pyqtSlot()
    def start_algorithm(self):
        """
        Mempersiapkan dan memulai thread algoritma.
        (Tidak ada perubahan di sini, worker yang akan memanggil 'backend')
        """
        start = self.start_combo.currentText()
        end = self.end_combo.currentText()
        time_budget = self.time_budget_input.value() * 60  # Konversi jam ke menit
        money_budget = self.money_budget_input.value()
        must_visit = [item.text() for item in self.must_visit_list.selectedItems()]

        if start == end:
            QMessageBox.warning(self, "Input Tidak Valid", "Titik Awal dan Tujuan Akhir tidak boleh sama.")
            return
        if start in must_visit:
            must_visit.remove(start)
        if end in must_visit:
            must_visit.remove(end)

        self.run_button.setDisabled(True)
        self.run_button.setText("Menjalankan Algoritma...")
        self.log_output.clear()
        self.progress_bar.setValue(0)
        
        self.figure.clear()
        self.canvas.draw()

        self.thread = QThread()
        self.worker = AlgorithmWorker(
            self.G, start, must_visit, end, time_budget, money_budget
        )
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.on_algorithm_finished)
        self.worker.progress.connect(self.progress_bar.setValue)
        
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()

    @pyqtSlot(object)
    def on_algorithm_finished(self, result):
        """
        Dipanggil saat thread worker selesai.
        """
        self.run_button.setDisabled(False)
        self.run_button.setText("Jalankan Algoritma Tur")
        
        if result is None:
            QMessageBox.critical(self, "Error", "Terjadi kegagalan saat menjalankan algoritma. Cek log.")
            self.progress_bar.setValue(0)
            return

        # [REFAKTOR] 'result' sekarang adalah 3-tuple (tour, time, cost)
        # yang dikirim oleh worker.
        optimal_tour, final_time, final_cost = result
        
        if not optimal_tour or len(optimal_tour) <= 1:
            print("\n-> Tidak ada rute yang ditemukan. Plot tidak digambar.")
            QMessageBox.warning(self, "Tidak Ada Rute", "Tidak ada rute yang berhasil ditemukan dengan anggaran tersebut.")
            return

        print("\n-> Menggambar visualisasi rute...")
        try:
            ax = self.figure.subplots()
            
            # [REFAKTOR] Memanggil fungsi 'visualize_tour' dari backend
            # dan menghapus argumen 'locations_pos' yang tidak lagi diperlukan.
            backend.visualize_tour(
                self.G,
                optimal_tour,
                self.start_combo.currentText(), self.end_combo.currentText(),
                final_time, final_cost,
                ax
            )
            self.canvas.draw() # Tampilkan gambar baru
            print("-> Visualisasi rute berhasil dibuat di GUI.")
        except Exception as e:
            print(f"\n❌ GAGAL MENGGAMBAR PLOT: {e}")
            QMessageBox.critical(self, "Error Plot", f"Gagal memvisualisasikan rute: {e}")

    @pyqtSlot()
    def save_preset(self):
        """
        Menyimpan konfigurasi saat ini ke file JSON.
        (Tidak ada perubahan di sini)
        """
        preset_data = {
            "time_budget": self.time_budget_input.value(),
            "money_budget": self.money_budget_input.value(),
            "start_point": self.start_combo.currentText(),
            "end_point": self.end_combo.currentText(),
            "must_visit": [item.text() for item in self.must_visit_list.selectedItems()]
        }
        
        filePath, _ = QFileDialog.getSaveFileName(
            self, "Simpan Preset", "", "JSON Files (*.json)"
        )
        
        if filePath:
            try:
                with open(filePath, 'w') as f:
                    json.dump(preset_data, f, indent=4)
                QMessageBox.information(self, "Sukses", "Preset berhasil disimpan.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Gagal menyimpan preset: {e}")

    @pyqtSlot()
    def load_preset(self):
        """
        Memuat konfigurasi dari file JSON.
        (Tidak ada perubahan di sini)
        """
        filePath, _ = QFileDialog.getOpenFileName(
            self, "Muat Preset", "", "JSON Files (*.json)"
        )
        
        if filePath:
            try:
                with open(filePath, 'r') as f:
                    preset_data = json.load(f)
                
                self.time_budget_input.setValue(preset_data.get("time_budget", 8.0))
                self.money_budget_input.setValue(preset_data.get("money_budget", 300000))
                self.start_combo.setCurrentText(preset_data.get("start_point", ""))
                self.end_combo.setCurrentText(preset_data.get("end_point", ""))
                
                self.must_visit_list.clearSelection()
                must_visit_items = preset_data.get("must_visit", [])
                for i in range(self.must_visit_list.count()):
                    item = self.must_visit_list.item(i)
                    if item.text() in must_visit_items:
                        item.setSelected(True)
                        
                QMessageBox.information(self, "Sukses", "Preset berhasil dimuat.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Gagal memuat preset: {e}")

    def closeEvent(self, event):
        """
        Memastikan stdout dikembalikan saat aplikasi ditutup.
        (Tidak ada perubahan di sini)
        """
        sys.stdout = sys.__stdout__  # Kembalikan stdout asli
        super().closeEvent(event)

# ==============================================================================
# TAHAP 4: EKSEKUSI APLIKASI
# ==============================================================================

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TourApp()
    window.show()
    sys.exit(app.exec())