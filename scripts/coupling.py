stok, analitik, email_terkirim = [], [], []
layanan_email = {"hidup": False}  # False = layanan email sedang down

def kurangi_stok(e): stok.append(e["id"])
def catat_analitik(e): analitik.append(e["id"])
def kirim_email(e):
    if e["id"] == 2 and not layanan_email["hidup"]:
        raise ConnectionError("layanan email down")
    email_terkirim.append(e["id"])
def cek_fraud(e):
    if e["id"] % 2 == 0:
        print(f"PERINGATAN: pesanan {e['id']} bernomor genap, perlu pemeriksaan fraud")

# Desain A: tightly coupled (order service memanggil semuanya langsung)
def buat_pesanan_tight(e):
    kurangi_stok(e); kirim_email(e); catat_analitik(e); cek_fraud(e)

# Desain B: loosely coupled (producer -> router -> consumer)
class Router:
    def __init__(self):
        self.pelanggan, self.dlq = {}, []
        self.handler = {}      # nama handler -> fungsi, dipakai oleh ulang_dlq
        self.selesai = set()   # kunci idempotensi: (nama handler, id event) yang sudah berhasil

    def subscribe(self, topik, handler):
        self.pelanggan.setdefault(topik, []).append(handler)
        self.handler[handler.__name__] = handler

    def _jalankan(self, h, event):
        kunci = (h.__name__, event["id"])
        if kunci in self.selesai:
            return True                    # efek ini sudah pernah diterapkan, lewati
        try:
            h(event)
        except Exception as err:
            self.dlq.append({"handler": h.__name__, "event": event, "error": str(err)})
            return False
        self.selesai.add(kunci)
        return True

    def publish(self, topik, event):
        for h in self.pelanggan.get(topik, []):
            self._jalankan(h, event)

    def ulang_dlq(self):
        """Coba ulang hanya handler yang gagal. Handler lain tidak dipanggil lagi."""
        antrean, self.dlq = self.dlq, []
        berhasil = 0
        for item in antrean:
            if self._jalankan(self.handler[item["handler"]], item["event"]):
                berhasil += 1
        return berhasil

router = Router()
for h in (kurangi_stok, kirim_email, catat_analitik, cek_fraud):
    router.subscribe("pesanan_baru", h)

print("== Desain A ==")
for i in (1, 2, 3):
    try:
        buat_pesanan_tight({"id": i}); print(f"pesanan {i}: sukses")
    except Exception as err:
        print(f"pesanan {i}: GAGAL ({err})")
print("stok:", stok, "| analitik:", analitik)

stok.clear(); analitik.clear(); email_terkirim.clear()

print("== Desain B ==")
for i in (1, 2, 3):
    router.publish("pesanan_baru", {"id": i}); print(f"pesanan {i}: diterima")
print("stok:", stok, "| analitik:", analitik)
print("dead-letter:", router.dlq)

print("== Tugas 5: ulang_dlq() ==")
print("email:", email_terkirim)
print("ulang saat email masih down :", router.ulang_dlq(), "berhasil | isi dlq:", len(router.dlq))
layanan_email["hidup"] = True
print("ulang setelah email pulih   :", router.ulang_dlq(), "berhasil | isi dlq:", len(router.dlq))
print("stok:", stok, "| analitik:", analitik, "| email:", email_terkirim)
print("ulang sekali lagi           :", router.ulang_dlq(), "berhasil | isi dlq:", len(router.dlq))
router.publish("pesanan_baru", {"id": 2})  # pengiriman ganda event 2
print("event 2 dikirim ulang      : stok:", stok, "| analitik:", analitik, "| email:", email_terkirim)