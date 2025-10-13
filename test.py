import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import heapq

# Definisi graf dengan lokasi wisata di Bandung (20 lokasi tersebar)
def create_bandung_graph():
    G = nx.Graph()
    
    # Daftar lokasi wisata dengan posisi yang lebih tersebar
    locations = {
        # Area Pusat Kota (bawah)
        'Stasiun Bandung': (2, 0),
        'Braga Street': (2.5, 0.5),
        'Alun-Alun Bandung': (1.5, 0.8),
        'Museum Konferensi': (1, 0.3),
        'Gedung Sate': (2.8, 1.2),
        
        # Area Tengah (tengah kiri-kanan)
        'Taman Lansia': (0.5, 2),
        'Masjid Raya': (1.2, 1.8),
        'Cihampelas Walk': (3, 2.5),
        'Dago Plaza': (3.5, 2),
        'Taman Film': (4.2, 2.3),
        
        # Area Dago & Punclut (atas kiri)
        'Dago Pakar': (1.5, 3.8),
        'Punclut': (0.8, 4.5),
        'Tebing Keraton': (0.3, 5.2),
        'Curug Dago': (1.8, 4.8),
        
        # Area Lembang (atas tengah-kanan)
        'De Ranch': (3.2, 5),
        'Farmhouse': (3.8, 5.8),
        'Lembang Park & Zoo': (4.5, 5.5),
        'Floating Market': (4, 6.5),
        
        # Area Timur (kanan)
        'Trans Studio': (5.2, 2.8),
        'Saung Angklung': (5.5, 1.5)
    }
    
    # Tambahkan node dengan posisi
    for loc, pos in locations.items():
        G.add_node(loc, pos=pos)
    
    # Tambahkan edge dengan bobot (waktu dalam menit)
    # Koneksi yang lebih kompleks dan realistis
    edges = [
        # Area Pusat Kota
        ('Stasiun Bandung', 'Braga Street', 8),
        ('Stasiun Bandung', 'Alun-Alun Bandung', 10),
        ('Stasiun Bandung', 'Museum Konferensi', 12),
        ('Braga Street', 'Alun-Alun Bandung', 7),
        ('Braga Street', 'Gedung Sate', 12),
        ('Alun-Alun Bandung', 'Museum Konferensi', 8),
        ('Alun-Alun Bandung', 'Gedung Sate', 15),
        ('Alun-Alun Bandung', 'Masjid Raya', 18),
        ('Museum Konferensi', 'Taman Lansia', 22),
        ('Gedung Sate', 'Masjid Raya', 14),
        ('Gedung Sate', 'Cihampelas Walk', 18),
        
        # Area Tengah
        ('Taman Lansia', 'Masjid Raya', 12),
        ('Taman Lansia', 'Dago Pakar', 25),
        ('Masjid Raya', 'Cihampelas Walk', 20),
        ('Cihampelas Walk', 'Dago Plaza', 10),
        ('Cihampelas Walk', 'Dago Pakar', 22),
        ('Dago Plaza', 'Taman Film', 12),
        ('Dago Plaza', 'Trans Studio', 25),
        ('Taman Film', 'Trans Studio', 15),
        ('Taman Film', 'De Ranch', 35),
        
        # Area Dago & Punclut
        ('Dago Pakar', 'Punclut', 15),
        ('Dago Pakar', 'Curug Dago', 18),
        ('Punclut', 'Tebing Keraton', 20),
        ('Punclut', 'Curug Dago', 12),
        ('Punclut', 'De Ranch', 28),
        ('Tebing Keraton', 'Curug Dago', 25),
        ('Curug Dago', 'De Ranch', 22),
        
        # Area Lembang
        ('De Ranch', 'Farmhouse', 15),
        ('De Ranch', 'Lembang Park & Zoo', 20),
        ('Farmhouse', 'Lembang Park & Zoo', 12),
        ('Farmhouse', 'Floating Market', 18),
        ('Lembang Park & Zoo', 'Floating Market', 15),
        
        # Area Timur
        ('Trans Studio', 'Saung Angklung', 18),
        ('Gedung Sate', 'Saung Angklung', 35),
        ('Dago Plaza', 'Saung Angklung', 22),
        
        # Koneksi lintas area (jalan alternatif)
        ('Masjid Raya', 'Dago Pakar', 28),
        ('Cihampelas Walk', 'Punclut', 30),
        ('Taman Film', 'Farmhouse', 40),
        ('Trans Studio', 'De Ranch', 38),
    ]
    
    for u, v, w in edges:
        G.add_edge(u, v, weight=w)
    
    return G, locations

