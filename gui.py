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
# This ensures matplotlib embeds correctly in PyQt6
matplotlib.use('QtAgg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

# ==============================================================================
# TAHAP 1: LOGIKA INTI DARI SCRIPT ASLI ANDA
# (Code from progressive_enriched_end_not0.py is pasted here)
# ==============================================================================

def create_bandung_culinary_graph():
    """
    [REFACTOR]
    Mendefinisikan graf dengan data kuliner.
    - Simpul (Node): Memiliki atribut 'pos', 'waktu_layanan', dan 'biaya'.
    - Sisi (Edge): Memiliki atribut 'weight' yang merepresentasikan WAKTU TEMPUH.
    """
    G = nx.Graph()
    
    locations_data = {
        'Alun-Alun Bandung': {'pos': (250, -200), 'waktu_layanan': 30, 'biaya': 35000},
        'Trans Studio Bandung': {'pos': (650, -150), 'waktu_layanan': 180, 'biaya': 250000},
        'Stasiun Bandung': {'pos': (100, -100), 'waktu_layanan': 0, 'biaya': 0},
        'Jalan Braga': {'pos': (350, -50), 'waktu_layanan': 60, 'biaya': 70000},
        'Saung Angklung Udjo': {'pos': (770, 150), 'waktu_layanan': 120, 'biaya': 80000},
        'Gedung Sate': {'pos': (450, 100), 'waktu_layanan': 30, 'biaya': 15000},
        'Monumen Perjuangan': {'pos': (350, 200), 'waktu_layanan': 20, 'biaya': 0},
        'Cihampelas Walk': {'pos': (150, 150), 'waktu_layanan': 90, 'biaya': 100000},
        'Kebun Binatang Bandung': {'pos': (250, 300), 'waktu_layanan': 90, 'biaya': 50000},
        'Hutan Babakan Siliwangi': {'pos': (280, 380), 'waktu_layanan': 45, 'biaya': 0},
        'Teras Cikapundung': {'pos': (220, 420), 'waktu_layanan': 30, 'biaya': 10000},
        'Pipinos Bakery': {'pos': (0, 550), 'waktu_layanan': 45, 'biaya': 50000},
        'Museum Srihadi Soedarsono': {'pos': (150, 500), 'waktu_layanan': 60, 'biaya': 20000},
        'Warung Sate Bu Ngantuk': {'pos': (250, 580), 'waktu_layanan': 60, 'biaya': 60000},
        'Kurokoffe': {'pos': (80, 620), 'waktu_layanan': 45, 'biaya': 45000},
        'Jonn & Sons': {'pos': (50, 680), 'waktu_layanan': 45, 'biaya': 50000},
        'Dago Pakar': {'pos': (700, 550), 'waktu_layanan': 90, 'biaya': 100000},
        'Punclut': {'pos': (350, 650), 'waktu_layanan': 75, 'biaya': 75000},
        'Farmhouse': {'pos': (400, 750), 'waktu_layanan': 120, 'biaya': 100000},
        'Sarae Hills': {'pos': (550, 780), 'waktu_layanan': 120, 'biaya': 50000},
        'Villa Niis': {'pos': (580, 850), 'waktu_layanan': 45, 'biaya': 60000},
        'Ramen Bajuri': {'pos': (300, 850), 'waktu_layanan': 60, 'biaya': 40000},
        'Floating Market': {'pos': (650, 900), 'waktu_layanan': 120, 'biaya': 40000},
        'De Ranch': {'pos': (750, 950), 'waktu_layanan': 90, 'biaya': 30000}
    }
    for loc, data in locations_data.items():
        G.add_node(loc, pos=data['pos'], waktu_layanan=data['waktu_layanan'], biaya=data['biaya'])
    edges = [
        ('Alun-Alun Bandung', 'Jalan Braga', 3), ('Alun-Alun Bandung', 'Stasiun Bandung', 6),
        ('Alun-Alun Bandung', 'Gedung Sate', 9), ('Jalan Braga', 'Gedung Sate', 4),
        ('Jalan Braga', 'Stasiun Bandung', 5), ('Jalan Braga', 'Trans Studio Bandung', 11),
        ('Stasiun Bandung', 'Gedung Sate', 8), ('Gedung Sate', 'Monumen Perjuangan', 6),
        ('Gedung Sate', 'Saung Angklung Udjo', 10), ('Gedung Sate', 'Trans Studio Bandung', 11),
        ('Monumen Perjuangan', 'Saung Angklung Udjo', 12), ('Saung Angklung Udjo', 'Trans Studio Bandung', 13),
        ('Monumen Perjuangan', 'Kebun Binatang Bandung', 5), ('Kebun Binatang Bandung', 'Hutan Babakan Siliwangi', 2),
        ('Hutan Babakan Siliwangi', 'Teras Cikapundung', 1), ('Teras Cikapundung', 'Cihampelas Walk', 3),
        ('Kebun Binatang Bandung', 'Cihampelas Walk', 6), ('Teras Cikapundung', 'Museum Srihadi Soedarsono', 4),
        ('Museum Srihadi Soedarsono', 'Pipinos Bakery', 3), ('Pipinos Bakery', 'Kurokoffe', 2),
        ('Kurokoffe', 'Jonn & Sons', 2), ('Jonn & Sons', 'Warung Sate Bu Ngantuk', 3),
        ('Warung Sate Bu Ngantuk', 'Punclut', 9), ('Cihampelas Walk', 'Dago Pakar', 16),
        ('Museum Srihadi Soedarsono', 'Dago Pakar', 15), ('Dago Pakar', 'Punclut', 13),
        ('Punclut', 'Sarae Hills', 2), ('Sarae Hills', 'Villa Niis', 7),
        ('Villa Niis', 'Ramen Bajuri', 8), ('Ramen Bajuri', 'Floating Market', 5),
        ('Floating Market', 'Farmhouse', 8), ('Farmhouse', 'De Ranch', 9),
        ('Punclut', 'De Ranch', 12),
    ]
    for u, v, w in edges: G.add_edge(u, v, weight=w)
    locations_pos = {loc: data['pos'] for loc, data in locations_data.items()}
    return G, locations_pos

def dijkstra(graph, start, end):
    if start not in graph or end not in graph: return float('inf')
    distances = {node: float('inf') for node in graph.nodes()}
    distances[start] = 0
    pq = [(0, start)]
    while pq:
        dist, current = heapq.heappop(pq)
        if current == end: break
        if dist > distances[current]: continue
        for neighbor in graph.neighbors(current):
            weight = graph[current][neighbor].get('weight', 1) 
            distance = dist + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(pq, (distance, neighbor))
    return distances[end]

def find_progressive_enriched_path(graph, start, end, available_nodes, 
                                   current_time_spent, current_cost_spent, 
                                   TIME_BUDGET, MONEY_BUDGET):
    path, current = [start], start
    remaining_nodes = set(available_nodes)
    alpha, beta = 0.7, 0.3 
    segment_time = 0.0
    segment_cost = 0.0
    service_time_at_segment_end = graph.nodes[end].get('waktu_layanan', 0)
    while current != end:
        competitors = remaining_nodes | {end}
        best_next_stop, best_score = None, float('inf')
        for competitor in competitors:
            dist_curr_comp = dijkstra(graph, current, competitor)
            dist_comp_end = dijkstra(graph, competitor, end)
            service_time_at_competitor = graph.nodes[competitor].get('waktu_layanan', 0)
            price = graph.nodes[competitor].get('biaya', 0)
            time_if_chosen = current_time_spent + segment_time + dist_curr_comp + service_time_at_competitor
            cost_if_chosen = current_cost_spent + segment_cost + price
            total_estimated_time = time_if_chosen + dist_comp_end
            if competitor != end:
                total_estimated_time += service_time_at_segment_end
            if total_estimated_time > TIME_BUDGET or cost_if_chosen > MONEY_BUDGET:
                continue 
            score = (alpha * dist_curr_comp) + (beta * dist_comp_end)
            if score < best_score:
                best_score, best_next_stop = score, competitor

        if best_next_stop is None:
            print(f"      -> ❌ PERINGATAN: Tidak ada rute layak ditemukan ke '{end}' dalam anggaran.")
            return [start], 0.0, 0.0 

        path.append(best_next_stop)
        travel_time_to_stop = dijkstra(graph, current, best_next_stop)
        segment_time += travel_time_to_stop
        current = best_next_stop
        segment_time += graph.nodes[current].get('waktu_layanan', 0)
        segment_cost += graph.nodes[current].get('biaya', 0)
        if current != end:
            if current in remaining_nodes:
                remaining_nodes.remove(current)
        else:
            break 
    return path, segment_time, segment_cost

def final_tour_algorithm(graph, start, must_visit, end, TIME_BUDGET, MONEY_BUDGET):
    """
    [PENTING] Fungsi ini sekarang akan di-run di thread terpisah.
    Semua 'print()' akan ditangkap dan dialihkan ke GUI.
    """
    all_nodes_set, unvisited_must_visit = set(graph.nodes()), set(must_visit)
    final_tour, current_pos = [start], start
    total_time = graph.nodes[start].get('waktu_layanan', 0)
    total_cost = graph.nodes[start].get('biaya', 0)

    print("\n" + "="*60 + "\nALGORITMA TUR KULINER (BUDGET-AWARE)\n" + "="*60)
    print(f"Anggaran Waktu: {TIME_BUDGET} menit ({TIME_BUDGET/60:.1f} jam)")
    print(f"Anggaran Biaya: Rp {MONEY_BUDGET:,.0f}")
    print(f"Status Awal: Waktu={total_time} menit, Biaya=Rp {total_cost:,.0f}")
    print(f"Titik Awal: {start}")
    print(f"Tujuan Akhir: {end}")
    print(f"Wajib Kunjung: {', '.join(must_visit) if must_visit else 'Tidak ada'}")
    print("="*60)

    # 1. Selesaikan semua lokasi WAJIB KUNJUNG
    while unvisited_must_visit:
        next_destination = min(unvisited_must_visit, key=lambda dest: dijkstra(graph, current_pos, dest))
        print(f"\nRencana segmen: dari '{current_pos}' menuju '{next_destination}' (Wajib)")
        
        travel_time_to_dest = dijkstra(graph, current_pos, next_destination)
        service_time_dest = graph.nodes[next_destination].get('waktu_layanan', 0)
        price_dest = graph.nodes[next_destination].get('biaya', 0)

        if (total_time + travel_time_to_dest + service_time_dest > TIME_BUDGET) or \
           (total_cost + price_dest > MONEY_BUDGET):
            print(f"  -> ❌ PERINGATAN: Lokasi wajib '{next_destination}' tidak dapat dikunjungi.")
            print(f"     Estimasi Waktu: {total_time + travel_time_to_dest + service_time_dest} menit (Budget: {TIME_BUDGET})")
            print(f"     Estimasi Biaya: Rp {total_cost + price_dest:,.0f} (Budget: Rp {MONEY_BUDGET:,.0f})")
            unvisited_must_visit.remove(next_destination)
            continue 

        nodes_to_consider = all_nodes_set - set(final_tour) - unvisited_must_visit
        segment, seg_time, seg_cost = find_progressive_enriched_path(
            graph, current_pos, next_destination, nodes_to_consider,
            total_time, total_cost, TIME_BUDGET, MONEY_BUDGET
        )
        
        if len(segment) > 1:
            final_tour.extend(segment[1:])
            total_time += seg_time
            total_cost += seg_cost
            print(f"  -> Rute Ditemukan: {' → '.join(segment[1:])}")
            print(f"     Waktu Segmen: {int(seg_time)} menit, Biaya Segmen: Rp {seg_cost:,.0f}")
            print(f"     Status Anggaran: Waktu={int(total_time)} menit, Biaya=Rp {total_cost:,.0f}")
        
        current_pos = next_destination
        unvisited_must_visit.remove(next_destination)

    # 2. Pergi ke TUJUAN AKHIR
    print(f"\nRencana segmen: dari '{current_pos}' menuju tujuan akhir '{end}'")
    nodes_to_consider = all_nodes_set - set(final_tour)
    segment, seg_time, seg_cost = find_progressive_enriched_path(
        graph, current_pos, end, nodes_to_consider,
        total_time, total_cost, TIME_BUDGET, MONEY_BUDGET
    )
    
    if len(segment) > 1:
        final_tour.extend(segment[1:])
        total_time += seg_time
        total_cost += seg_cost
        print(f"  -> Rute Ditemukan: {' → '.join(segment[1:])}")
        print(f"     Waktu Segmen: {int(seg_time)} menit, Biaya Segmen: Rp {seg_cost:,.0f}")

    unique_tour = []
    for loc in final_tour:
        if not unique_tour or unique_tour[-1] != loc:
            unique_tour.append(loc)
            
    print("\n" + "="*60 + "\nHASIL RUTE TUR FINAL\n" + "="*60)
    print(f"Rute Lengkap: {' → '.join(unique_tour)}")
    print(f"Total Waktu Aktual: {int(total_time)} menit ({total_time/60:.1f} jam)")
    print(f"Total Biaya Aktual: Rp {total_cost:,.0f}")
    print(f"\nSisa Anggaran Waktu: {int(TIME_BUDGET - total_time)} menit")
    print(f"Sisa Anggaran Biaya: Rp {MONEY_BUDGET - total_cost:,.0f}")
    print("="*60)
    
    return unique_tour, total_time, total_cost

# --- [PERUBAHAN BESAR] FUNGSI VISUALISASI ---
def visualize_tour(graph, locations_pos, tour, start_point, end_point, total_time_spent, total_cost_spent, ax):
    """
    [GUI REFACTOR]
    Fungsi ini tidak lagi memanggil `plt.show()` atau `plt.figure()`.
    Ia menerima 'ax' (sebuah Matplotlib Axes object) dan menggambar di atasnya.
    """
    ax.clear() # Hapus gambar sebelumnya
    pos = locations_pos
    
    title = (
        f"Rute Tur Kuliner dari {start_point} ke {end_point}\n"
        f"Total Waktu: {int(total_time_spent)} menit ({total_time_spent/60:.1f} jam) | "
        f"Total Biaya: Rp {total_cost_spent:,.0f}"
    )
    ax.set_title(title, fontsize=12, fontweight='bold', pad=20)

    # Gambar semua node dan edge (latar belakang)
    nx.draw_networkx_nodes(graph, pos, node_color='lightgray', node_size=800, ax=ax)
    nx.draw_networkx_labels(graph, pos, font_size=7, font_weight='bold', ax=ax)
    nx.draw_networkx_edges(graph, pos, width=1, alpha=0.3, ax=ax)

    # Sorot node yang dikunjungi
    tour_nodes = set(tour)
    node_colors = {node: ('#FFD700' if node in tour_nodes else 'lightgray') for node in graph.nodes()} # Gold
    node_colors[start_point], node_colors[end_point] = '#90EE90', '#F08080' # LightGreen, LightCoral
    nx.draw_networkx_nodes(graph, pos, node_color=list(node_colors.values()), node_size=1000, ax=ax)

    # Gambar edge rute tur
    tour_edges = [(tour[i], tour[i+1]) for i in range(len(tour)-1)]
    nx.draw_networkx_edges(graph, pos, edgelist=tour_edges,
                          width=2.5, edge_color='#FF6347', arrows=True, arrowsize=20, ax=ax) # Tomato Red
    
    edge_labels = nx.get_edge_attributes(graph, 'weight')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_size=8, label_pos=0.5, font_color='black', ax=ax)

    # Tambahkan label urutan
    for i, node in enumerate(tour):
        x, y = pos[node]
        ax.text(x, y + 0.18, f'#{i+1}', fontsize=10, fontweight='bold', color='darkred', ha='center',
                bbox=dict(boxstyle='circle,pad=0.2', facecolor='white', alpha=0.7))

    legend_elements = [ plt.Line2D([0], [0], marker='o', color='w', label=f'Start ({start_point})', markerfacecolor='#90EE90', ms=15),
                        plt.Line2D([0], [0], marker='o', color='w', label=f'End ({end_point})', markerfacecolor='#F08080', ms=15),
                        plt.Line2D([0], [0], marker='o', color='w', label='Dikunjungi', markerfacecolor='#FFD700', ms=15),
                        plt.Line2D([0], [0], marker='o', color='w', label='Tidak Dikunjungi', markerfacecolor='lightgray', ms=15),
                        plt.Line2D([0], [0], color='#FF6347', lw=3, label='Rute Tur (Perjalanan)') ]
    ax.legend(handles=legend_elements, loc='best', fontsize=10)
    
    # Tidak ada plt.show() atau plt.savefig() di sini
    # Canvas akan di-draw ulang oleh main GUI
    
