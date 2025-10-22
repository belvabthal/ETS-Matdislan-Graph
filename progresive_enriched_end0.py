import networkx as nx
import matplotlib.pyplot as plt
import heapq
import textwrap

# --- TAHAP 2: FUNGSI PEMBUATAN GRAF KULINER (FINAL) ---
def create_bandung_culinary_graph():
    """
    [POSISI DIPERBARUI]
    Mendefinisikan graf dengan posisi (pos) vertex yang telah disesuaikan
    berdasarkan koordinat geografis nyata untuk visualisasi yang lebih akurat.
    """
    G = nx.Graph()
    
    # [POSISI DIPERBARUI] Database lokasi dengan koordinat yang sudah dipetakan
    locations_data = {
        # Format: 'Nama Lokasi': {'pos': (x, y), 'waktu_layanan': menit, 'biaya': IDR}
        # Area Pusat Kota & Selatan 360
        'Waroeng Lokal': {'pos': (180, 460), 'waktu_layanan': 20, 'biaya': 85000},
        'Dimsum Sembilan Ayam': {'pos': (165, 565), 'waktu_layanan': 10, 'biaya': 45000},
        'Toko Roti Sidodadi': {'pos': (288, 465), 'waktu_layanan': 5, 'biaya': 100000},
        'Sudirman Street Bandung': {'pos': (275, 360), 'waktu_layanan': 15, 'biaya': 50000},
        'Warung Bu Imas': {'pos': (475, 370), 'waktu_layanan': 10, 'biaya': 60000},
        'Ramen Bajuri (Lengkong)': {'pos': (500, 290), 'waktu_layanan': 20, 'biaya': 40000},
        'Makaroni Squad': {'pos': (498, 440), 'waktu_layanan': 7, 'biaya': 20000},
        'Mie Naripan': {'pos': (603, 410), 'waktu_layanan': 20, 'biaya': 86000},
        'Jalan Braga': {'pos': (580, 500), 'waktu_layanan': 120, 'biaya': 300000},
        'Emperano Pizza': {'pos': (780, 290), 'waktu_layanan': 25, 'biaya': 80000},

        # Area Dago, Cihapit, Trunojoyo
        'Drunk Baker': {'pos': (658, 640), 'waktu_layanan': 10, 'biaya': 100000},
        'Bakmie Tjo Kin': {'pos': (710, 720), 'waktu_layanan': 15, 'biaya': 50000},
        'Five Monkeys Burger': {'pos': (740, 640), 'waktu_layanan': 20, 'biaya': 100000},
        'Sate Jando Belakang Gd Sate': {'pos': (630, 750), 'waktu_layanan': 10, 'biaya': 35000},
        'Iga Bakar Si Jangkung': {'pos': (500, 770), 'waktu_layanan': 60, 'biaya': 80000},
        'Kedai Roti Ibu Saya': {'pos': (490, 840), 'waktu_layanan': 10, 'biaya': 30000},
        
        # Area Sukajadi & Ciumbuleuit (Utara)
        'Mie Soobek': {'pos': (280, 810), 'waktu_layanan': 15, 'biaya': 55000},
        'Pipinos Bakery': {'pos': (330, 900), 'waktu_layanan': 45, 'biaya': 50000},
        'Warung Sate Bu Ngantuk': {'pos': (350, 1040), 'waktu_layanan': 60, 'biaya': 60000},
        'Kurokoffe': {'pos': (290, 1000), 'waktu_layanan': 45, 'biaya': 45000},
        'Wandas Club': {'pos': (230, 980), 'waktu_layanan': 20, 'biaya': 80000},
        'Jonn & Sons': {'pos': (260, 1110), 'waktu_layanan': 45, 'biaya': 50000},
        'Harmony Dimsum': {'pos': (200, 1170), 'waktu_layanan': 15, 'biaya': 70000},
    }


    for loc, data in locations_data.items():
        G.add_node(loc, pos=data['pos'], waktu_layanan=data['waktu_layanan'], biaya=data['biaya'])
    
    edges = [
        # Edges Awal Anda
        ('Warung Bu Imas', 'Waroeng Lokal', 9),
        ('Warung Bu Imas', 'Jalan Braga', 7),
        ('Waroeng Lokal', 'Sate Jando Belakang Gd Sate', 8),
        ('Jalan Braga', 'Sate Jando Belakang Gd Sate', 4),
        ('Emperano Pizza', 'Five Monkeys Burger', 9),
        ('Emperano Pizza', 'Mie Naripan', 8),
        ('Mie Naripan', 'Drunk Baker', 3),
        ('Drunk Baker', 'Sudirman Street Bandung', 7),
        ('Mie Naripan', 'Bakmie Tjo Kin', 6),
        ('Bakmie Tjo Kin', 'Sate Jando Belakang Gd Sate', 3),
        ('Bakmie Tjo Kin', 'Waroeng Lokal', 10),
        ('Jalan Braga', 'Makaroni Squad', 7),
        ('Mie Naripan', 'Makaroni Squad', 8),
        ('Kedai Roti Ibu Saya', 'Sate Jando Belakang Gd Sate', 5),
        ('Kedai Roti Ibu Saya', 'Waroeng Lokal', 8),
        ('Kedai Roti Ibu Saya', 'Jonn & Sons', 7),
        ('Kurokoffe', 'Wandas Club', 1),
        ('Jalan Braga', 'Toko Roti Sidodadi', 4),
        ('Toko Roti Sidodadi', 'Warung Bu Imas', 3),
        ('Kurokoffe', 'Harmony Dimsum', 16),
        ('Warung Bu Imas', 'Ramen Bajuri (Lengkong)', 4),

        # [PENAMBAHAN] 4 Edge baru dari Anda
        ('Kurokoffe', 'Pipinos Bakery', 3),
        ('Pipinos Bakery', 'Warung Sate Bu Ngantuk', 3),
        ('Kurokoffe', 'Warung Sate Bu Ngantuk', 2),
        ('Mie Soobek', 'Iga Bakar Si Jangkung', 14),

        # [PENAMBAHAN] 8 Edge baru dari data "Google Maps" untuk konektivitas
        ('Sudirman Street Bandung', 'Waroeng Lokal', 7),
        ('Dimsum Sembilan Ayam', 'Waroeng Lokal', 8),
        ('Five Monkeys Burger', 'Sate Jando Belakang Gd Sate', 5),
        ('Mie Soobek', 'Pipinos Bakery', 12),
        ('Iga Bakar Si Jangkung', 'Kedai Roti Ibu Saya', 10),
        ('Jonn & Sons', 'Harmony Dimsum', 5),
        ('Wandas Club', 'Jonn & Sons', 3),
    ]

    for u, v, w in edges: G.add_edge(u, v, weight=w)
    
    return G

