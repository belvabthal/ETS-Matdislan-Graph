import networkx as nx
import matplotlib.pyplot as plt
import heapq
import textwrap # [REFACTOR] Tambahan untuk visualisasi

# --- TAHAP 2: FUNGSI PEMBUATAN GRAF KULINER ---

def create_bandung_culinary_graph():
    """
    [REFACTOR]
    Mendefinisikan graf dengan data kuliner.
    - Simpul (Node): Memiliki atribut 'pos', 'waktu_layanan', dan 'biaya'.
    - Sisi (Edge): Memiliki atribut 'weight' yang merepresentasikan WAKTU TEMPUH.
    """
    G = nx.Graph()
    
    # [REFACTOR] Data lokasi sekarang mencakup 'waktu_layanan' (menit) dan 'biaya' (IDR)
    # Saya menggunakan data dari file Anda, dan menambahkan data kuliner fiktif
    # (Anda bisa menggantinya dengan data riset Anda nanti)
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

    # Menambahkan simpul (node) beserta semua atributnya
    for loc, data in locations_data.items():
        G.add_node(loc, pos=data['pos'], waktu_layanan=data['waktu_layanan'], biaya=data['biaya'])
    
    # Daftar sisi (edge) dengan bobot = 'waktu_tempuh' (menit)
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
    # [REFACTOR] 'weight' di sini secara eksplisit berarti 'waktu_tempuh'
    for u, v, w in edges: G.add_edge(u, v, weight=w)
    
    # [REFACTOR] Mengembalikan dict posisi untuk visualisasi
    locations_pos = {loc: data['pos'] for loc, data in locations_data.items()}
    return G, locations_pos

# --- TAHAP 3: LOGIKA INTI ALGORITMA ---

def dijkstra(graph, start, end):
    # Algoritma Dijkstra Anda sudah benar dan efisien.
    # Ini akan mencari jalur terpendek berdasarkan 'weight' (waktu_tempuh).
    if start not in graph or end not in graph: return float('inf')
    distances = {node: float('inf') for node in graph.nodes()}
    distances[start] = 0
    pq = [(0, start)]
    while pq:
        dist, current = heapq.heappop(pq)
        if current == end: break
        if dist > distances[current]: continue
        for neighbor in graph.neighbors(current):
            # [REFACTOR] Pastikan 'weight' ada, beri default 1 jika tidak ada
            weight = graph[current][neighbor].get('weight', 1) 
            distance = dist + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(pq, (distance, neighbor))
    return distances[end]

def find_progressive_enriched_path(graph, start, end, available_nodes, 
                                   current_time_spent, current_cost_spent, 
                                   TIME_BUDGET, MONEY_BUDGET):
    """
    [REFACTOR v2]
    Fungsi ini sekarang menghitung WAKTU LAYANAN di simpul 'end'.
    """
    path, current = [start], start
    remaining_nodes = set(available_nodes)
    alpha, beta = 0.7, 0.3 

    segment_time = 0.0
    segment_cost = 0.0

    # [PERUBAHAN 1] Ambil waktu layanan 'end' node SATU KALI di awal
    # Kita membutuhkannya untuk estimasi
    service_time_at_segment_end = graph.nodes[end].get('waktu_layanan', 0)

    while current != end:
        competitors = remaining_nodes | {end}
        best_next_stop, best_score = None, float('inf')

        for competitor in competitors:
            # 1. Hitung Waktu Tempuh ke kompetitor
            dist_curr_comp = dijkstra(graph, current, competitor)
            # 2. Hitung Waktu Tempuh dari kompetitor ke tujuan (untuk heuristik)
            dist_comp_end = dijkstra(graph, competitor, end)
            
            # 3. Ambil data biaya & waktu dari simpul kompetitor
            service_time_at_competitor = graph.nodes[competitor].get('waktu_layanan', 0)
            price = graph.nodes[competitor].get('biaya', 0)

            # 4. === PEMERIKSAAN KELAYAKAN (CONSTRAINT CHECK v2) ===
            
            # Waktu jika kita memilih 'competitor' (termasuk layanan DI SANA)
            time_if_chosen = current_time_spent + segment_time + dist_curr_comp + service_time_at_competitor
            cost_if_chosen = current_cost_spent + segment_cost + price
            
            # Waktu estimasi total untuk menyelesaikan segmen JIKA kita memilih 'competitor' ini
            total_estimated_time = time_if_chosen + dist_comp_end
            
            # [PERUBAHAN 1 - LOGIKA]
            # Jika 'competitor' BUKAN 'end', kita harus tambahkan waktu layanan 'end'
            # untuk estimasi total.
            # Jika 'competitor' ADALAH 'end', 'service_time_at_competitor' SUDAH 
            # merupakan waktu layanan 'end', jadi 'time_if_chosen' (dan 'total_estimated_time') sudah benar.
            if competitor != end:
                total_estimated_time += service_time_at_segment_end

            # Sekarang lakukan pengecekan dengan estimasi yang sudah akurat
            if total_estimated_time > TIME_BUDGET or cost_if_chosen > MONEY_BUDGET:
                continue # Pilihan ini tidak layak

            # 5. Jika layak, hitung skor heuristiknya
            score = (alpha * dist_curr_comp) + (beta * dist_comp_end)
            if score < best_score:
                best_score, best_next_stop = score, competitor

        if best_next_stop is None:
            # Tidak ada kompetitor yang layak, termasuk 'end' node itu sendiri.
            # Ini berarti kita GAGAL mencapai tujuan segmen.
            print(f"      -> ❌ PERINGATAN: Tidak ada rute layak ditemukan ke '{end}' dalam anggaran.")
            # Kembalikan path kosong dan 0 biaya, karena kita tidak bergerak
            return [start], 0.0, 0.0 

        # --- Update Path dan Biaya untuk Pilihan Terbaik ---
        path.append(best_next_stop)
        
        # Hitung biaya perjalanan dari simpul sebelumnya ke simpul terpilih
        travel_time_to_stop = dijkstra(graph, current, best_next_stop)
        
        # Akumulasi total waktu tempuh segmen
        segment_time += travel_time_to_stop
        
        current = best_next_stop
        
        # [PERUBAHAN 2]
        # Tambahkan waktu layanan & biaya SELALU, baik itu stopover atau 'end'.
        # Kita tidak lagi menggunakan 'if current != end:'
        segment_time += graph.nodes[current].get('waktu_layanan', 0)
        segment_cost += graph.nodes[current].get('biaya', 0)
            
        if current != end:
            # Jika ini bukan 'end', kita hanya perlu me-remove dari 'remaining_nodes'
            if current in remaining_nodes:
                remaining_nodes.remove(current)
        else:
            # Jika ini ADALAH 'end', kita sudah selesai. Break loop.
            break 
            
    return path, segment_time, segment_cost