# ==============================================================================
# TAHAP 2: KELAS-KELAS HELPER UNTUK GUI (THREADING & LOGGING)
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
            
            # Panggil fungsi algoritma inti Anda
            result = final_tour_algorithm(
                self.graph, self.start, self.must_visit, self.end,
                self.time_budget, self.money_budget
            )
            
            self.progress.emit(100) # Selesai
            self.finished.emit(result) # Kirim hasil
        except Exception as e:
            print(f"\n❌ TERJADI ERROR PADA ALGORITMA:\n{e}")
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
        self.G, self.locations_pos = create_bandung_culinary_graph()
        self.location_list = sorted(list(self.locations_pos.keys()))

    def init_ui(self):
        """
        Membangun semua komponen User Interface.
        """
        self.setWindowTitle("🗺️ Sistem Rekomendasi Tur Kuliner Bandung (Budget-Aware)")
        self.setGeometry(100, 100, 1600, 900)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        # Layout utama (Kiri: Kontrol, Kanan: Output)
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
        self.money_budget_input.setValue(300000)
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
        
        # Set layout pembagian (80% plot, 20% log)
        right_layout.setStretchFactor(plot_group, 4)
        right_layout.setStretchFactor(log_group, 1)

        # Gabungkan panel kiri dan kanan
        main_layout.addWidget(left_panel)
        main_layout.addWidget(right_panel)
        main_layout.setStretchFactor(left_panel, 1)
        main_layout.setStretchFactor(right_panel, 3)
        
        # Terapkan styling
        self.set_stylesheet()

    def set_stylesheet(self):
        """
        Menerapkan QSS (Qt Style Sheet) untuk tema 'eyes-friendly' (dark).
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
            /* Styling untuk Matplotlib Toolbar */
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
        
        # Set default yang berbeda
        self.start_combo.setCurrentText("Stasiun Bandung")
        self.end_combo.setCurrentText("De Ranch")

    def connect_signals(self):
        """
        Menghubungkan sinyal (cth: klik tombol) ke slot (fungsi).
        """
        self.run_button.clicked.connect(self.start_algorithm)
        self.save_preset_button.clicked.connect(self.save_preset)
        self.load_preset_button.clicked.connect(self.load_preset)
        
        # Sinyal untuk update Info Panel
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
        """
        self.log_output.moveCursor(self.log_output.textCursor().MoveOperation.End)
        self.log_output.insertPlainText(text)

    @pyqtSlot(str)
    def update_info_panel(self, location_name):
        """
        Menampilkan detail lokasi di Info Panel.
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
        """
        # 1. Ambil semua input dari GUI
        start = self.start_combo.currentText()
        end = self.end_combo.currentText()
        time_budget = self.time_budget_input.value() * 60  # Konversi jam ke menit
        money_budget = self.money_budget_input.value()
        must_visit = [item.text() for item in self.must_visit_list.selectedItems()]

        # 2. Validasi
        if start == end:
            QMessageBox.warning(self, "Input Tidak Valid", "Titik Awal dan Tujuan Akhir tidak boleh sama.")
            return
        if start in must_visit:
            must_visit.remove(start)
        if end in must_visit:
            must_visit.remove(end)

        # 3. Persiapan GUI untuk proses
        self.run_button.setDisabled(True)
        self.run_button.setText("Menjalankan Algoritma...")
        self.log_output.clear()
        self.progress_bar.setValue(0)
        
        # 4. Hapus gambar sebelumnya
        self.figure.clear()
        self.canvas.draw()

        # 5. Siapkan Thread dan Worker
        self.thread = QThread()
        self.worker = AlgorithmWorker(
            self.G, start, must_visit, end, time_budget, money_budget
        )
        self.worker.moveToThread(self.thread)

        # 6. Hubungkan sinyal dari worker ke GUI
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.on_algorithm_finished)
        self.worker.progress.connect(self.progress_bar.setValue)
        
        # 7. Cleanup thread setelah selesai
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        # 8. Mulai!
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

        optimal_tour, final_time, final_cost = result
        
        if not optimal_tour or len(optimal_tour) <= 1:
            print("\n-> Tidak ada rute yang ditemukan. Plot tidak digambar.")
            QMessageBox.warning(self, "Tidak Ada Rute", "Tidak ada rute yang berhasil ditemukan dengan anggaran tersebut.")
            return

        print("\n-> Menggambar visualisasi rute...")
        try:
            # Gambar di canvas yang ada
            ax = self.figure.subplots()
            visualize_tour(
                self.G, self.locations_pos,
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
        """
        filePath, _ = QFileDialog.getOpenFileName(
            self, "Muat Preset", "", "JSON Files (*.json)"
        )
        
        if filePath:
            try:
                with open(filePath, 'r') as f:
                    preset_data = json.load(f)
                
                # Terapkan data ke GUI
                self.time_budget_input.setValue(preset_data.get("time_budget", 8.0))
                self.money_budget_input.setValue(preset_data.get("money_budget", 300000))
                self.start_combo.setCurrentText(preset_data.get("start_point", ""))
                self.end_combo.setCurrentText(preset_data.get("end_point", ""))
                
                # Reset pilihan list
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