# Implementasi Dijkstra untuk mencari jarak terpendek
def dijkstra(graph, start, end):
    distances = {node: float('inf') for node in graph.nodes()}
    distances[start] = 0
    previous = {node: None for node in graph.nodes()}
    pq = [(0, start)]
    
    while pq:
        current_dist, current = heapq.heappop(pq)
        
        if current == end:
            break
        
        if current_dist > distances[current]:
            continue
        
        for neighbor in graph.neighbors(current):
            weight = graph[current][neighbor]['weight']
            distance = current_dist + weight
            
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous[neighbor] = current
                heapq.heappush(pq, (distance, neighbor))
    
    return distances[end], previous

# Algoritma Greedy Nearest Neighbor
def nearest_neighbor_tour(graph, start, must_visit, end):
    current = start
    unvisited = set(must_visit)
    tour = [current]
    total_time = 0
    
    print("=" * 60)
    print("ALGORITMA GREEDY - NEAREST NEIGHBOR HEURISTIC")
    print("=" * 60)
    print(f"Titik Awal: {start}")
    print(f"Tujuan Akhir: {end}")
    print(f"Destinasi yang Harus Dikunjungi: {', '.join(must_visit)}")
    print("=" * 60)
    
    step = 1
    while unvisited:
        print(f"\n📍 LANGKAH {step}: Posisi Sekarang = {current}")
        print(f"   Destinasi Tersisa: {', '.join(unvisited)}")
        
        # Cari tetangga terdekat
        nearest = None
        min_distance = float('inf')
        
        for destination in unvisited:
            dist, _ = dijkstra(graph, current, destination)
            print(f"   - Jarak ke {destination}: {dist} menit")
            
            if dist < min_distance:
                min_distance = dist
                nearest = destination
        
        print(f"   ✓ Pilih: {nearest} (terdekat: {min_distance} menit)")
        
        # Pindah ke tetangga terdekat
        tour.append(nearest)
        total_time += min_distance
        unvisited.remove(nearest)
        current = nearest
        step += 1
    
    # Pergi ke tujuan akhir
    final_dist, _ = dijkstra(graph, current, end)
    tour.append(end)
    total_time += final_dist
    
    print(f"\n📍 LANGKAH {step}: Posisi Sekarang = {current}")
    print(f"   - Jarak ke tujuan akhir ({end}): {final_dist} menit")
    print(f"   ✓ Menuju tujuan akhir")
    
    print("\n" + "=" * 60)
    print("HASIL RUTE OPTIMAL (GREEDY)")
    print("=" * 60)
    print(f"Rute: {' → '.join(tour)}")
    print(f"Total Waktu Perjalanan: {total_time} menit ({total_time/60:.1f} jam)")
    print("=" * 60)
    
    return tour, total_time

