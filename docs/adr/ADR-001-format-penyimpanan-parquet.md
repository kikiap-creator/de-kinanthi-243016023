# ADR-001: Memilih Parquet sebagai format penyimpanan data analitik

**Status**: disetujui

**Konteks**: Pipeline Batik Kinanthi saat ini menyimpan salinan mentah transaksi sebagai CSV (`data/raw/transaksi.csv`). Data terus bertambah dari tiga kanal, dan lapisan analitik akan membacanya berulang kali untuk laporan omzet dan model prediksi. Format yang dipilih harus menjaga tipe kolom, hemat ruang, cepat dibaca per kolom, dan bisa dibuka oleh banyak alat seperti pandas, Spark, dan DuckDB.

**Opsi**:

| Opsi | Biaya | Latensi | Kompleksitas |
|---|---|---|---|
| A. CSV tetap | Tanpa biaya tambahan, tetapi ukuran file besar sehingga biaya simpan lebih tinggi | Seluruh baris dibaca walau hanya butuh beberapa kolom, lambat pada data besar | Terendah dan terbaca di editor teks, tetapi tipe data dan skema tidak terjaga |
| B. Parquet | File lebih kecil berkat kompresi per kolom | Hanya kolom yang diperlukan dibaca, cepat untuk agregasi seperti omzet per kanal | Sedang: butuh pustaka seperti `pyarrow` dan tidak terbaca di editor teks |
| C. Format tabel lakehouse (Delta Lake atau Apache Iceberg) | Sama dengan B ditambah penyimpanan metadata | Baik, dengan dukungan transaksi dan time travel | Tertinggi: butuh mesin dan katalog tambahan, berlebihan untuk satu pipeline kecil |

**Keputusan**: Opsi B, Parquet. Format ini menjaga skema dan tipe data, hemat ruang, dan cepat untuk kueri agregasi per kolom. Keputusannya juga mudah dibalik. Opsi C ditunda sampai ada kebutuhan pembaruan per baris atau time travel.

**Tipe**: two-way. Parquet adalah format terbuka. Mengubahnya kembali ke CSV atau format lain hanya perlu skrip pendek, jadi kesalahan memilih murah diperbaiki.

**Konsekuensi**:

- Dampak: File analitik lebih kecil, skema tertulis di dalam file, dan pembacaan per kolom lebih cepat.
- Risiko: Berkas tidak bisa dibuka di editor teks sehingga pemeriksaan manual perlu alat bantu. Versi `pyarrow` dan pandas harus dijaga kompatibel, dan perubahan skema perlu dikelola.
- Exit plan: Konversi ke CSV dengan `pd.read_parquet(...).to_csv(...)`. Akses data lewat satu fungsi baca dan tulis supaya penggantian format hanya menyentuh fungsi itu. CSV mentah dari sumber tetap disimpan sebagai cadangan.
