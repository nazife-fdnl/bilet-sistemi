"""Bilet arayüzü ve etkinlik türlerine özel bilet sınıfları."""

from __future__ import annotations

from abc import ABC, abstractmethod
from decimal import Decimal

from bilet_sistemi.para import yuvarla
from bilet_sistemi.salon.koltuk import Koltuk


# [Factory Method kalıbı] Rol: Product
# Oluşturucuların ürettiği bütün biletlerin ortak arayüzü.
# Satış kodu yalnızca bu arayüzü bilir; somut bilet sınıflarını tanımaz.
class Bilet(ABC):

    @abstractmethod
    def aciklama(self) -> str:
        """Biletin kullanıcıya gösterilecek açıklaması."""

    @abstractmethod
    def fiyat(self) -> Decimal:
        """Biletin ödenecek tutarı (TL)."""


# Somut biletlerin ortak verisini tutan ara sınıf (kalıp rolü değildir;
# üç bilet sınıfında aynı alanları tekrar yazmamak için vardır).
class EtkinlikBileti(Bilet, ABC):

    def __init__(self, etkinlik_adi: str, koltuk: Koltuk, taban_fiyat: Decimal) -> None:
        self.etkinlik_adi = etkinlik_adi
        self.koltuk = koltuk
        self.taban_fiyat = taban_fiyat


# [Factory Method kalıbı] Rol: ConcreteProduct
# Konserde VIP bloktaki koltuklar taban fiyatın iki katıdır.
class KonserBileti(EtkinlikBileti):

    VIP_CARPANI = Decimal("2.0")

    def aciklama(self) -> str:
        return f"Konser: {self.etkinlik_adi} | Koltuk {self.koltuk.kod} ({self.koltuk.kategori})"

    def fiyat(self) -> Decimal:
        if self.koltuk.kategori == "vip":
            return yuvarla(self.taban_fiyat * self.VIP_CARPANI)
        return yuvarla(self.taban_fiyat)


# [Factory Method kalıbı] Rol: ConcreteProduct
# Tiyatroda sahneye yakın ilk üç sıra yüzde 25 daha pahalıdır.
class TiyatroBileti(EtkinlikBileti):

    ON_SIRA_SINIRI = 3
    ON_SIRA_CARPANI = Decimal("1.25")

    def aciklama(self) -> str:
        return f"Tiyatro: {self.etkinlik_adi} | Koltuk {self.koltuk.kod} (sıra {self.koltuk.sira_no})"

    def fiyat(self) -> Decimal:
        if self.koltuk.sira_no <= self.ON_SIRA_SINIRI:
            return yuvarla(self.taban_fiyat * self.ON_SIRA_CARPANI)
        return yuvarla(self.taban_fiyat)


# [Factory Method kalıbı] Rol: ConcreteProduct
# Konferansta koltuktan bağımsız tek fiyat vardır; bilete katılım sertifikası dahildir.
class KonferansBileti(EtkinlikBileti):

    def aciklama(self) -> str:
        return (f"Konferans: {self.etkinlik_adi} | Koltuk {self.koltuk.kod} "
                f"| Katılım sertifikası dahil")

    def fiyat(self) -> Decimal:
        return yuvarla(self.taban_fiyat)
