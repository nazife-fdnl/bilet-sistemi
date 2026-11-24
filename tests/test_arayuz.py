"""Arayüz testleri: menü, koltuk haritası ve hazır senaryolar."""

import unittest
from datetime import date
from typing import List

from bilet_sistemi.arayuz import (
    KomutSatiriArayuzu,
    kalip_turu,
    koltuk_haritasi,
    kullanici_demosu,
    senaryo_girdisi,
)
from bilet_sistemi.salon import salon_olustur
from bilet_sistemi.uygulama import ornek_gise

BUGUN = date(2026, 11, 24)


def calistir(adimlar: List[str]):
    """Arayüzü verilen cevaplarla çalıştırır; (gişe, tüm çıktı) döndürür."""
    satirlar: List[str] = []
    gise = ornek_gise(BUGUN)
    KomutSatiriArayuzu(gise, senaryo_girdisi(adimlar, satirlar.append), satirlar.append).calistir()
    return gise, "\n".join(satirlar)


class KoltukHaritasiTestleri(unittest.TestCase):

    def test_harita_durum_simgelerini_gosterir(self) -> None:
        salon = salon_olustur("Test", {"A": (1, 3)})
        salon.koltuk_bul("A-1-2").tut()
        salon.koltuk_bul("A-1-3").sat()
        harita = koltuk_haritasi(salon)
        self.assertIn("boş 1 / 3", harita)
        satir = [s for s in harita.splitlines() if s.strip().startswith("A-1")][0]
        self.assertEqual(satir.split()[1:], [".", "T", "X"])


class MenuTestleri(unittest.TestCase):

    def test_cikis(self) -> None:
        _, cikti = calistir(["0"])
        self.assertIn("Güle güle!", cikti)

    def test_girdi_bitince_program_kapanir(self) -> None:
        _, cikti = calistir([])
        self.assertIn("Güle güle!", cikti)

    def test_etkinlik_listesi(self) -> None:
        _, cikti = calistir(["1", "0"])
        for metin in ("Rock Gecesi", "Hamlet", "Yazılım Mimarisi Zirvesi"):
            self.assertIn(metin, cikti)

    def test_bilet_satin_alma_akisi(self) -> None:
        gise, cikti = calistir(["3", "K1", "B-1-3", "3", "1,3", "E", "0"])
        self.assertIn("Tutar : 1045.00 TL", cikti)
        self.assertIn("Satış tamamlandı. Satış no: 1", cikti)
        self.assertEqual(gise.koltuk_bul("K1", "B-1-3").durum_adi, "Satıldı")

    def test_onaylanmayan_satis_yapilmaz(self) -> None:
        gise, cikti = calistir(["3", "K1", "A-1-1", "1", "", "H", "0"])
        self.assertIn("Satın alma iptal edildi.", cikti)
        self.assertEqual(gise.satislar(), [])
        self.assertEqual(gise.koltuk_bul("K1", "A-1-1").durum_adi, "Boş")

    def test_tut_ve_birak(self) -> None:
        gise, cikti = calistir(["4", "F1", "A-1-5", "5", "F1", "A-1-5", "0"])
        self.assertIn("A-1-5 koltuğu tutuldu.", cikti)
        self.assertIn("A-1-5 koltuğu bırakıldı", cikti)
        self.assertEqual(gise.koltuk_bul("F1", "A-1-5").durum_adi, "Boş")

    def test_iptal_ve_rapor(self) -> None:
        _, cikti = calistir(["3", "T1", "P-2-4", "2", "", "E", "6", "1", "7", "0"])
        self.assertIn("1 numaralı satış iptal edildi", cikti)
        self.assertIn("İPTAL", cikti)
        self.assertIn("Toplam ciro: 0.00 TL", cikti)

    def test_hatalar_programi_durdurmaz(self) -> None:
        _, cikti = calistir(["9", "2", "X9", "3", "K1", "A-1-1", "7", "0"])
        self.assertIn("Geçersiz seçim", cikti)
        self.assertIn("Hata: 'X9' kodlu etkinlik yok.", cikti)
        self.assertIn("Hata: 1-4 arası bir tarife numarası girin.", cikti)
        self.assertIn("Güle güle!", cikti)

    def test_gecersiz_ekstra_numarasi(self) -> None:
        gise, cikti = calistir(["3", "K1", "A-1-1", "1", "1,7", "0"])
        self.assertIn("Hata: '7' geçerli bir ekstra numarası değil.", cikti)
        self.assertEqual(gise.satislar(), [])

    def test_rakam_benzeri_karakterler_programi_cokertmez(self) -> None:
        _, cikti = calistir(["6", "²", "3", "K1", "A-1-1", "²", "0"])
        self.assertIn("Hata: Satış numarası bir sayı olmalı.", cikti)
        self.assertIn("Hata: 1-4 arası bir tarife numarası girin.", cikti)
        self.assertIn("Güle güle!", cikti)

    def test_satilmis_koltuk_icin_teklif_verilmez(self) -> None:
        gise, cikti = calistir(["3", "K1", "A-1-1", "1", "", "E",
                                "3", "K1", "A-1-1", "0"])
        self.assertIn("Hata: A-1-1: koltuk satılamaz (durum: Satıldı).", cikti)
        self.assertEqual(cikti.count("Tutar : "), 1)
        self.assertEqual(len(gise.satislar()), 1)

    def test_satis_numarasi_sayi_olmali(self) -> None:
        _, cikti = calistir(["6", "abc", "0"])
        self.assertIn("Hata: Satış numarası bir sayı olmalı.", cikti)


class DemoTestleri(unittest.TestCase):

    def test_kullanici_demosu_hatasiz_tamamlanir(self) -> None:
        satirlar: List[str] = []
        kullanici_demosu(satirlar.append, bugun=BUGUN)
        cikti = "\n".join(satirlar)
        self.assertIn("Satış tamamlandı. Satış no: 3", cikti)
        self.assertIn("Hata: B-1-3: satılmış koltuk tutulamaz.", cikti)
        self.assertIn("Toplam ciro: 507.50 TL", cikti)
        self.assertTrue(cikti.rstrip().endswith("Güle güle!"))

    def test_kalip_turu_hatasiz_tamamlanir(self) -> None:
        satirlar: List[str] = []
        kalip_turu(satirlar.append)
        cikti = "\n".join(satirlar)
        self.assertIn("Toplam: 797.50 TL", cikti)
        self.assertIn("Salon(Kültür Merkezi, 49/52 boş)", cikti)


if __name__ == "__main__":
    unittest.main()
