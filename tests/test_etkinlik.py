"""Factory Method kalıbı testleri: etkinlik türüne göre bilet üretimi."""

import unittest
from decimal import Decimal

from bilet_sistemi.etkinlik import (
    KonferansBileti,
    KonferansOlusturucu,
    KonserBileti,
    KonserOlusturucu,
    TiyatroBileti,
    TiyatroOlusturucu,
)
from bilet_sistemi.hatalar import GecersizIslemHatasi
from bilet_sistemi.salon import Koltuk


class EtkinlikOlusturucuTestleri(unittest.TestCase):

    def test_her_olusturucu_kendi_bilet_turunu_uretir(self) -> None:
        koltuk = Koltuk("A-1-1", sira_no=1)
        self.assertIsInstance(KonserOlusturucu("Rock Gecesi", Decimal("500")).bilet_olustur(koltuk), KonserBileti)
        self.assertIsInstance(TiyatroOlusturucu("Hamlet", Decimal("300")).bilet_olustur(koltuk), TiyatroBileti)
        self.assertIsInstance(KonferansOlusturucu("Yazılım Zirvesi", Decimal("200")).bilet_olustur(koltuk), KonferansBileti)

    def test_konserde_vip_koltuk_iki_kat_fiyatlidir(self) -> None:
        konser = KonserOlusturucu("Rock Gecesi", Decimal("500"))
        vip = konser.bilet_olustur(Koltuk("B-1-1", sira_no=1, kategori="vip"))
        standart = konser.bilet_olustur(Koltuk("A-1-1", sira_no=1))
        self.assertEqual(vip.fiyat(), Decimal("1000.00"))
        self.assertEqual(standart.fiyat(), Decimal("500.00"))

    def test_tiyatroda_on_siralar_pahalidir(self) -> None:
        tiyatro = TiyatroOlusturucu("Hamlet", Decimal("300"))
        self.assertEqual(tiyatro.bilet_olustur(Koltuk("A-2-1", sira_no=2)).fiyat(), Decimal("375.00"))
        self.assertEqual(tiyatro.bilet_olustur(Koltuk("A-5-1", sira_no=5)).fiyat(), Decimal("300.00"))

    def test_konferans_tek_fiyat_ve_sertifika_icerir(self) -> None:
        bilet = KonferansOlusturucu("Yazılım Zirvesi", Decimal("200")).bilet_olustur(
            Koltuk("A-1-1", sira_no=1, kategori="vip"))
        self.assertEqual(bilet.fiyat(), Decimal("200.00"))
        self.assertIn("sertifika", bilet.aciklama())

    def test_bilet_sat_koltugu_satilmis_yapar(self) -> None:
        koltuk = Koltuk("A-1-1", sira_no=1)
        KonserOlusturucu("Rock Gecesi", Decimal("500")).bilet_sat(koltuk)
        self.assertEqual(koltuk.durum_adi, "Satıldı")

    def test_satilmis_koltuga_bilet_satilamaz(self) -> None:
        koltuk = Koltuk("A-1-1", sira_no=1)
        konser = KonserOlusturucu("Rock Gecesi", Decimal("500"))
        konser.bilet_sat(koltuk)
        with self.assertRaises(GecersizIslemHatasi):
            konser.bilet_sat(koltuk)


if __name__ == "__main__":
    unittest.main()