def final_tour_algorithm(graph, start, must_visit, end, TIME_BUDGET, MONEY_BUDGET):
    """
    [REFACTOR]
    Fungsi orkestrasi utama, sekarang melacak total anggaran.
    """
    all_nodes_set, unvisited_must_visit = set(graph.nodes()), set(must_visit)
    final_tour, current_pos = [start], start
    
    # [REFACTOR] Inisialisasi pelacak anggaran GLOBAL
    # Tambahkan biaya & waktu dari titik AWAL
    total_time = graph.nodes[start].get('waktu_layanan', 0)
    total_cost = graph.nodes[start].get('biaya', 0)

    print("\n" + "="*60 + "\nALGORITMA TUR KULINER (BUDGET-AWARE)\n" + "="*60)
    print(f"Anggaran Waktu: {TIME_BUDGET} menit ({TIME_BUDGET/60:.1f} jam)")
    print(f"Anggaran Biaya: Rp {MONEY_BUDGET:,.0f}")
    print(f"Status Awal: Waktu={total_time} menit, Biaya=Rp {total_cost:,.0f}")
    print("="*60)

    # 1. Selesaikan semua lokasi WAJIB KUNJUNG
    while unvisited_must_visit:
        # Pilih lokasi wajib terdekat dari posisi sekarang
        next_destination = min(unvisited_must_visit, key=lambda dest: dijkstra(graph, current_pos, dest))
        
        print(f"\nRencana segmen: dari '{current_pos}' menuju '{next_destination}'")
        
        # [REFACTOR] Pengecekan Awal: Apakah kita BISA MENCAPAI lokasi wajib ini?
        travel_time_to_dest = dijkstra(graph, current_pos, next_destination)
        service_time_dest = graph.nodes[next_destination].get('waktu_layanan', 0)
        price_dest = graph.nodes[next_destination].get('biaya', 0)

        if (total_time + travel_time_to_dest + service_time_dest > TIME_BUDGET) or \
           (total_cost + price_dest > MONEY_BUDGET):
            print(f"  -> ❌ PERINGATAN: Lokasi wajib '{next_destination}' tidak dapat dikunjungi.")
            print(f"     Estimasi Waktu: {total_time + travel_time_to_dest + service_time_dest} menit (Budget: {TIME_BUDGET})")
            print(f"     Estimasi Biaya: Rp {total_cost + price_dest:,.0f} (Budget: Rp {MONEY_BUDGET:,.0f})")
            unvisited_must_visit.remove(next_destination)
            continue # Lanjut ke lokasi wajib berikutnya

        # Jika bisa, cari rute progresif ke sana
        nodes_to_consider = all_nodes_set - set(final_tour) - unvisited_must_visit
        
        segment, seg_time, seg_cost = find_progressive_enriched_path(
            graph, current_pos, next_destination, nodes_to_consider,
            total_time, total_cost, TIME_BUDGET, MONEY_BUDGET
        )
        
        if len(segment) > 1:
            final_tour.extend(segment[1:])
            # [REFACTOR] Update total anggaran global
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
        # [REFACTOR] Update total anggaran global
        total_time += seg_time
        total_cost += seg_cost
        print(f"  -> Rute Ditemukan: {' → '.join(segment[1:])}")
        print(f"     Waktu Segmen: {int(seg_time)} menit, Biaya Segmen: Rp {seg_cost:,.0f}")

    # Bersihkan duplikat jika ada
    unique_tour = []
    for loc in final_tour:
        if not unique_tour or unique_tour[-1] != loc:
            unique_tour.append(loc)
            
    print("\n" + "="*60 + "\nHASIL RUTE TUR FINAL (TAHAP 3)\n" + "="*60)
    print(f"Rute Lengkap: {' → '.join(unique_tour)}")
    print(f"Total Waktu Aktual: {int(total_time)} menit ({total_time/60:.1f} jam)")
    print(f"Total Biaya Aktual: Rp {total_cost:,.0f}")
    print(f"\nSisa Anggaran Waktu: {int(TIME_BUDGET - total_time)} menit")
    print(f"Sisa Anggaran Biaya: Rp {MONEY_BUDGET - total_cost:,.0f}")
    print("="*60)
    
    # [REFACTOR] Kembalikan total biaya untuk visualisasi
    return unique_tour, total_time, total_cost

