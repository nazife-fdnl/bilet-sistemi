"""Uygulama katmanı testleri: BiletGisesi üzerinden uçtan uca satış işlemleri."""

import unittest
from datetime import date
from decimal import Decimal

from bilet_sistemi.hatalar import BulunamadiHatasi, GecersizIslemHatasi, GecersizSecimHatasi
from bilet_sistemi.uygulama import EKSTRALAR, TARIFELER, ornek_gise

BUGUN = date(2026, 11, 24)


class OrnekVeriTestleri(unittest.TestCase):

    def setUp(self) -> None:
        self.gise = ornek_gise(BUGUN)

    def test_uc_etkinlik_ve_kapasiteleri(self) -> None:
        ozet = {e.kod: (e.tur, e.salon.kapasite()) for e in self.gise.etkinlikler()}
        self.assertEqual(ozet, {"K1": ("Konser", 56), "T1": ("Tiyatro", 48), "F1": ("Konferans", 50)})

    def test_kalan_gunler(self) -> None:
        kalan = {e.kod: e.kalan_gun(BUGUN) for e in self.gise.etkinlikler()}
        self.assertEqual(kalan, {"K1": 45, "T1": 20, "F1": 60})

    def test_tarife_ve_ekstra_kodlari(self) -> None:
        self.assertEqual(list(TARIFELER), ["standart", "ogrenci", "erken", "kurumsal"])
        self.assertEqual(list(EKSTRALAR), ["vip", "otopark", "sigorta"])


class SatisTestleri(unittest.TestCase):

    def setUp(self) -> None:
        self.gise = ornek_gise(BUGUN)

    def test_satin_al_koltugu_satar_ve_kayit_olusturur(self) -> None:
        satis = self.gise.satin_al("K1", "A-1-1")
        self.assertEqual(satis.no, 1)
        self.assertEqual(satis.tutar, Decimal("500.00"))
        self.assertEqual(satis.tarife, "Standart")
        self.assertEqual(satis.koltuk.durum_adi, "Satıldı")
        self.assertEqual(self.gise.etkinlik_bul("K1").salon.bos_koltuk_sayisi(), 55)

    def test_satis_numaralari_artarak_verilir(self) -> None:
        self.assertEqual(self.gise.satin_al("K1", "A-1-1").no, 1)
        self.assertEqual(self.gise.satin_al("T1", "P-1-1").no, 2)

    def test_kodlar_buyuk_kucuk_harf_ve_bosluk_duyarsizdir(self) -> None:
        satis = self.gise.satin_al(" k1 ", " a-1-1 ")
        self.assertEqual(satis.koltuk.kod, "A-1-1")

    def test_vip_erken_kayit_vip_giris_ve_sigorta(self) -> None:
        # 500 x 2 (VIP blok) = 1000; erken kayıt %20 -> 800; +150 VIP -> 950; sigorta %10 -> 1045
        satis = self.gise.satin_al("K1", "B-1-3", "erken", ["vip", "sigorta"])
        self.assertEqual(satis.tutar, Decimal("1045.00"))
        self.assertEqual(satis.ekstralar, ["vip", "sigorta"])
        self.assertTrue(satis.bilet.aciklama().endswith("+ VIP giriş + İptal sigortası"))

    def test_erken_kayit_otuz_gunden_az_kalan_etkinlikte_indirim_yapmaz(self) -> None:
        # Tiyatroya 20 gün var; 2. sıra ön sıra: 300 x 1.25 = 375
        self.assertEqual(self.gise.satin_al("T1", "P-2-1", "erken").tutar, Decimal("375.00"))

    def test_tiyatro_ogrenci(self) -> None:
        self.assertEqual(self.gise.satin_al("T1", "P-2-4", "ogrenci").tutar, Decimal("262.50"))

    def test_konferans_kurumsal_otopark(self) -> None:
        # 200 x 0.85 = 170; +75 otopark = 245
        self.assertEqual(self.gise.satin_al("F1", "A-1-5", "kurumsal", ["otopark"]).tutar, Decimal("245.00"))

    def test_satis_tutari_satis_aninda_sabitlenir(self) -> None:
        from bilet_sistemi.ekstra import VipGiris
        satis = self.gise.satin_al("K1", "A-1-2", "standart", ["vip"])
        self.assertEqual(satis.tutar, Decimal("650.00"))
        eski = VipGiris.UCRET
        try:
            VipGiris.UCRET = Decimal("200")  # sonradan fiyat değişikliği
            self.assertEqual(satis.tutar, Decimal("650.00"))
            self.assertEqual(self.gise.toplam_ciro(), Decimal("650.00"))
        finally:
            VipGiris.UCRET = eski

    def test_fiyat_teklifi_koltugu_degistirmez(self) -> None:
        teklif = self.gise.fiyat_teklifi("K1", "A-1-1", "ogrenci", ["otopark"])
        self.assertEqual(teklif.fiyat(), Decimal("425.00"))
        self.assertEqual(self.gise.koltuk_bul("K1", "A-1-1").durum_adi, "Boş")
        self.assertEqual(self.gise.satislar(), [])

    def test_tutulan_koltuk_satilabilir(self) -> None:
        self.gise.koltuk_tut("F1", "A-1-5")
        self.assertEqual(self.gise.koltuk_bul("F1", "A-1-5").durum_adi, "Tutuldu")
        self.gise.satin_al("F1", "A-1-5")
        self.assertEqual(self.gise.koltuk_bul("F1", "A-1-5").durum_adi, "Satıldı")

    def test_tutulan_koltuk_birakilabilir(self) -> None:
        self.gise.koltuk_tut("F1", "A-1-5")
        self.gise.koltuk_birak("F1", "A-1-5")
        self.assertEqual(self.gise.koltuk_bul("F1", "A-1-5").durum_adi, "Boş")

    def test_satilmis_koltuk_tekrar_satilamaz_ve_kayit_olusmaz(self) -> None:
        self.gise.satin_al("K1", "A-1-1")
        with self.assertRaises(GecersizIslemHatasi):
            self.gise.satin_al("K1", "A-1-1")
        self.assertEqual(len(self.gise.satislar()), 1)


