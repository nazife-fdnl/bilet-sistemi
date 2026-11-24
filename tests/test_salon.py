"""Composite kalıbı testleri: salon ağacı."""

import unittest

from bilet_sistemi.hatalar import GecersizIslemHatasi
from bilet_sistemi.salon import Koltuk, KoltukGrubu, salon_olustur


class SalonTestleri(unittest.TestCase):

    def setUp(self) -> None:
        # A bloğu: 2 sıra x 3 koltuk = 6, B bloğu (VIP): 1 sıra x 4 koltuk = 4
        self.salon = salon_olustur("Büyük Salon", {"A": (2, 3), "B": (1, 4)}, vip_bloklar=["B"])

    def test_kapasite_butun_agac_icin_toplanir(self) -> None:
        self.assertEqual(self.salon.kapasite(), 10)

    def test_tek_koltuk_ve_grup_ayni_arayuzu_kullanir(self) -> None:
        koltuk = self.salon.koltuk_bul("A-1-1")
        blok_a = self.salon.cocuklar()[0]
        self.assertEqual(koltuk.kapasite(), 1)
        self.assertEqual(blok_a.kapasite(), 6)

    def test_satilan_koltuk_bos_sayisini_her_seviyede_azaltir(self) -> None:
        self.salon.koltuk_bul("A-2-3").sat()
        blok_a = self.salon.cocuklar()[0]
        sira_a2 = blok_a.cocuklar()[1]
        self.assertEqual(sira_a2.bos_koltuk_sayisi(), 2)
        self.assertEqual(blok_a.bos_koltuk_sayisi(), 5)
        self.assertEqual(self.salon.bos_koltuk_sayisi(), 9)

    def test_vip_blok_koltuklari_vip_kategorisindedir(self) -> None:
        self.assertEqual(self.salon.koltuk_bul("B-1-2").kategori, "vip")
        self.assertEqual(self.salon.koltuk_bul("A-1-2").kategori, "standart")

    def test_olmayan_koltuk_none_doner(self) -> None:
        self.assertIsNone(self.salon.koltuk_bul("Z-9-9"))

    def test_gruba_yeni_bilesen_eklenebilir(self) -> None:
        loca = KoltukGrubu("Loca", "Blok")
        loca.ekle(Koltuk("L-1-1", sira_no=1, kategori="vip"))
        self.salon.ekle(loca)
        self.assertEqual(self.salon.kapasite(), 11)
        self.assertIsNotNone(self.salon.koltuk_bul("L-1-1"))

    def test_grup_kendi_icine_eklenemez(self) -> None:
        with self.assertRaises(GecersizIslemHatasi):
            self.salon.ekle(self.salon)
        blok_a = self.salon.cocuklar()[0]
        with self.assertRaises(GecersizIslemHatasi):
            blok_a.cocuklar()[0].ekle(blok_a)  # sıranın içine kendi bloğu

    def test_ayni_bilesen_iki_kez_eklenemez(self) -> None:
        sira = KoltukGrubu("X-1", "Sıra")
        koltuk = Koltuk("X-1-1", sira_no=1)
        sira.ekle(koltuk)
        with self.assertRaises(GecersizIslemHatasi):
            sira.ekle(koltuk)
        self.assertEqual(sira.kapasite(), 1)

    def test_bilesen_cikarilabilir(self) -> None:
        blok_b = self.salon.cocuklar()[1]
        self.salon.cikar(blok_b)
        self.assertEqual(self.salon.kapasite(), 6)


if __name__ == "__main__":
    unittest.main()