# --- TAHAP 4: FUNGSI VISUALISASI ---
def visualize_tour(graph, locations_pos, tour, start_point, end_point, total_time_spent, total_cost_spent):
    """
    [REFACTOR]
    Fungsi visualisasi sekarang menerima total_time dan total_cost
    dan menampilkannya di judul.
    """
    pos = locations_pos # Gunakan posisi yang sudah diteruskan
    plt.figure(figsize=(15, 12)); ax = plt.gca()

    # [REFACTOR] Judul diupdate untuk menampilkan SEMUA biaya (waktu & uang)
    title = (
        f"Rute Tur Kuliner dari {start_point} ke {end_point}\n"
        f"Total Waktu (Perjalanan + Layanan): {int(total_time_spent)} menit ({total_time_spent/60:.1f} jam)\n"
        f"Total Biaya Kuliner: Rp {total_cost_spent:,.0f}"
    )
    ax.set_title(title, fontsize=16, fontweight='bold', pad=20)

    # Gambar semua node dan edge (latar belakang)
    nx.draw_networkx_nodes(graph, pos, node_color='lightgray', node_size=800, ax=ax)
    nx.draw_networkx_labels(graph, pos, font_size=7, font_weight='bold', ax=ax)
    nx.draw_networkx_edges(graph, pos, width=1, alpha=0.3, ax=ax)

    # Sorot node yang dikunjungi
    tour_nodes = set(tour)
    node_colors = {node: ('gold' if node in tour_nodes else 'lightgray') for node in graph.nodes()}
    node_colors[start_point], node_colors[end_point] = 'lightgreen', 'lightcoral'
    nx.draw_networkx_nodes(graph, pos, node_color=list(node_colors.values()), node_size=1000, ax=ax)

    # Gambar edge rute tur
    tour_edges = [(tour[i], tour[i+1]) for i in range(len(tour)-1)]
    nx.draw_networkx_edges(graph, pos, edgelist=tour_edges,
                          width=2.5, edge_color='red', arrows=True, arrowsize=20, ax=ax)
    
    # Label bobot (waktu tempuh) pada edge
    edge_labels = nx.get_edge_attributes(graph, 'weight')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_size=8, label_pos=0.5, font_color='black', ax=ax)

    # Tambahkan label urutan (#1, #2, ...) pada node yang dikunjungi
    for i, node in enumerate(tour):
        x, y = pos[node]
        ax.text(x, y + 0.18, f'#{i+1}', fontsize=10, fontweight='bold', color='darkred', ha='center',
                bbox=dict(boxstyle='circle,pad=0.2', facecolor='white', alpha=0.7))

    # [REFACTOR] Tambahkan legenda untuk atribut simpul (biaya & waktu layanan)
    legend_text = "Atribut Simpul (Estimasi):\n"
    for node in tour:
        nama = textwrap.fill(f"#{i+1} {node}", 25) # Potong nama panjang
        waktu = graph.nodes[node]['waktu_layanan']
        biaya = graph.nodes[node]['biaya']
        if waktu > 0 or biaya > 0:
             legend_text += f"{node}: {waktu} min, Rp {biaya:,.0f}\n"

    # Tampilkan legenda di sisi plot
    # plt.text(1.02, 0.98, legend_text, transform=ax.transAxes, fontsize=9,
    #          verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    legend_elements = [ plt.Line2D([0], [0], marker='o', color='w', label=f'Start ({start_point})', markerfacecolor='lightgreen', ms=15),
                        plt.Line2D([0], [0], marker='o', color='w', label=f'End ({end_point})', markerfacecolor='lightcoral', ms=15),
                        plt.Line2D([0], [0], marker='o', color='w', label='Dikunjungi', markerfacecolor='gold', ms=15),
                        plt.Line2D([0], [0], marker='o', color='w', label='Tidak Dikunjungi', markerfacecolor='lightgray', ms=15),
                        plt.Line2D([0], [0], color='red', lw=3, label='Rute Tur (Perjalanan)') ]
    ax.legend(handles=legend_elements, loc='best', fontsize=10)
    
    plt.tight_layout()
    plt.savefig('bandung_tour_kuliner_budget.png', dpi=300)
    plt.show()

