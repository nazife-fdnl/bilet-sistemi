"""Decorator kalıbı testleri: ekstra hizmetler."""

import unittest
from decimal import Decimal

from bilet_sistemi.ekstra import IptalSigortasi, Otopark, VipGiris
from bilet_sistemi.etkinlik import Bilet, KonserOlusturucu
from bilet_sistemi.fiyat import OgrenciIndirimi
from bilet_sistemi.salon import Koltuk


class EkstraHizmetTestleri(unittest.TestCase):

    def setUp(self) -> None:
        konser = KonserOlusturucu("Rock Gecesi", Decimal("500"))
        self.bilet = konser.bilet_olustur(Koltuk("A-1-1", sira_no=1))  # 500 TL

    def test_tek_ekstra_fiyata_ve_aciklamaya_eklenir(self) -> None:
        sarili = VipGiris(self.bilet)
        self.assertEqual(sarili.fiyat(), Decimal("650.00"))
        self.assertTrue(sarili.aciklama().endswith("+ VIP giriş"))

    def test_ekstralar_ic_ice_birlestirilebilir(self) -> None:
        sarili = Otopark(VipGiris(self.bilet))
        self.assertEqual(sarili.fiyat(), Decimal("725.00"))
        self.assertIn("VIP giriş + Otopark", sarili.aciklama())

    def test_ayni_ekstra_iki_kez_eklenebilir(self) -> None:
        # İki araçlık otopark
        self.assertEqual(Otopark(Otopark(self.bilet)).fiyat(), Decimal("650.00"))

    def test_sigorta_sardigi_tutarin_yuzde_onudur(self) -> None:
        self.assertEqual(IptalSigortasi(self.bilet).fiyat(), Decimal("550.00"))

    def test_sarma_sirasi_sigorta_ucretini_degistirir(self) -> None:
        # Sigorta en dışta: (500 + 150) x 1.10 = 715
        self.assertEqual(IptalSigortasi(VipGiris(self.bilet)).fiyat(), Decimal("715.00"))
        # Sigorta içte: 500 x 1.10 + 150 = 700
        self.assertEqual(VipGiris(IptalSigortasi(self.bilet)).fiyat(), Decimal("700.00"))

    def test_sarili_bilet_hala_bir_bilettir(self) -> None:
        self.assertIsInstance(Otopark(VipGiris(self.bilet)), Bilet)

    def test_indirim_bilete_ekstra_ucretlere_degil_uygulanir(self) -> None:
        konser = KonserOlusturucu("Rock Gecesi", Decimal("500"))
        ogrenci = konser.bilet_olustur(Koltuk("A-1-2", sira_no=1), OgrenciIndirimi())  # 350 TL
        self.assertEqual(VipGiris(ogrenci).fiyat(), Decimal("500.00"))


if __name__ == "__main__":
    unittest.main()
