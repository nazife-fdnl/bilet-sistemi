"""Kalıp yapısı testleri.

Davranış testlerinden ayrı olarak, her kalıbın rollerinin ayrı sınıflarla
karşılandığını, arayüzlerin abc.ABC ile tanımlandığını ve kodda rol
yorumlarının bulunduğunu denetler. Kod yeniden yazılırsa kalıp yapısının
korunduğunu bu testler gösterir.
"""

import inspect
import unittest
from abc import ABC
from pathlib import Path

from bilet_sistemi.durum import BosDurum, KoltukDurumu, SatildiDurum, TutulduDurum
from bilet_sistemi.ekstra import EkstraHizmet, IptalSigortasi, Otopark, VipGiris
from bilet_sistemi.etkinlik import (
    Bilet,
    EtkinlikBileti,
    EtkinlikOlusturucu,
    KonferansBileti,
    KonferansOlusturucu,
    KonserBileti,
    KonserOlusturucu,
    TiyatroBileti,
    TiyatroOlusturucu,
)
from bilet_sistemi.fiyat import (
    ErkenKayitIndirimi,
    FiyatStratejisi,
    KurumsalIndirim,
    OgrenciIndirimi,
    StandartFiyat,
)
from bilet_sistemi.salon import Koltuk, KoltukGrubu, SalonBileseni

PAKET = Path(__file__).resolve().parent.parent / "bilet_sistemi"

# Kalıp → (arayüz, somut sınıflar)
KALIPLAR = {
    "State": (KoltukDurumu, [BosDurum, TutulduDurum, SatildiDurum]),
    "Composite": (SalonBileseni, [Koltuk, KoltukGrubu]),
    "Factory Method (Product)": (Bilet, [KonserBileti, TiyatroBileti, KonferansBileti]),
    "Factory Method (Creator)": (EtkinlikOlusturucu, [KonserOlusturucu, TiyatroOlusturucu, KonferansOlusturucu]),
    "Strategy": (FiyatStratejisi, [StandartFiyat, OgrenciIndirimi, ErkenKayitIndirimi, KurumsalIndirim]),
    "Decorator": (EkstraHizmet, [VipGiris, IptalSigortasi, Otopark]),
}

# Kalıp → (rol yorumlarının bulunması gereken dosyalar, beklenen roller)
ROL_YORUMLARI = {
    "State": (["durum/koltuk_durumu.py", "durum/durumlar.py", "salon/koltuk.py"],
              ["State", "ConcreteState", "Context"]),
    "Composite": (["salon/bilesen.py", "salon/koltuk.py", "salon/koltuk_grubu.py"],
                  ["Component", "Leaf", "Composite"]),
    "Factory Method": (["etkinlik/bilet.py", "etkinlik/olusturucu.py"],
                       ["Product", "ConcreteProduct", "Creator", "ConcreteCreator"]),
    "Strategy": (["fiyat/strateji.py", "etkinlik/bilet.py"],
                 ["Strategy", "ConcreteStrategy", "Context"]),
    "Decorator": (["ekstra/hizmet.py"], ["Decorator", "ConcreteDecorator"]),
}


class KalipYapisiTestleri(unittest.TestCase):

    def test_arayuzler_soyut_ve_dogrudan_olusturulamaz(self) -> None:
        for kalip, (arayuz, _) in KALIPLAR.items():
            with self.subTest(kalip=kalip):
                self.assertTrue(issubclass(arayuz, ABC))
                self.assertTrue(inspect.isabstract(arayuz))

    def test_somut_siniflar_arayuzden_turer_ve_somuttur(self) -> None:
        for kalip, (arayuz, somutlar) in KALIPLAR.items():
            for sinif in somutlar:
                with self.subTest(kalip=kalip, sinif=sinif.__name__):
                    self.assertTrue(issubclass(sinif, arayuz))
                    self.assertFalse(inspect.isabstract(sinif))

    def test_decorator_hem_bilettir_hem_bilet_sarar(self) -> None:
        self.assertTrue(issubclass(EkstraHizmet, Bilet))
        self.assertTrue(inspect.isabstract(EkstraHizmet))
        parametreler = inspect.signature(EkstraHizmet.__init__).parameters
        self.assertIn("bilet", parametreler)

    def test_strategy_context_stratejiyi_tutar(self) -> None:
        self.assertTrue(issubclass(EtkinlikBileti, Bilet))
        parametreler = inspect.signature(EtkinlikBileti.__init__).parameters
        self.assertIn("fiyat_stratejisi", parametreler)

    def test_state_context_ve_composite_leaf_ayni_koltuk_sinifidir(self) -> None:
        self.assertTrue(issubclass(Koltuk, SalonBileseni))
        self.assertTrue(hasattr(Koltuk, "durumu_degistir"))

    def test_factory_method_soyut_ve_alt_siniflarda_yazilmis(self) -> None:
        self.assertIn("bilet_olustur", EtkinlikOlusturucu.__abstractmethods__)
        for sinif in (KonserOlusturucu, TiyatroOlusturucu, KonferansOlusturucu):
            with self.subTest(sinif=sinif.__name__):
                self.assertIn("bilet_olustur", sinif.__dict__)

    def test_rol_yorumlari_kodda_bulunur(self) -> None:
        for kalip, (dosyalar, roller) in ROL_YORUMLARI.items():
            metin = "\n".join((PAKET / d).read_text(encoding="utf-8") for d in dosyalar)
            for rol in roller:
                with self.subTest(kalip=kalip, rol=rol):
                    self.assertIn(f"[{kalip} kalıbı] Rol: {rol}", metin)


if __name__ == "__main__":
    unittest.main()
