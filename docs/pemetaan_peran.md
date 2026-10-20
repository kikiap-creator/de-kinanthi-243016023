# Pemetaan peran Batik Kinanthi

| No | Kebutuhan pemilik Batik Kinanthi | Peran utama | Alasan singkat | Tahap lifecycle |
|---|---|---|---|---|
| 1 | Data penjualan dari toko, web, dan marketplace dikumpulkan ke satu tempat setiap malam | Data Engineer | Memindahkan dan menyatukan data dari banyak sumber secara otomatis | Ingestion |
| 2 | Dashboard omzet harian per kanal | Data Analyst | Menyajikan omzet dari tabel siap pakai dalam grafik yang dibaca pemilik setiap hari | Serving |
| 3 | Prediksi kebutuhan stok kain bulan depan | Data Scientist | Memprediksi kebutuhan dengan model peramalan dari riwayat penjualan | Serving |
| 4 | Tabel pelanggan tidak boleh berisi data ganda | Data Engineer | Menjaga kualitas data lewat pemeriksaan dan penghapusan duplikat di dalam pipeline | Transformation |
| 5 | Laporan motif terlaris per kota untuk rapat bulanan | Data Analyst | Menggabungkan data penjualan, produk, dan pelanggan menjadi ringkasan untuk rapat | Serving |
| 6 | Rekomendasi produk untuk pelanggan di situs web | Data Scientist | Membuat model rekomendasi dari pola pembelian pelanggan | Serving |
| 7 | Data transaksi lama tetap tersimpan aman dan hemat biaya | Data Engineer | Mengatur penyimpanan jangka panjang yang aman dan murah (retensi, enkripsi, backup) | Storage |
| 8 | Analisis penyebab penurunan penjualan marketplace bulan lalu | Data Analyst | Menelusuri penyebab dengan membandingkan periode, produk, dan harga untuk menjawab "mengapa" | Serving |

## Pertanyaan

### (a) Mengapa kebutuhan 3 dan 6 tidak bisa dikerjakan sebelum kebutuhan 1 dan 4 selesai?

Kebutuhan 3 (prediksi stok kain) dan kebutuhan 6 (rekomendasi produk) adalah pekerjaan Data Scientist. Modelnya dilatih dari riwayat penjualan dan pembelian, dan mutu model dibatasi oleh mutu data yang dipakai melatihnya. Karena itu dua kebutuhan hulu harus selesai lebih dulu.

Kebutuhan 1 menyediakan data yang utuh. Sebelum data toko, web, dan marketplace dikumpulkan ke satu tempat, riwayat penjualan tersebar di tiga sistem. Model yang hanya memakai satu kanal melihat sebagian kecil penjualan. Pada data latihan, toko menyumbang sekitar 29% omzet dan marketplace sekitar 51%, jadi model yang hanya memakai data toko akan meleset jauh saat memperkirakan kebutuhan kain.

Kebutuhan 4 menyediakan data pelanggan yang bersih. Kalau satu pelanggan tercatat ganda, riwayat pembeliannya terpecah menjadi dua profil. Rekomendasi produk bergantung pada riwayat per pelanggan, sehingga profil yang terpecah menghasilkan rekomendasi yang salah. Jumlah pelanggan yang menggembung juga mengacaukan perkiraan permintaan.

Urutan ini sama dengan posisi peran di tabel modul: Data Engineer berada di hulu, Data Scientist di hilir. Pekerjaan hilir hanya sebaik data yang diserahkan hulu.

### (b) Apa risiko satu orang merangkap tiga peran di UMKM, dan bagian apa yang sebaiknya diotomatisasi lebih dulu?

Risiko satu orang merangkap Data Engineer, Data Scientist, dan Data Analyst:

1. Pekerjaan rutin tercecer. Pengumpulan data malam hari harus berjalan setiap hari, sedangkan analisis dan model dikerjakan sesekali. Saat orang itu sibuk membangun model, pipeline tidak terawat dan data terlambat.
2. Satu titik kegagalan. Pengetahuan tentang pipeline hanya ada di satu orang. Kalau ia sakit atau berhenti, tidak ada yang bisa memperbaikinya.
3. Tidak ada pemeriksaan silang. Orang yang sama membuat data dan membacanya, sehingga kesalahan seperti data ganda mudah lolos tanpa terlihat.
4. Hak akses terlalu luas. Satu akun memegang semua hak, padahal prinsip hak akses minimum menyarankan akun terpisah untuk tiap peran (lihat baris Security di `undercurrents.md`).
5. Kedalaman keahlian menurun. Tiga bidang sekaligus sulit dikuasai, sehingga mutu tiap pekerjaan turun.

Bagian yang sebaiknya diotomatisasi lebih dulu adalah pengumpulan data harian (kebutuhan 1) beserta pemeriksaan kualitasnya (kebutuhan 4). Keduanya paling sering berulang, paling mudah salah bila dikerjakan manual, dan menjadi dasar semua pekerjaan lain. Dashboard omzet harian (kebutuhan 2) mengikuti otomatis begitu tabel mart terisi setiap malam.

Pada Latihan 2, `pipeline_mini.py` sudah mengotomatiskan alur dan pemeriksaannya. Yang belum ada adalah penjadwalan, jadi langkah otomatisasi berikutnya adalah menjalankan pipeline itu setiap malam.