# --- TAHAP 3: LOGIKA INTI ALGORITMA ---
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

    while current != end:
        competitors = remaining_nodes | {end}
        best_next_stop, best_score = None, float('inf')

        for competitor in competitors:
            if competitor not in graph: continue
            
            dist_curr_comp = dijkstra(graph, current, competitor)
            dist_comp_end = dijkstra(graph, competitor, end)
            
            if dist_curr_comp == float('inf') or dist_comp_end == float('inf'):
                score = float('inf')
            else:
                service_time = graph.nodes[competitor].get('waktu_layanan', 0)
                price = graph.nodes[competitor].get('biaya', 0)

                time_if_chosen = current_time_spent + segment_time + dist_curr_comp + service_time
                cost_if_chosen = current_cost_spent + segment_cost + price
                
                time_to_reach_segment_end = time_if_chosen + dist_comp_end
                
                if time_to_reach_segment_end > TIME_BUDGET or cost_if_chosen > MONEY_BUDGET:
                    score = float('inf')
                else:
                    score = (alpha * dist_curr_comp) + (beta * dist_comp_end)

            if score < best_score:
                best_score, best_next_stop = score, competitor

        if best_next_stop is None or best_score == float('inf'):
            best_next_stop = end
            
            travel_time_to_end = dijkstra(graph, current, end)
            if travel_time_to_end == float('inf') or (current_time_spent + segment_time + travel_time_to_end > TIME_BUDGET):
                 return [start], 0.0, 0.0, f"Gagal: Anggaran waktu/rute tidak cukup untuk mencapai '{end}'."

        path.append(best_next_stop)
        travel_time_to_stop = dijkstra(graph, current, best_next_stop)
        segment_time += travel_time_to_stop
        
        current = best_next_stop
        
        # =============================================== #
        #              BLOK KRUSIAL YANG BENAR            #
        # =============================================== #
        # Hanya tambahkan biaya/waktu jika BUKAN tujuan akhir segmen ('end')
        if current != end:
            segment_time += graph.nodes[current].get('waktu_layanan', 0)
            segment_cost += graph.nodes[current].get('biaya', 0)
            
            if current in remaining_nodes:
                remaining_nodes.remove(current)
        # =============================================== #
        
        if current == end:
            break
            
    # Mengembalikan HANYA waktu tempuh total segmen + biaya/waktu stopover
    return path, segment_time, segment_cost, "Sukses"