# Visualisasi graf dan rute
def visualize_tour(graph, locations, tour, total_time):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 8))
    
    # Subplot 1: Graf Lengkap
    pos = nx.get_node_attributes(graph, 'pos')
    
    ax1.set_title('Graf Lengkap Lokasi Wisata Bandung (20 Lokasi)', fontsize=14, fontweight='bold', pad=20)
    nx.draw_networkx_nodes(graph, pos, node_color='lightblue', 
                          node_size=1500, ax=ax1)
    nx.draw_networkx_labels(graph, pos, font_size=6, font_weight='bold', ax=ax1)
    nx.draw_networkx_edges(graph, pos, width=1, alpha=0.4, ax=ax1)
    
    # Tampilkan bobot edge
    edge_labels = nx.get_edge_attributes(graph, 'weight')
    edge_labels = {k: f"{v}m" for k, v in edge_labels.items()}
    nx.draw_networkx_edge_labels(graph, pos, edge_labels, font_size=5, ax=ax1)
    
    ax1.axis('off')
    ax1.set_aspect('equal')
    
    # Subplot 2: Rute Tour
    ax2.set_title(f'Rute Tour Optimal (Greedy)\nTotal: {total_time} menit ({total_time/60:.1f} jam)', 
                  fontsize=14, fontweight='bold', pad=20)
    
    # Gambar semua node dengan warna berbeda
    node_colors = []
    for node in graph.nodes():
        if node == tour[0]:
            node_colors.append('lightgreen')  # Start
        elif node == tour[-1]:
            node_colors.append('lightcoral')  # End
        elif node in tour:
            node_colors.append('gold')  # Visited
        else:
            node_colors.append('lightgray')  # Not visited
    
    nx.draw_networkx_nodes(graph, pos, node_color=node_colors, 
                          node_size=1500, ax=ax2)
    nx.draw_networkx_labels(graph, pos, font_size=6, font_weight='bold', ax=ax2)
    
    # Gambar semua edge dengan transparansi
    nx.draw_networkx_edges(graph, pos, width=1, alpha=0.2, ax=ax2)
    
    # Highlight rute tour
    tour_edges = [(tour[i], tour[i+1]) for i in range(len(tour)-1)]
    nx.draw_networkx_edges(graph, pos, edgelist=tour_edges, 
                          width=3, edge_color='red', 
                          arrows=True, arrowsize=20, 
                          arrowstyle='->', ax=ax2)
    
    # Tambahkan nomor urutan kunjungan
    for i, node in enumerate(tour):
        x, y = pos[node]
        ax2.text(x-0.15, y+0.25, f'#{i+1}', fontsize=10, 
                fontweight='bold', color='red',
                bbox=dict(boxstyle='circle', facecolor='white', edgecolor='red'))
    
    ax2.axis('off')
    ax2.set_aspect('equal')
    
    # Tambahkan legend
    legend_elements = [
        plt.Line2D([0], [0], marker='o', color='w', label='Start (Stasiun Bandung)',
                  markerfacecolor='lightgreen', markersize=12),
        plt.Line2D([0], [0], marker='o', color='w', label='End (Floating Market)',
                  markerfacecolor='lightcoral', markersize=12),
        plt.Line2D([0], [0], marker='o', color='w', label='Dikunjungi',
                  markerfacecolor='gold', markersize=12),
        plt.Line2D([0], [0], marker='o', color='w', label='Tidak Dikunjungi',
                  markerfacecolor='lightgray', markersize=12),
        plt.Line2D([0], [0], color='red', linewidth=3, label='Rute Tour')
    ]
    ax2.legend(handles=legend_elements, loc='upper left', fontsize=9)
    
    plt.tight_layout()
    plt.savefig('bandung_tour_greedy.png', dpi=300, bbox_inches='tight')
    plt.show()

# Main program
if __name__ == "__main__":
    # Buat graf
    G, locations = create_bandung_graph()
    
    # Tentukan parameter tour
    start_point = 'Stasiun Bandung'
    end_point = 'Floating Market'
    must_visit = [
        'Braga Street', 'Gedung Sate', 'Cihampelas Walk', 
        'Dago Pakar', 'Punclut', 'Farmhouse', 'Trans Studio',
        'Taman Film', 'De Ranch', 'Curug Dago'
    ]
    
    print("\n🗺️  SISTEM REKOMENDASI TUR WISATA BANDUNG")
    print("   Menggunakan Algoritma Greedy (Nearest Neighbor Heuristic)")
    print()
    
    # Jalankan algoritma
    optimal_tour, total_time = nearest_neighbor_tour(G, start_point, must_visit, end_point)
    
    # Visualisasi
    visualize_tour(G, locations, optimal_tour, total_time)
    
    print("\n✅ Visualisasi berhasil dibuat!")
    print("   File disimpan sebagai: bandung_tour_greedy.png")