# --- FUNGSI MAIN & HELPER INPUT ---

def get_user_choice(prompt, choices, exclude=None):
    # Fungsi helper ini sudah bagus, tidak perlu diubah.
    if exclude is None: exclude = []
    while True:
        try:
            idx = int(input(f"Masukkan nomor untuk {prompt} (1-{len(choices)}): ")) - 1
            if 0 <= idx < len(choices):
                choice = choices[idx]
                if choice not in exclude: print(f"✓ {prompt} dipilih: {choice}\n"); return choice
                else: print("! Lokasi sudah dipilih, silakan pilih yang lain.")
            else: print("! Nomor tidak valid.")
        except ValueError: print("! Masukkan harus berupa angka.")
        
def get_user_choices(prompt, choices, exclude=None):
    # Fungsi helper ini sudah bagus, tidak perlu diubah.
    if exclude is None: exclude = []
    while True:
        try:
            visit_input = input(f"Masukkan nomor {prompt} (cth: 3, 7, 10): ")
            if not visit_input.strip():
                print("✓ Tidak ada lokasi wajib kunjung tambahan.\n")
                return []
            indices = [int(i.strip()) - 1 for i in visit_input.split(',')]
            temp_list, valid = [], all(0 <= idx < len(choices) for idx in indices)
            if not valid: print("! Terdapat nomor yang tidak valid. Coba lagi."); continue
            for idx in indices:
                choice = choices[idx]
                if choice not in exclude and choice not in temp_list: temp_list.append(choice)
            if temp_list: print(f"✓ Lokasi wajib kunjung: {', '.join(temp_list)}\n"); return temp_list
            else: print("! Tidak ada lokasi valid yang dipilih. Coba lagi.")
        except ValueError: print("! Format input salah. Pastikan hanya angka dan koma.")

def main():
    # [REFACTOR] Panggil fungsi graf kuliner yang baru
    G, locations_pos = create_bandung_culinary_graph() 
    location_list = sorted(list(locations_pos.keys()))
    
    print("🗺️  SISTEM REKOMENDASI TUR KULINER BANDUNG (BUDGET-AWARE)"); print("="*70)
    for i, loc in enumerate(location_list): print(f"{i+1:2d}. {loc}")
    print("="*70)

    # [REFACTOR] === Input Anggaran Baru ===
    while True:
        try:
            time_budget_hours = float(input("Masukkan total ANGGARAN WAKTU (dalam Jam, cth: 8.5): "))
            TIME_BUDGET = time_budget_hours * 60
            money_budget = int(input("Masukkan total ANGGARAN BIAYA (dalam Rupiah, cth: 300000): "))
            MONEY_BUDGET = money_budget
            print(f"✓ Anggaran ditetapkan: {TIME_BUDGET} menit dan Rp {MONEY_BUDGET:,.0f}\n")
            break
        except ValueError:
            print("! Input tidak valid. Coba lagi.")
    # ======================================

    start_point = get_user_choice("TITIK AWAL", location_list)
    end_point = get_user_choice("TUJUAN AKHIR", location_list, exclude=[start_point])
    must_visit = get_user_choices("LOKASI WAJIB KUNJUNG (pisahkan dgn koma)", location_list, exclude=[start_point, end_point])
    
    # [REFACTOR] Panggil algoritma final dengan anggaran
    optimal_tour, final_time, final_cost = final_tour_algorithm(
        G, start_point, must_visit, end_point, TIME_BUDGET, MONEY_BUDGET
    )
    
    # [REFACTOR] Panggil visualisasi dengan data biaya final
    visualize_tour(G, locations_pos, optimal_tour, start_point, end_point, final_time, final_cost)
    
    print("\n✅ Visualisasi berhasil dibuat! File disimpan sebagai: bandung_tour_kuliner_budget.png")

if __name__ == "__main__":
    main()