"""Etkinlik türüne göre bilet oluşturan sınıflar."""

from __future__ import annotations

from abc import ABC, abstractmethod
from decimal import Decimal

from bilet_sistemi.etkinlik.bilet import Bilet, KonferansBileti, KonserBileti, TiyatroBileti
from bilet_sistemi.salon.koltuk import Koltuk


# [Factory Method kalıbı] Rol: Creator
# Bilet satışının ortak adımlarını (koltuğu satmak, bileti döndürmek) yürütür.
# Hangi tür biletin üretileceğine alt sınıflar karar verir: bilet_olustur()
# fabrika metodudur ve her etkinlik türü onu kendine göre yazar.
class EtkinlikOlusturucu(ABC):

    def __init__(self, etkinlik_adi: str, taban_fiyat: Decimal) -> None:
        self.etkinlik_adi = etkinlik_adi
        self.taban_fiyat = taban_fiyat

    @abstractmethod
    def bilet_olustur(self, koltuk: Koltuk) -> Bilet:
        """Fabrika metodu: bu etkinlik türüne ait bileti üretir."""

    def bilet_sat(self, koltuk: Koltuk) -> Bilet:
        """Koltuğu satar ve o koltuk için bu etkinliğin biletini döndürür.

        Koltuk satışa uygun değilse koltuğun durumu (State kalıbı)
        GecersizIslemHatasi fırlatır ve bilet verilmez.
        """
        bilet = self.bilet_olustur(koltuk)
        koltuk.sat()
        return bilet


# [Factory Method kalıbı] Rol: ConcreteCreator
class KonserOlusturucu(EtkinlikOlusturucu):

    def bilet_olustur(self, koltuk: Koltuk) -> Bilet:
        return KonserBileti(self.etkinlik_adi, koltuk, self.taban_fiyat)


# [Factory Method kalıbı] Rol: ConcreteCreator
class TiyatroOlusturucu(EtkinlikOlusturucu):

    def bilet_olustur(self, koltuk: Koltuk) -> Bilet:
        return TiyatroBileti(self.etkinlik_adi, koltuk, self.taban_fiyat)


# [Factory Method kalıbı] Rol: ConcreteCreator
class KonferansOlusturucu(EtkinlikOlusturucu):

    def bilet_olustur(self, koltuk: Koltuk) -> Bilet:
        return KonferansBileti(self.etkinlik_adi, koltuk, self.taban_fiyat)
