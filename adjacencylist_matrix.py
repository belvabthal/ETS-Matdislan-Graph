import networkx as nx
import numpy as np
import sys

# --- TAHAP 1: Impor Model Graf ---
# Kita mengimpor fungsi pembuat graf dari file utama Anda.
# [RALAT] Nama file dipastikan 'progresive_enriched_end0.py'
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
    """
    Fungsi ini mengambil objek graf NetworkX dan mencetak
    dua representasi formalnya: Adjacency List dan Adjacency Matrix.
    Ini adalah inti dari 'Pemodelan dan Analisis Awal'.
    """

    print("======================================================")
    print("      PEMODELAN & ANALISIS AWAL GRAF KULINER")
    print("        (Data: progresive_enriched_end0.py)")
    print("======================================================")
    
    # Mendefinisikan urutan simpul yang konsisten
    # Ini akan mencakup simpul dari 'locations_data' DAN 'Stasiun Bandung'
    node_list = list(graph.nodes())

    # --- 1. Adjacency List (Konektivitas Dasar) ---
    print("\n[ Tahap 1: Adjacency List (Konektivitas Dasar) ]\n")
    print("Ini memodelkan 'Simpul mana terhubung ke mana?'")
    
    for i, node_name in enumerate(node_list):
        # Mengambil daftar tetangga (neighbors) untuk setiap simpul
        neighbors = list(graph.neighbors(node_name))
        
        # Format nama simpul agar rapi
        nama_simpul_terpotong = (node_name[:28] + '..') if len(node_name) > 28 else node_name
        
        print(f"Simpul [{i:02d}] ({nama_simpul_terpotong}):")
        
        # Cetak tetangganya dengan rapi
        if neighbors:
            for neighbor in neighbors:
                print(f"          -> {neighbor}")
        else:
            print("          (Tidak ada koneksi)")
        print("-" * 35) # Pemisah antar simpul

    # --- 2. Adjacency Matrix (Bobot = Waktu Tempuh) ---
    print("\n[ Tahap 2: Adjacency Matrix (Bobot = Waktu Tempuh) ]\n")
    print("Ini memodelkan 'Berapa lama perjalanan antar simpul?'")
    print("Nilai M[i][j] = waktu tempuh dari simpul i ke simpul j.")
    print("Nilai 0 berarti tidak ada koneksi *langsung*.\n")

    # Membuat Adjacency Matrix menggunakan NumPy
    # 'nodelist' memastikan urutan baris/kolom matriks sama dengan daftar di atas
    # 'weight='weight'' memberi tahu networkx untuk mengisi matriks dengan atribut 'weight' (waktu tempuh)
    # 'dtype=int' membuat angkanya rapi (integer)
    adj_matrix = nx.to_numpy_array(graph, nodelist=node_list, weight='weight', dtype=int)

    # Mencetak daftar urutan simpul untuk referensi matriks
    print("--- Urutan Simpul (Indeks Matriks) ---")
    for i, node_name in enumerate(node_list):
        print(f"[{i:02d}] = {node_name}")
    print("--- (Akhir Urutan Simpul) ---\n")

    # Mencetak matriksnya
    print("--- Adjacency Matrix (M) ---")
    # Mengatur opsi cetak NumPy agar seluruh matriks ditampilkan (tidak terpotong)
    # 'suppress=True' membuat cetakan angka lebih rapi
    np.set_printoptions(threshold=np.inf, linewidth=np.inf, suppress=True)
    
    # Mencetak header kolom (indeks 0 - 23, karena ada 24 simpul)
    header = "Idx   " + " ".join([f"{i:2d}" for i in range(len(node_list))])
    print(header)
    print("----  " + "---" * len(node_list))

    # Mencetak baris matriks dengan indeks barisnya
    for i, row in enumerate(adj_matrix):
        row_str = " ".join([f"{val:2d}" for val in row])
        print(f"[{i:02d}] | {row_str}")
        
    print("--- (Akhir Adjacency Matrix) ---")
    print("\n======================================================")


def main():
    # Buat graf persis seperti di program utama Anda
    # [RALAT] Fungsi ini hanya mengembalikan G (graf)
    G = create_bandung_culinary_graph()
    
    # Panggil fungsi untuk menampilkan model formalnya
    tampilkan_representasi_formal(G)

if __name__ == "__main__":
    main()