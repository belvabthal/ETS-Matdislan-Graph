import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

def create_culinary_graph():
    """
    Membangun model Graf G = (V, E) untuk studi kasus kuliner Bandung.
    - Atribut Simpul (V): nama, waktu_layanan, estimasi_biaya
    - Bobot Sisi (E): waktu_tempuh
    """
    G = nx.Graph()

    # 1. Definisikan Atribut Simpul (Node Attributes)
    # (id, {dict_of_attributes})
    nodes_data = [
        (0, {'nama': 'Stasiun Bandung', 'waktu_layanan': 0, 'biaya': 0}),
        (1, {'nama': 'Sudirman Street', 'waktu_layanan': 75, 'biaya': 70000}),
        (2, {'nama': 'Kopi Purnama', 'waktu_layanan': 45, 'biaya': 45000}),
        (3, {'nama': 'Iga Bakar Si Jangkung', 'waktu_layanan': 60, 'biaya': 80000}),
        (4, {'nama': 'Seblak Sultan', 'waktu_layanan': 45, 'biaya': 30000}),
        (5, {'nama': 'Kue Balok Cihampelas', 'waktu_layanan': 20, 'biaya': 25000}),
        (6, {'nama': 'Hotel Cihampelas', 'waktu_layanan': 0, 'biaya': 0})
    ]
    G.add_nodes_from(nodes_data)

    # 2. Definisikan Sisi Berbobot (Weighted Edges)
    # (u, v, {weight_attribute: value})
    # Kita sebut bobotnya 'waktu_tempuh' agar jelas
    edges_data = [
        (0, 1, {'waktu_tempuh': 12}),
        (0, 2, {'waktu_tempuh': 15}),
        (0, 3, {'waktu_tempuh': 18}),
        (1, 2, {'waktu_tempuh': 10}),
        (2, 3, {'waktu_tempuh': 10}),
        (2, 4, {'waktu_tempuh': 20}),
        (3, 4, {'waktu_tempuh': 15}),
        (3, 5, {'waktu_tempuh': 10}),
        (4, 6, {'waktu_tempuh': 5}),
        (5, 6, {'waktu_tempuh': 3})
    ]
    G.add_edges_from(edges_data)
    
    return G

def print_graph_representations(graph):
    """
    Mencetak Adjacency List dan Adjacency Matrix
    Mirip dengan fungsi di Task03_Timproyek.py
    """
    print("--- (Tahap 2) Representasi Graf Formal ---")
    
    # 1. Adjacency List (Basic)
    print("\n[ Adjacency List (Konektivitas Dasar) ]")
    adj_list = nx.to_dict_of_lists(graph)
    node_names = nx.get_node_attributes(graph, 'nama')
    
    for node, neighbors in adj_list.items():
        nama_simpul = node_names[node]
        nama_tetangga = [node_names[n] for n in neighbors]
        print(f'Simpul [{node}] ({nama_simpul}): {nama_tetangga}')

    # 2. Adjacency Matrix (Berbobot)
    print("\n[ Adjacency Matrix (Bobot = Waktu Tempuh) ]")
    nodes = sorted(graph.nodes())
    # Kita gunakan 'waktu_tempuh' sebagai 'weight' untuk matriks
    adj_matrix = nx.to_numpy_array(graph, nodelist=nodes, weight='waktu_tempuh', dtype=int)
    
    print("Urutan Simpul:", nodes)
    print(adj_matrix)

def visualize_culinary_graph(graph):
    """
    Visualisasi dasar dari graf kuliner
    """
    plt.figure(figsize=(12, 9))
    
    # Ambil atribut untuk label
    pos = nx.spring_layout(graph, seed=42)
    node_labels = nx.get_node_attributes(graph, 'nama')
    edge_labels = nx.get_edge_attributes(graph, 'waktu_tempuh')
    
    nx.draw_networkx_nodes(graph, pos, node_color='skyblue', node_size=2500)
    nx.draw_networkx_labels(graph, pos, labels=node_labels, font_size=9, font_weight='bold')
    nx.draw_networkx_edges(graph, pos, edge_color='gray', width=2)
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_color='red')
    
    plt.title("Visualisasi Graf Kuliner Bandung (Tahap 2)", size=16)
    plt.axis('off') # Matikan sumbu
    plt.savefig('graf_kuliner_tahap2.png')
    print("\nVisualisasi graf disimpan sebagai 'graf_kuliner_tahap2.png'")


# --- Main Execution ---
if __name__ == "__main__":
    # 1. Buat Graf
    G_kuliner = create_culinary_graph()
    
    # 2. Cetak Representasi (Sesuai Tahap 2)
    print_graph_representations(G_kuliner)
    
    # 3. Visualisasi (Sesuai Tahap 4, tapi baik untuk cek)
    visualize_culinary_graph(G_kuliner)