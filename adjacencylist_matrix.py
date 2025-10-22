import networkx as nx
import numpy as np
import sys

try:
    from progresive_enriched_end0 import create_bandung_culinary_graph
except ImportError:
    print("="*60)
    print("ERROR: GAGAL MENGIMPOR")
    print("Pastikan file ini ('tampilkan_model_final.py')")
    print("berada di folder yang sama dengan 'progresive_enriched_end0.py'")
    print("="*60)
    sys.exit()

def tampilkan_representasi_formal(graph):
    print("======================================================")
    print("      PEMODELAN & ANALISIS AWAL GRAF KULINER")
    print("        (Data: progresive_enriched_end0.py)")
    print("======================================================")
    
    node_list = list(graph.nodes())

    # --- 1. Adjacency List (Konektivitas Dasar) ---
    print("\n[ Tahap 1: Adjacency List (Konektivitas Dasar) ]\n")
    print("Ini memodelkan 'Simpul mana terhubung ke mana?'")
    
    for i, node_name in enumerate(node_list):
        neighbors = list(graph.neighbors(node_name))
        
        nama_simpul_terpotong = (node_name[:28] + '..') if len(node_name) > 28 else node_name
        
        print(f"Simpul [{i:02d}] ({nama_simpul_terpotong}):")
        
        if neighbors:
            for neighbor in neighbors:
                print(f"          -> {neighbor}")
        else:
            print("          (Tidak ada koneksi)")
        print("-" * 35)

    # --- 2. Adjacency Matrix (Bobot = Waktu Tempuh) ---
    print("\n[ Tahap 2: Adjacency Matrix (Bobot = Waktu Tempuh) ]\n")
    print("Ini memodelkan 'Berapa lama perjalanan antar simpul?'")
    print("Nilai M[i][j] = waktu tempuh dari simpul i ke simpul j.")
    print("Nilai 0 berarti tidak ada koneksi *langsung*.\n")

    adj_matrix = nx.to_numpy_array(graph, nodelist=node_list, weight='weight', dtype=int)

    print("--- Urutan Simpul (Indeks Matriks) ---")
    for i, node_name in enumerate(node_list):
        print(f"[{i:02d}] = {node_name}")
    print("--- (Akhir Urutan Simpul) ---\n")

    print("--- Adjacency Matrix (M) ---")
    
    np.set_printoptions(threshold=np.inf, linewidth=np.inf, suppress=True)
    
    header = "Idx   " + " ".join([f"{i:2d}" for i in range(len(node_list))])
    print(header)
    print("----  " + "---" * len(node_list))

    for i, row in enumerate(adj_matrix):
        row_str = " ".join([f"{val:2d}" for val in row])
        print(f"[{i:02d}] | {row_str}")
        
    print("--- (Akhir Adjacency Matrix) ---")
    print("\n======================================================")


def main():
    G = create_bandung_culinary_graph()
    
    tampilkan_representasi_formal(G)

if __name__ == "__main__":
    main()