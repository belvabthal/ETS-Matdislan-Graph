import networkx as nx
import matplotlib.pyplot as plt
import heapq

# --- FUNGSI PEMBUATAN GRAF (DENGAN EDGE TERBARU) ---
def create_bandung_graph():
    """
    Mendefinisikan graf dengan data bobot (edge) yang diperbarui 
    berdasarkan pengukuran Google Maps.
    """
    G = nx.Graph()
    locations = {
        'Alun-Alun Bandung': (250, -200),
        'Trans Studio Bandung': (650, -150),
        'Stasiun Bandung': (100, -100),
        'Jalan Braga': (350, -50),
        'Saung Angklung Udjo': (770, 150),
        'Gedung Sate': (450, 100),
        'Monumen Perjuangan': (350, 200),
        'Cihampelas Walk': (150, 150),
        'Kebun Binatang Bandung': (250, 300),
        'Hutan Babakan Siliwangi': (280, 380),
        'Teras Cikapundung': (220, 420),
        'Pipinos Bakery (Ciumbuleuit)': (0, 550),
        'Museum Srihadi Soedarsono (Ciumbuleuit)': (150, 500),
        'Warung Sate Bu Ngantuk (Ciumbuleuit)': (250, 580),
        'Kurokoffe (Ciumbuleuit)': (80, 620),
        'Jonn & Sons (Ciumbuleuit)': (50, 680),
        'Dago Pakar': (700, 550),
        'Punclut': (350, 650),
        'Farmhouse (Lembang)': (400, 750),
        'Sarae Hills (Pagermaneuh)': (550, 780),
        'Villa Niis': (580, 850),
        'Ramen Bajuri (Lembang)': (300, 850),
        'Floating Market (Lembang)': (650, 900),
        'De Ranch (Lembang)': (750, 950)
    }
    for loc, pos in locations.items(): G.add_node(loc, pos=pos)
    
    # Daftar edge dengan nama yang sudah disesuaikan dengan dictionary 'locations'
    edges = [
        ('Alun-Alun Bandung', 'Jalan Braga', 3),
        ('Alun-Alun Bandung', 'Stasiun Bandung', 6),
        ('Alun-Alun Bandung', 'Gedung Sate', 9),
        ('Jalan Braga', 'Gedung Sate', 4),
        ('Jalan Braga', 'Stasiun Bandung', 5),
        ('Jalan Braga', 'Trans Studio Bandung', 11),
        ('Stasiun Bandung', 'Gedung Sate', 8),
        ('Gedung Sate', 'Monumen Perjuangan', 6),
        ('Gedung Sate', 'Saung Angklung Udjo', 10),
        ('Gedung Sate', 'Trans Studio Bandung', 11),
        ('Monumen Perjuangan', 'Saung Angklung Udjo', 12),
        ('Saung Angklung Udjo', 'Trans Studio Bandung', 13),

        ('Monumen Perjuangan', 'Kebun Binatang Bandung', 5),
        ('Kebun Binatang Bandung', 'Hutan Babakan Siliwangi', 2),
        ('Hutan Babakan Siliwangi', 'Teras Cikapundung', 1),
        ('Teras Cikapundung', 'Cihampelas Walk', 3),
        ('Kebun Binatang Bandung', 'Cihampelas Walk', 6),
        ('Teras Cikapundung', 'Museum Srihadi Soedarsono (Ciumbuleuit)', 4),
        ('Museum Srihadi Soedarsono (Ciumbuleuit)', 'Pipinos Bakery (Ciumbuleuit)', 3),
        ('Pipinos Bakery (Ciumbuleuit)', 'Kurokoffe (Ciumbuleuit)', 2),
        ('Kurokoffe (Ciumbuleuit)', 'Jonn & Sons (Ciumbuleuit)', 2),
        ('Jonn & Sons (Ciumbuleuit)', 'Warung Sate Bu Ngantuk (Ciumbuleuit)', 3),
        ('Warung Sate Bu Ngantuk (Ciumbuleuit)', 'Punclut', 9),
        ('Cihampelas Walk', 'Dago Pakar', 16),
        ('Museum Srihadi Soedarsono (Ciumbuleuit)', 'Dago Pakar', 15),
        ('Dago Pakar', 'Punclut', 13),
        ('Punclut', 'Sarae Hills (Pagermaneuh)', 2),
        ('Sarae Hills (Pagermaneuh)', 'Villa Niis', 7),
        ('Villa Niis', 'Ramen Bajuri (Lembang)', 8),
        ('Ramen Bajuri (Lembang)', 'Floating Market (Lembang)', 5),
        ('Floating Market (Lembang)', 'Farmhouse (Lembang)', 8),
        ('Farmhouse (Lembang)', 'De Ranch (Lembang)', 9),
        ('Punclut', 'De Ranch (Lembang)', 12),
    ]
    for u, v, w in edges: G.add_edge(u, v, weight=w)
    return G, locations

