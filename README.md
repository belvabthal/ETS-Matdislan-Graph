# 🗺️ Optimasi Itinerary Kuliner Viral Bandung Menggunakan Algoritma Dijkstra dan Enrichment Path

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

Optimasi Itinerary Kuliner Viral Bandung Menggunakan Algoritma Dijkstra dan Enrichment Path adalah aplikasi desktop yang membantu Anda merencanakan tur wisata kuliner di Bandung secara optimal. Dengan menggunakan algoritma graf (Modified Dijkstra dan Progressive Pathfinding), aplikasi ini memberikan rekomendasi rute terbaik berdasarkan batasan waktu dan anggaran biaya Anda.

**Fitur Utama:**
- **23 Lokasi Wisata Kuliner** viral di Bandung
- **Budget-Aware Routing** dengan batasan waktu dan biaya
- **Must-Visit Points** untuk lokasi wajib kunjung
- **Interactive Visualization** menggunakan graf NetworkX
- **Modern GUI** dengan PyQt6

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
git clone https://github.com/belvabthal/ETS-Matdislan-Graph.git
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

1. **Set Starting Point**: Pilih lokasi awal perjalanan
2. **Set Destination**: Pilih lokasi tujuan akhir
3. **Set Budget**: Tentukan anggaran waktu (jam) dan biaya (Rupiah)
4. **Select Must-Visit** (Optional): Pilih lokasi yang wajib dikunjungi
5. **Plan Tour**: Klik tombol "Rencanakan Tur"
6. **View Results**: Lihat rute optimal dan visualisasi graf

---

## 📂 Project Structure

```
ETS-Matdislan-Graph/
│
├── progresive_enriched_end0.py      # Core logic: graf, algoritma, visualisasi
├── gui_sigma.py                     # PyQt6 GUI application
├── adjacencylist_matrix.py          # Demo adjacency representation
├── styles.qss                       # Dark mode stylesheet
├── LICENSE
└── README.md
```

---

## 🧠 Algorithm Overview

### Graph Model
- **Nodes**: 23 lokasi wisata dengan atribut posisi, waktu layanan, dan biaya
- **Edges**: Koneksi antar lokasi dengan bobot waktu tempuh (menit)

### Progressive Enriched Pathfinding
- Modified Dijkstra's algorithm untuk shortest path
- Heuristic weighting (α=0.7, β=0.3) untuk path optimization
- Budget validation untuk setiap langkah rute
- Multi-point routing dengan support must-visit locations

### Visualization
- NetworkX graph rendering dengan Matplotlib
- Color-coded nodes (start: Oranye, end: merah, visited: kuning)
- Route highlighting dengan numbered sequence
- Real-time budget tracking

---

## 🗺️ Available Locations

Aplikasi mencakup 23 lokasi wisata kuliner viral di Bandung:

**Area Pusat Kota & Selatan**: Waroeng Lokal, Dimsum Sembilan Ayam, Toko Roti Sidodadi, Sudirman Street Bandung, Warung Bu Imas, Ramen Bajuri, Makaroni Squad, Mie Naripan, Jalan Braga, Emperao Pizza

**Area Dago, Cihapit, Trunojoyo**: Drunk Baker, Bakmie Tjo Kin, Five Monkeys Burger, Sate Jando Belakang Gd Sate, Iga Bakar Si Jangkung, Kedai Roti Ibu Saya

**Area Sukajadi & Ciumbuleuit (Utara)**: Mie Soobek, Pipinos Bakery, Warung Sate Bu Ngantuk, Kurokoffe, Wandas Club, Jonn & Sons, Harmony Dimsum

---

## 🔧 Build Options

**Standard Run**
```bash
python gui_sigma.py
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

**241524035 - Belva Abthal Hidayat**  
**241524053 - Muhammad Fakhri Widodo**
**241524056 - Muhammad Zein Arridho**
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

**Made with ❤️ by Belva, Fakhri, Zein**

*"Jadikan perjalanan kulinermu di Bandung lebih efisien, hemat, dan menyenangkan!"*

[![GitHub](https://img.shields.io/badge/GitHub-Repository-blue?style=flat&logo=github)](https://github.com/belvabthal/ETS-Matdislan-Graph)

</div>