# Identifikasi undercurrents pada `pipeline_mini.py`

Nomor baris merujuk ke `scripts/pipeline_mini.py`. Baris Security adalah contoh dari modul.

| Undercurrent | Bukti penerapan di kode | Kekurangan | Usulan perbaikan |
|---|---|---|---|
| Security | Kredensial dibaca dari `.env` lewat `load_dotenv()` | Pipeline memakai user `de_user` yang punya hak penuh | Buat user khusus pipeline: hanya baca `transaksi`, tulis `mart_omzet_harian` |
| Data management | `check_quality()` (baris 34-45) memeriksa id ganda, total <= 0, dan kanal kosong. `store_raw()` (baris 26-31) menyimpan salinan mentah. | Tabel `transaksi` dibuat oleh `pandas.to_sql` tanpa primary key dan tanpa constraint. Database menerima total negatif pada INSERT di Latihan 2, jadi satu-satunya penjaga ada di kode pipeline. | Tambahkan primary key pada `id_transaksi` dan constraint `CHECK (total > 0)` langsung di tabel `transaksi` |
| DataOps | Log di setiap tahap lewat `logging` (baris 8-10, 22, 31, 45, 54, 61). Pemeriksaan kualitas berjalan otomatis dan menghentikan pipeline (baris 43-44). | Tidak ada tes otomatis. Kegagalan hanya terlihat di terminal, jadi tidak ada yang tahu bila pipeline dijalankan tanpa dipantau. | Tulis tes `pytest` untuk `check_quality()` dan `transform()`, lalu jalankan otomatis di GitHub Actions pada setiap push |
| Data architecture | Lima tahap dipisah menjadi fungsi `ingest`, `store_raw`, `check_quality`, `transform`, dan `serve` (baris 19-61), dengan alur sumber, `data/raw`, lalu `mart_omzet_harian`. | Salinan mentah berupa satu CSV lokal yang ditimpa setiap eksekusi, jadi riwayat hilang. | Simpan salinan mentah dengan nama berstempel waktu, misalnya di bucket `raw` pada MinIO, supaya tiap eksekusi punya arsip sendiri |
| Orchestration | `main()` (baris 64-72) memanggil lima tahap berurutan dan berhenti saat `check_quality()` gagal. | Pipeline dijalankan manual dari terminal, tanpa jadwal, retry, atau notifikasi, padahal kebutuhan pemilik adalah pengumpulan data setiap malam. | Jadwalkan pipeline setiap malam dengan orkestrator seperti Airflow (atau Task Scheduler untuk tahap awal), lengkap dengan retry dan notifikasi gagal |
| Software engineering | Fungsi kecil dengan satu tugas, type hint, docstring, jalur berkas lewat `pathlib` (baris 16), dan blok `if __name__ == "__main__"` (baris 75). | Nama tabel dan `RAW_DIR` tertanam di kode, dan `ingest()` (baris 21) selalu membaca seluruh tabel `transaksi`. | Pindahkan nama tabel dan jalur berkas ke modul konfigurasi terpisah, supaya fungsi bisa dipakai untuk tabel lain tanpa mengubah kodenya |

## Pertanyaan Sesi 2

### Mengapa `mart_omzet_harian` tetap aman saat data rusak masuk?

Karena di `main()` pemanggilan `check_quality()` berada sebelum `transform()` dan `serve()`. Ketika pemeriksaan melempar `ValueError`, eksekusi langsung keluar dari `main()` dan `serve()` tidak pernah dipanggil. Padahal `serve()` yang menulis ulang tabel mart lewat `to_sql(..., if_exists="replace")`. Selama gerbang kualitas tertutup, pengguna dashboard tetap melihat angka dari eksekusi terakhir yang sehat. Pada uji di Latihan 2, mart tetap 5.000 transaksi dan Rp12.508.975.000 setelah pipeline gagal, padahal tabel sumber sudah memuat baris rusak.

### `transaksi.csv` tetap diperbarui walaupun data rusak. Masalah atau berguna?

Menurut saya lebih berguna, dengan satu catatan. Salinan mentah apa adanya adalah bukti. Dari berkas itu saya bisa melihat baris mana yang rusak, kapan masuk, dan apakah masalahnya ada di sumber atau di pipeline, tanpa harus query ulang sumber yang mungkin sudah berubah. Setelah sumber diperbaiki, berkas yang sama bisa dipakai untuk menjalankan ulang pipeline.

Catatannya, berkas ini berisi data yang belum lolos validasi, jadi tidak boleh dipakai langsung untuk analisis. Pipeline juga menimpa berkas yang sama di setiap eksekusi, sehingga salinan rusak menggantikan salinan bersih terakhir dan riwayatnya hilang. Perbaikan yang masuk akal adalah menyimpan tiap eksekusi dengan nama berstempel waktu dan memindahkan data yang gagal ke folder terpisah, misalnya `quarantine/`.