def final_tour_algorithm(graph, start, must_visit, end, TIME_BUDGET, MONEY_BUDGET):
    unvisited_must_visit = set(must_visit)
    final_tour, current_pos = [start], start
    
    total_time = graph.nodes[start].get('waktu_layanan', 0)
    total_cost = graph.nodes[start].get('biaya', 0)
    
    log_messages = [
        f"Anggaran Waktu: {TIME_BUDGET} menit ({TIME_BUDGET/60:.1f} jam)",
        f"Anggaran Biaya: Rp {MONEY_BUDGET:,.0f}",
        f"Status Awal: Waktu={int(total_time)} menit, Biaya=Rp {total_cost:,.0f}\n" + "="*30
    ]

    while unvisited_must_visit:
        reachable_must_visit = {
            dest for dest in unvisited_must_visit 
            if dijkstra(graph, current_pos, dest) != float('inf')
        }
        
        if not reachable_must_visit:
            log_messages.append(f"-> ❌ PERINGATAN: Tidak ada lokasi wajib terjangkau dari '{current_pos}'.")
            unvisited_must_visit.clear()
            continue

        next_destination = min(reachable_must_visit, key=lambda dest: dijkstra(graph, current_pos, dest))
        unvisited_must_visit.remove(next_destination)
        
        log_messages.append(f"\nMerencanakan segmen: '{current_pos}' -> '{next_destination}'")
        
        travel_time_to_dest = dijkstra(graph, current_pos, next_destination)
        service_time_dest = graph.nodes[next_destination].get('waktu_layanan', 0)
        price_dest = graph.nodes[next_destination].get('biaya', 0)

        if (total_time + travel_time_to_dest + service_time_dest > TIME_BUDGET) or \
           (total_cost + price_dest > MONEY_BUDGET):
            log_messages.append(f"-> ❌ GAGAL: Anggaran tidak cukup untuk lokasi wajib '{next_destination}'.")
            continue

        nodes_to_consider = set(graph.nodes()) - set(final_tour) - unvisited_must_visit
        
        segment, seg_time, seg_cost, status = find_progressive_enriched_path(
            graph, current_pos, next_destination, nodes_to_consider,
            total_time, total_cost, TIME_BUDGET, MONEY_BUDGET
        )
        
        if status != "Sukses" or len(segment) <= 1:
            log_messages.append(f"-> ❌ GAGAL: {status}")
            return final_tour, total_time, total_cost, log_messages

        final_tour.extend(segment[1:])
        
        # =============================================== #
        #          LOGIKA PENAMBAHAN BIAYA YANG BENAR     #
        # =============================================== #
        # seg_time = total waktu tempuh + total waktu layanan stopover
        # seg_cost = total biaya stopover
        
        total_time += seg_time # Tambahkan waktu tempuh + layanan stopover
        total_cost += seg_cost # Tambahkan biaya stopover
        
        # Tambahkan waktu layanan & biaya dari tujuan segmen ('must_visit' node)
        if current_pos != next_destination: # Pastikan kita benar-benar bergerak
            total_time += graph.nodes[next_destination].get('waktu_layanan', 0)
            total_cost += graph.nodes[next_destination].get('biaya', 0)
        # =============================================== #
        
        log_messages.append(f"-> Rute Ditemukan: {' → '.join(segment[1:])}")
        log_messages.append(f"   Status Anggaran: Waktu={int(total_time)} menit, Biaya=Rp {total_cost:,.0f}")
        
        current_pos = next_destination

    log_messages.append(f"\nMerencanakan segmen akhir: '{current_pos}' -> '{end}'")
    
    if dijkstra(graph, current_pos, end) == float('inf'):
        log_messages.append(f"-> ❌ GAGAL: Tujuan akhir '{end}' tidak terjangkau dari '{current_pos}'.")
        return final_tour, total_time, total_cost, log_messages

    nodes_to_consider = set(graph.nodes()) - set(final_tour)
    
    segment, seg_time, seg_cost, status = find_progressive_enriched_path(
        graph, current_pos, end, nodes_to_consider,
        total_time, total_cost, TIME_BUDGET, MONEY_BUDGET
    )
    
    if status == "Sukses" and len(segment) > 1:
        final_tour.extend(segment[1:])
        total_time += seg_time # 'seg_time' sudah termasuk waktu tempuh
        total_cost += seg_cost # 'seg_cost' sudah termasuk biaya stopover (jika ada)
        # Kita TIDAK menambahkan biaya/waktu 'end' node (tujuan akhir tur), sesuai asumsi.
        log_messages.append(f"-> Rute Ditemukan: {' → '.join(segment[1:])}")
    elif status != "Sukses":
        log_messages.append(f"-> ❌ GAGAL: {status}")

    unique_tour = []
    for loc in final_tour:
        if not unique_tour or unique_tour[-1] != loc:
            unique_tour.append(loc)
            
    return unique_tour, total_time, total_cost, log_messages