# --- LOGIKA PERJALANAN PROGRESIF (TIDAK BERUBAH) ---
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
            weight = graph[current][neighbor]['weight']
            distance = dist + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(pq, (distance, neighbor))
    return distances[end]

def find_progressive_enriched_path(graph, start, end, available_nodes):
    path, current = [start], start
    remaining_nodes = set(available_nodes)
    alpha, beta = 0.7, 0.3
    while current != end:
        competitors = remaining_nodes | {end}
        best_next_stop, best_score = None, float('inf')
        for competitor in competitors:
            dist_curr_comp = dijkstra(graph, current, competitor)
            dist_comp_end = dijkstra(graph, competitor, end)
            score = (alpha * dist_curr_comp) + (beta * dist_comp_end)
            if score < best_score:
                best_score, best_next_stop = score, competitor
        if best_next_stop is None: break
        path.append(best_next_stop)
        current = best_next_stop
        if current in remaining_nodes:
            remaining_nodes.remove(current)
    return path, sum(dijkstra(graph, path[i], path[i+1]) for i in range(len(path) - 1))

def final_tour_algorithm(graph, start, must_visit, end):
    all_nodes_set, unvisited_must_visit = set(graph.nodes()), set(must_visit)
    final_tour, current_pos = [start], start
    print("\n" + "="*60 + "\nALGORITMA PERJALANAN PROGRESIF (DATA AKURAT)\n" + "="*60)
    while unvisited_must_visit:
        next_destination = min(unvisited_must_visit, key=lambda dest: dijkstra(graph, current_pos, dest))
        print(f"\nRencana segmen: dari '{current_pos}' menuju '{next_destination}'")
        nodes_to_consider = all_nodes_set - set(final_tour) - unvisited_must_visit
        segment, segment_time = find_progressive_enriched_path(graph, current_pos, next_destination, nodes_to_consider)
        print(f"  -> Rute Ditemukan: {' → '.join(segment[1:])} ({int(segment_time)} menit)")
        final_tour.extend(segment[1:])
        current_pos = next_destination
        unvisited_must_visit.remove(next_destination)
    print(f"\nRencana segmen: dari '{current_pos}' menuju tujuan akhir '{end}'")
    nodes_to_consider = all_nodes_set - set(final_tour)
    segment, segment_time = find_progressive_enriched_path(graph, current_pos, end, nodes_to_consider)
    print(f"  -> Rute Ditemukan: {' → '.join(segment[1:])} ({int(segment_time)} menit)")
    final_tour.extend(segment[1:])
    unique_tour = []
    for loc in final_tour:
        if not unique_tour or unique_tour[-1] != loc:
            unique_tour.append(loc)
    total_time = sum(dijkstra(graph, unique_tour[i], unique_tour[i+1]) for i in range(len(unique_tour)-1))
    print("\n" + "="*60 + "\nHASIL RUTE TUR FINAL\n" + "="*60)
    print(f"Rute Lengkap: {' → '.join(unique_tour)}")
    print(f"Total Waktu Perjalanan: {int(total_time)} menit ({total_time/60:.1f} jam)\n" + "="*60)
    return unique_tour

