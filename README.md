# 🗺️ Bandung Culinary Tour Planner

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![NetworkX](https://img.shields.io/badge/NetworkX-3.0+-orange.svg)
![PyQt6](https://img.shields.io/badge/PyQt6-6.0+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

**Sistem Rekomendasi Rute Wisata Kuliner Bandung Berbasis Algoritma Graf**

Aplikasi pintar untuk merencanakan perjalanan kuliner di Bandung dengan optimasi waktu dan biaya menggunakan teori graf dan algoritma Dijkstra.

</div>

---

## 🎯 Overview

Bandung Culinary Tour Planner adalah aplikasi desktop yang membantu Anda merencanakan tur wisata kuliner di Bandung secara optimal. Dengan menggunakan algoritma graf (Modified Dijkstra dan Progressive Pathfinding), aplikasi ini memberikan rekomendasi rute terbaik berdasarkan batasan waktu dan anggaran biaya Anda.

**Fitur Utama:**
- **24 Lokasi Wisata Kuliner** populer di Bandung
- **Budget-Aware Routing** dengan batasan waktu dan biaya
- **Must-Visit Points** untuk lokasi wajib kunjung
- **Interactive Visualization** menggunakan graf NetworkX
- **Modern GUI** dengan PyQt6 dan dark mode theme

---

## 📋 Prerequisites

- **Python 3.8+**
- **pip** (Python package manager)

**Required Libraries:**
- NetworkX
- Matplotlib
- PyQt6

---

## 🛠️ Installation

**1. Clone the Repository**
```bash
git clone https://github.com/username/ETS-Matdislan-Graph.git
cd ETS-Matdislan-Graph
```

**2. Install Dependencies**
```bash
pip install networkx matplotlib pyqt6
```

**3. Run the Application**
```bash
python gui_sigma.py
```

---

## 🎮 How to Use

### GUI Mode (Recommended)

1. **Set Starting Point**: Pilih lokasi awal perjalanan
2. **Set Destination**: Pilih lokasi tujuan akhir
3. **Set Budget**: Tentukan anggaran waktu (jam) dan biaya (Rupiah)
4. **Select Must-Visit** (Optional): Pilih lokasi yang wajib dikunjungi
5. **Plan Tour**: Klik tombol "Rencanakan Tur"
6. **View Results**: Lihat rute optimal dan visualisasi graf

### CLI Mode

```bash
python progresive_enriched_end_not0.py
```

Ikuti instruksi di terminal untuk input. Hasil visualisasi akan disimpan sebagai `bandung_tour_kuliner_budget.png`.

---

## 📂 Project Structure

```
ETS-Matdislan-Graph/
│
├── progresive_enriched_end0.py      # Core logic: graf, algoritma, visualisasi
├── progresive_enriched_end_not0.py  # CLI version
├── gui_sigma.py                     # PyQt6 GUI application
├── adjacencylist_matrix.py          # Demo adjacency representation
├── styles.qss                       # Dark mode stylesheet
├── LICENSE
└── README.md
```

---

## 🧠 Algorithm Overview

### Graph Model
- **Nodes**: 24 lokasi wisata dengan atribut posisi, waktu layanan, dan biaya
- **Edges**: Koneksi antar lokasi dengan bobot waktu tempuh (menit)

### Progressive Enriched Pathfinding
- Modified Dijkstra's algorithm untuk shortest path
- Heuristic weighting (α=0.7, β=0.3) untuk path optimization
- Budget validation untuk setiap langkah rute
- Multi-point routing dengan support must-visit locations

### Visualization
- NetworkX graph rendering dengan Matplotlib
- Color-coded nodes (start: hijau, end: merah, visited: kuning)
- Route highlighting dengan numbered sequence
- Real-time budget tracking

---

## 🗺️ Available Locations

Aplikasi mencakup 24 lokasi wisata kuliner populer di Bandung:

**Area Pusat Kota**: Alun-Alun Bandung, Jalan Braga, Gedung Sate, Waroeng Lokal

**Area Trans Studio**: Trans Studio Bandung, Saung Angklung Udjo

**Area Dago**: Cihampelas Walk, Dago Pakar, Punclut, Museum Srihadi Soedarsono

**Area Lembang**: Floating Market, Farmhouse, De Ranch, Villa Niis, Sarae Hills

**Kuliner Spot**: Warung Sate Bu Ngantuk, Kurokoffe, Jonn & Sons, Pipinos Bakery, Ramen Bajuri

Dan masih banyak lagi...

---

## 🔧 Build Options

**Standard Run**
```bash
python gui_sigma.py
```

**CLI Version**
```bash
python progresive_enriched_end_not0.py
```

**Demo Graph Representation**
```bash
python adjacencylist_matrix.py
```

---

## 🐛 Troubleshooting

**ModuleNotFoundError**
```bash
pip install --upgrade networkx matplotlib pyqt6
```

**GUI tidak muncul**
- Pastikan running di environment yang support GUI
- Untuk WSL: Install X Server (VcXsrv, Xming)

**Stylesheet tidak load**
- Pastikan file `styles.qss` berada di direktori yang sama dengan `gui_sigma.py`

---

## 📜 License

Proyek ini dilisensikan di bawah **MIT License** - lihat file [LICENSE](LICENSE) untuk detail.

---

## 👤 Author


Politeknik Negeri Bandung  
2025

---

## 🙏 Acknowledgments

- **NetworkX** - Graph library untuk Python
- **Matplotlib** - Visualization library
- **PyQt6** - Modern GUI framework
- **Dosen Matematika Diskrit Lanjut** - Bimbingan dan inspirasi proyek

---

<div align="center">

**Made with ❤️ by ...**

*"Jadikan perjalanan kulinermu di Bandung lebih efisien, hemat, dan menyenangkan!"*

[![GitHub](https://img.shields.io/badge/GitHub-Repository-blue?style=flat&logo=github)](https://github.com/username/ETS-Matdislan-Graph)

</div>