# --- TAHAP 4: FUNGSI VISUALISASI ---
def visualize_tour(graph, tour, start_point, end_point, total_time_spent, total_cost_spent, ax):
    ax.clear() 
    pos = nx.get_node_attributes(graph, 'pos')
    
    title = (
        f"Rute Tur dari {start_point} ke {end_point}\n"
        f"Total Waktu: {int(total_time_spent)} menit ({total_time_spent/60:.1f} jam) | "
        f"Total Biaya: Rp {total_cost_spent:,.0f}"
    )
    ax.set_title(title, fontsize=10, fontweight='bold')

    # Periksa apakah 'pos' ada sebelum menggambar
    if not pos:
        ax.text(0.5, 0.5, "Data posisi tidak tersedia.", ha='center', va='center')
        return

    nx.draw_networkx_nodes(graph, pos, node_color='lightgray', node_size=500, ax=ax)
    
    labels_to_draw = {n: '\n'.join(textwrap.wrap(n, 12)) for n in graph.nodes() if n in pos}
    nx.draw_networkx_labels(graph, pos, font_size=6, font_weight='bold', ax=ax,
                            labels=labels_to_draw)
    
    nx.draw_networkx_edges(graph, pos, width=1, alpha=0.3, ax=ax)

    edge_weights = nx.get_edge_attributes(graph, 'weight')
    # Filter edge_weights hanya untuk edge yang nodenya ada di 'pos'
    valid_edge_weights = {(u, v): w for (u, v), w in edge_weights.items() if u in pos and v in pos}
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=valid_edge_weights, font_size=7, ax=ax, label_pos=0.3)

    tour_nodes = set(tour)
    node_colors = {node: ('gold' if node in tour_nodes else 'lightgray') for node in graph.nodes()}
    
    # === PERUBAHAN DI SINI ===
    if start_point in graph.nodes():
        node_colors[start_point] = '#F57C00' # Diubah dari 'lightgreen'
    if end_point in graph.nodes():
        node_colors[end_point] = 'lightcoral'
    # =========================
    
    # Filter node colors hanya untuk node yang ada di 'pos'
    nodes_with_pos = list(pos.keys())
    filtered_node_colors = [node_colors.get(node, 'lightgray') for node in nodes_with_pos]
    nx.draw_networkx_nodes(graph, pos, nodelist=nodes_with_pos, node_color=filtered_node_colors, node_size=600, ax=ax)


    if len(tour) > 1:
        # Filter tour_edges hanya untuk edge yang kedua nodenya ada di 'pos'
        valid_tour_edges = [(u, v) for u, v in zip(tour[:-1], tour[1:]) if u in pos and v in pos]
        nx.draw_networkx_edges(graph, pos, edgelist=valid_tour_edges,
                              width=2.0, edge_color='#F57C00', arrows=True, arrowsize=15, ax=ax)
    
    for i, node in enumerate(tour):
        if node in pos:
            x, y = pos[node]
            ax.text(x, y + 25, f'#{i+1}', fontsize=8, fontweight='bold', color='darkred', ha='center',
                    bbox=dict(boxstyle='circle,pad=0.2', facecolor='white', alpha=0.6))
    
    # === PERUBAHAN DI SINI ===
    legend_elements = [ plt.Line2D([0], [0], marker='o', color='w', label='Start', markerfacecolor='#F57C00', ms=10), # Diubah
                        plt.Line2D([0], [0], marker='o', color='w', label='End', markerfacecolor='lightcoral', ms=10),
                        plt.Line2D([0], [0], marker='o', color='w', label='Dikunjungi', markerfacecolor='gold', ms=10),
                        plt.Line2D([0], [0], color='#F57C00', lw=2, label='Rute Tur')]
    # =========================
    
    ax.legend(handles=legend_elements, loc='upper right', fontsize=8)
    try: # Gunakan try-except untuk mencegah error jika figure belum siap
      ax.figure.tight_layout()
    except Exception as e:
      print(f"Warning: Could not apply tight_layout: {e}")