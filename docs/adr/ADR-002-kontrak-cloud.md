# ADR-002: Kontrak layanan cloud untuk data Batik Kinanthi

**Status**: disetujui

**Konteks**: Batik Kinanthi berencana memindahkan database dan penyimpanan datanya dari laptop ke layanan cloud agar data tiga kanal tersimpan aman dan bisa diakses pipeline setiap malam. Penyedia cloud menawarkan harga satuan lebih murah untuk komitmen yang lebih lama. Beban kerja UMKM ini belum stabil: baru ada satu pipeline dan pemakaian belum terukur.

**Opsi**:

| Opsi | Biaya | Latensi | Kompleksitas |
|---|---|---|---|
| A. Kontrak 3 tahun dengan komitmen penuh | Harga satuan terendah, tetapi tagihan komitmen tetap berjalan walau pemakaian turun dan keluar lebih awal kena penalti | Tidak berpengaruh | Rendah di awal, tetapi risiko keuangan terkunci tiga tahun |
| B. Kontrak 1 tahun dengan komitmen sebagian dari beban dasar | Harga satuan menengah, komitmen terbatas pada beban yang sudah terukur | Tidak berpengaruh | Sedang: perlu memantau pemakaian dan memutuskan perpanjangan |
| C. On-demand tanpa komitmen | Harga satuan tertinggi dan tagihan berubah-ubah | Tidak berpengaruh | Rendah, tetapi anggaran sulit diprediksi |

**Keputusan**: Opsi B. Pemakaian belum terukur, sehingga komitmen penuh tiga tahun mengunci biaya sebelum beban dasar diketahui. Kontrak satu tahun tetap lebih murah daripada on-demand tanpa mengunci terlalu lama. Opsi A ditinjau lagi saat perpanjangan, bila beban sudah stabil selama setahun.

**Tipe**: one-way. Selama masa kontrak, komitmen biaya tidak bisa dibatalkan tanpa penalti. Risikonya dibatasi dengan masa kontrak satu tahun dan komitmen sebagian.

**Konsekuensi**:

- Dampak: Biaya tahun pertama lebih rendah daripada on-demand untuk sebagian beban, dan lebih mudah dianggarkan.
- Risiko: Bila pemakaian turun di bawah komitmen, selisihnya tetap dibayar. Pemakaian layanan khusus penyedia juga dapat mengikat secara teknis (vendor lock-in).
- Exit plan: Komitmen hanya untuk beban dasar yang sudah terukur. Data disimpan dalam format terbuka (lihat ADR-001) dan diekspor rutin ke penyimpanan lain. Layanan khusus penyedia tanpa padanan dihindari. Pemakaian ditinjau tiga bulan sebelum kontrak berakhir untuk memutuskan perpanjangan atau pindah.