# --- FUNGSI VISUALISASI DAN MAIN (Tidak perlu diubah) ---
def visualize_tour(graph, locations, tour, start_point, end_point):
    total_time = sum(dijkstra(graph, tour[i], tour[i+1]) for i in range(len(tour)-1))
    pos = nx.get_node_attributes(graph, 'pos')
    plt.figure(figsize=(15, 12)); ax = plt.gca()
    ax.set_title(f'Rute Tur Progresif dari {start_point} ke {end_point}\nTotal Waktu: {int(total_time)} menit ({total_time/60:.1f} jam)',
                 fontsize=16, fontweight='bold', pad=20)
    nx.draw_networkx_nodes(graph, pos, node_color='lightgray', node_size=800, ax=ax)
    nx.draw_networkx_labels(graph, pos, font_size=7, font_weight='bold', ax=ax)
    nx.draw_networkx_edges(graph, pos, width=1, alpha=0.3, ax=ax)
    tour_nodes = set(tour)
    node_colors = {node: ('gold' if node in tour_nodes else 'lightgray') for node in graph.nodes()}
    node_colors[start_point], node_colors[end_point] = 'lightgreen', 'lightcoral'
    nx.draw_networkx_nodes(graph, pos, node_color=list(node_colors.values()), node_size=1000, ax=ax)
    tour_edges = [(tour[i], tour[i+1]) for i in range(len(tour)-1)]
    nx.draw_networkx_edges(graph, pos, edgelist=tour_edges,
                          width=2.5, edge_color='red', arrows=True, arrowsize=20, ax=ax)
    edge_labels = {
        (u, v): str(int(d['weight']))
        for u, v, d in graph.edges(data=True)
        # if (u, v) in tour_edges or (v, u) in tour_edges
    }
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_size=8, label_pos=0.5, font_color='black', ax=ax)
    for i, node in enumerate(tour):
        x, y = pos[node]
        ax.text(x, y + 0.18, f'#{i+1}', fontsize=10, fontweight='bold', color='darkred', ha='center',
                bbox=dict(boxstyle='circle,pad=0.2', facecolor='white', alpha=0.7))
    legend_elements = [ plt.Line2D([0], [0], marker='o', color='w', label=f'Start ({start_point})', markerfacecolor='lightgreen', ms=15),
                        plt.Line2D([0], [0], marker='o', color='w', label=f'End ({end_point})', markerfacecolor='lightcoral', ms=15),
                        plt.Line2D([0], [0], marker='o', color='w', label='Dikunjungi', markerfacecolor='gold', ms=15),
                        plt.Line2D([0], [0], marker='o', color='w', label='Tidak Dikunjungi', markerfacecolor='lightgray', ms=15),
                        plt.Line2D([0], [0], color='red', lw=3, label='Rute Tur') ]
    ax.legend(handles=legend_elements, loc='best', fontsize=10)
    plt.tight_layout(); plt.savefig('bandung_tour_progresif_akurat.png', dpi=300); plt.show()

def main():
    G, locations = create_bandung_graph()
    location_list = sorted(list(locations.keys()))
    print("🗺️  SISTEM REKOMENDASI TUR WISATA BANDUNG (LOGIKA PROGRESIF & DATA AKURAT)"); print("="*70)
    for i, loc in enumerate(location_list): print(f"{i+1:2d}. {loc}")
    print("="*70)
    start_point = get_user_choice("TITIK AWAL", location_list)
    end_point = get_user_choice("TUJUAN AKHIR", location_list, exclude=[start_point])
    must_visit = get_user_choices("LOKASI WAJIB KUNJUNG (pisahkan dgn koma)", location_list, exclude=[start_point, end_point])
    optimal_tour = final_tour_algorithm(G, start_point, must_visit, end_point)
    visualize_tour(G, locations, optimal_tour, start_point, end_point)
    print("\n✅ Visualisasi berhasil dibuat! File disimpan sebagai: bandung_tour_progresif_akurat.png")

def get_user_choice(prompt, choices, exclude=None):
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

if __name__ == "__main__":
    main()