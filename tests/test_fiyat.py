"""Strategy kalıbı testleri: fiyat kuralları."""

import unittest
from decimal import Decimal

from bilet_sistemi.etkinlik import KonserOlusturucu, TiyatroOlusturucu
from bilet_sistemi.fiyat import ErkenKayitIndirimi, KurumsalIndirim, OgrenciIndirimi, StandartFiyat
from bilet_sistemi.salon import Koltuk


class FiyatStratejisiTestleri(unittest.TestCase):

    def setUp(self) -> None:
        self.konser = KonserOlusturucu("Rock Gecesi", Decimal("500"))
        self.koltuk = Koltuk("A-1-1", sira_no=1)

    def test_strateji_verilmezse_standart_fiyat_uygulanir(self) -> None:
        bilet = self.konser.bilet_olustur(self.koltuk)
        self.assertIsInstance(bilet.fiyat_stratejisi, StandartFiyat)
        self.assertEqual(bilet.fiyat(), Decimal("500.00"))

    def test_ogrenci_indirimi_yuzde_otuz(self) -> None:
        bilet = self.konser.bilet_olustur(self.koltuk, OgrenciIndirimi())
        self.assertEqual(bilet.fiyat(), Decimal("350.00"))

    def test_erken_kayit_otuz_gun_ve_fazlasinda_gecerli(self) -> None:
        self.assertEqual(self.konser.bilet_olustur(self.koltuk, ErkenKayitIndirimi(45)).fiyat(), Decimal("400.00"))
        self.assertEqual(self.konser.bilet_olustur(self.koltuk, ErkenKayitIndirimi(30)).fiyat(), Decimal("400.00"))

    def test_erken_kayit_otuz_gunden_az_kalinca_gecersiz(self) -> None:
        bilet = self.konser.bilet_olustur(self.koltuk, ErkenKayitIndirimi(10))
        self.assertEqual(bilet.fiyat(), Decimal("500.00"))

    def test_kurumsal_indirim_yuzde_on_bes(self) -> None:
        bilet = self.konser.bilet_olustur(self.koltuk, KurumsalIndirim())
        self.assertEqual(bilet.fiyat(), Decimal("425.00"))

    def test_strateji_etkinlik_kuralindan_sonra_uygulanir(self) -> None:
        # Tiyatro ön sıra: 300 x 1.25 = 375, öğrenci indirimi: 375 x 0.70 = 262.50
        tiyatro = TiyatroOlusturucu("Hamlet", Decimal("300"))
        bilet = tiyatro.bilet_olustur(Koltuk("A-1-1", sira_no=1), OgrenciIndirimi())
        self.assertEqual(bilet.fiyat(), Decimal("262.50"))

    def test_strateji_calisma_aninda_degistirilebilir(self) -> None:
        bilet = self.konser.bilet_olustur(self.koltuk)
        bilet.fiyat_stratejisi = OgrenciIndirimi()
        self.assertEqual(bilet.fiyat(), Decimal("350.00"))

    def test_bilet_sat_stratejiyi_bilete_aktarir(self) -> None:
        bilet = self.konser.bilet_sat(self.koltuk, KurumsalIndirim())
        self.assertEqual(bilet.fiyat(), Decimal("425.00"))
        self.assertEqual(self.koltuk.durum_adi, "Satıldı")


if __name__ == "__main__":
    unittest.main()
