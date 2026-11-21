"""State kalıbı testleri: koltuk durum geçişleri."""

import unittest

from bilet_sistemi.hatalar import GecersizIslemHatasi
from bilet_sistemi.salon import Koltuk


class KoltukDurumTestleri(unittest.TestCase):

    def setUp(self) -> None:
        self.koltuk = Koltuk("A-1-1", sira_no=1)

    def test_yeni_koltuk_bos_ve_musaittir(self) -> None:
        self.assertEqual(self.koltuk.durum_adi, "Boş")
        self.assertTrue(self.koltuk.musait_mi())

    def test_tut_sonra_sat(self) -> None:
        self.koltuk.tut()
        self.assertEqual(self.koltuk.durum_adi, "Tutuldu")
        self.assertFalse(self.koltuk.musait_mi())
        self.koltuk.sat()
        self.assertEqual(self.koltuk.durum_adi, "Satıldı")

    def test_bos_koltuk_dogrudan_satilabilir(self) -> None:
        self.koltuk.sat()
        self.assertEqual(self.koltuk.durum_adi, "Satıldı")

    def test_tutulan_koltuk_birakilinca_bos_olur(self) -> None:
        self.koltuk.tut()
        self.koltuk.birak()
        self.assertEqual(self.koltuk.durum_adi, "Boş")

    def test_satilan_koltuk_iptal_edilince_bos_olur(self) -> None:
        self.koltuk.sat()
        self.koltuk.iptal_et()
        self.assertTrue(self.koltuk.musait_mi())

    def test_satilmis_koltuk_tekrar_tutulamaz(self) -> None:
        self.koltuk.sat()
        with self.assertRaises(GecersizIslemHatasi):
            self.koltuk.tut()

    def test_satilmis_koltuk_tekrar_satilamaz(self) -> None:
        self.koltuk.sat()
        with self.assertRaises(GecersizIslemHatasi):
            self.koltuk.sat()

    def test_tutulmus_koltuk_tekrar_tutulamaz(self) -> None:
        self.koltuk.tut()
        with self.assertRaises(GecersizIslemHatasi):
            self.koltuk.tut()

    def test_bos_koltuk_birakilamaz_ve_iptal_edilemez(self) -> None:
        with self.assertRaises(GecersizIslemHatasi):
            self.koltuk.birak()
        with self.assertRaises(GecersizIslemHatasi):
            self.koltuk.iptal_et()


if __name__ == "__main__":
    unittest.main()