class IptalVeRaporTestleri(unittest.TestCase):

    def setUp(self) -> None:
        self.gise = ornek_gise(BUGUN)
        self.gise.satin_al("K1", "B-1-3", "erken", ["vip", "sigorta"])  # 1045.00
        self.gise.satin_al("T1", "P-2-4", "ogrenci")                     # 262.50
        self.gise.satin_al("F1", "A-1-5", "kurumsal", ["otopark"])       # 245.00

    def test_toplam_ciro(self) -> None:
        self.assertEqual(self.gise.toplam_ciro(), Decimal("1552.50"))

    def test_iptal_koltugu_bosaltir_ve_ciroyu_dusurur(self) -> None:
        satis = self.gise.satis_iptal(1)
        self.assertTrue(satis.iptal_edildi)
        self.assertEqual(satis.koltuk.durum_adi, "Boş")
        self.assertEqual(self.gise.toplam_ciro(), Decimal("507.50"))
        self.assertEqual(len(self.gise.satislar()), 2)
        self.assertEqual(len(self.gise.satislar(iptaller_dahil=True)), 3)

    def test_ayni_satis_iki_kez_iptal_edilemez(self) -> None:
        self.gise.satis_iptal(2)
        with self.assertRaises(GecersizIslemHatasi):
            self.gise.satis_iptal(2)

    def test_iptal_edilen_koltuk_yeniden_satilabilir(self) -> None:
        self.gise.satis_iptal(1)
        self.assertEqual(self.gise.satin_al("K1", "B-1-3").no, 4)

    def test_etkinlik_ozeti(self) -> None:
        self.gise.satis_iptal(1)
        ozet = [(e.kod, adet, ciro) for e, adet, ciro in self.gise.etkinlik_ozeti()]
        self.assertEqual(ozet, [("K1", 0, Decimal("0.00")),
                                ("T1", 1, Decimal("262.50")),
                                ("F1", 1, Decimal("245.00"))])


class HataTestleri(unittest.TestCase):

    def setUp(self) -> None:
        self.gise = ornek_gise(BUGUN)

    def test_olmayan_etkinlik(self) -> None:
        with self.assertRaises(BulunamadiHatasi):
            self.gise.satin_al("X9", "A-1-1")

    def test_olmayan_koltuk(self) -> None:
        with self.assertRaises(BulunamadiHatasi):
            self.gise.satin_al("K1", "Z-1-1")

    def test_olmayan_satis(self) -> None:
        with self.assertRaises(BulunamadiHatasi):
            self.gise.satis_iptal(99)

    def test_gecersiz_tarife_koltugu_satmaz(self) -> None:
        with self.assertRaises(GecersizSecimHatasi):
            self.gise.satin_al("K1", "A-1-1", "bedava")
        self.assertEqual(self.gise.koltuk_bul("K1", "A-1-1").durum_adi, "Boş")

    def test_gecersiz_ekstra_koltugu_satmaz(self) -> None:
        with self.assertRaises(GecersizSecimHatasi):
            self.gise.satin_al("K1", "A-1-1", "standart", ["havai_fisek"])
        self.assertEqual(self.gise.koltuk_bul("K1", "A-1-1").durum_adi, "Boş")
        self.assertEqual(self.gise.satislar(), [])

    def test_gecmis_etkinlige_bilet_satilamaz(self) -> None:
        gise = ornek_gise(BUGUN)
        gise._bugun = date(2027, 6, 1)  # bütün etkinlikler geçmişte
        with self.assertRaises(GecersizIslemHatasi):
            gise.satin_al("K1", "A-1-1")
        self.assertEqual(gise.koltuk_bul("K1", "A-1-1").durum_adi, "Boş")

    def test_bos_koltuk_birakilamaz(self) -> None:
        with self.assertRaises(GecersizIslemHatasi):
            self.gise.koltuk_birak("K1", "A-1-1")


if __name__ == "__main__":
    unittest.main()
