"""Bilet arayüzü ve etkinlik türlerine özel bilet sınıfları."""

from __future__ import annotations

from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Optional

from bilet_sistemi.fiyat import FiyatStratejisi, StandartFiyat
from bilet_sistemi.para import yuvarla
from bilet_sistemi.salon.koltuk import Koltuk


# [Factory Method kalıbı] Rol: Product
# Oluşturucuların ürettiği bütün biletlerin ortak arayüzü.
# Satış kodu yalnızca bu arayüzü bilir; somut bilet sınıflarını tanımaz.
#
# [Decorator kalıbı] Rol: Component
# Ekstra hizmetler (EkstraHizmet) de bu arayüzü uygular ve bir Bilet'i sarar;
# sarılmış bilet de istemciye yine bir Bilet olarak görünür.
class Bilet(ABC):

    @abstractmethod
    def aciklama(self) -> str:
        """Biletin kullanıcıya gösterilecek açıklaması."""

    @abstractmethod
    def fiyat(self) -> Decimal:
        """Biletin ödenecek tutarı (TL)."""


# Somut biletlerin ortak verisini tutan ara sınıf; üç bilet sınıfında
# aynı alanları tekrar yazmamak için vardır.
#
# [Strategy kalıbı] Rol: Context
# Bilet, fiyat kuralını bir FiyatStratejisi nesnesinde tutar. Önce etkinlik
# türünün kendi fiyatını (tur_fiyati) bulur, sonra seçilen stratejiyi uygular.
# Yeni bir indirim türü bu sınıfa dokunmadan eklenebilir.
# (fiyat() içinde alt sınıfın tur_fiyati() adımını çağırmak bir Template Method
# benzeridir; ayrı bir kalıp olarak sayılmamıştır.)
class EtkinlikBileti(Bilet, ABC):

    def __init__(
        self,
        etkinlik_adi: str,
        koltuk: Koltuk,
        taban_fiyat: Decimal,
        fiyat_stratejisi: Optional[FiyatStratejisi] = None,
    ) -> None:
        self.etkinlik_adi = etkinlik_adi
        self.koltuk = koltuk
        self.taban_fiyat = taban_fiyat
        self.fiyat_stratejisi: FiyatStratejisi = fiyat_stratejisi or StandartFiyat()

    @abstractmethod
    def tur_fiyati(self) -> Decimal:
        """Etkinlik türünün kuralına göre indirimsiz fiyat."""

    def fiyat(self) -> Decimal:
        return yuvarla(self.fiyat_stratejisi.uygula(self.tur_fiyati()))


# [Factory Method kalıbı] Rol: ConcreteProduct
# [Decorator kalıbı] Rol: ConcreteComponent
# Konserde VIP bloktaki koltuklar taban fiyatın iki katıdır.
class KonserBileti(EtkinlikBileti):

    VIP_CARPANI = Decimal("2.0")

    def aciklama(self) -> str:
        return f"Konser: {self.etkinlik_adi} | Koltuk {self.koltuk.kod} ({self.koltuk.kategori})"

    def tur_fiyati(self) -> Decimal:
        if self.koltuk.kategori == "vip":
            return self.taban_fiyat * self.VIP_CARPANI
        return self.taban_fiyat


# [Factory Method kalıbı] Rol: ConcreteProduct
# [Decorator kalıbı] Rol: ConcreteComponent
# Tiyatroda sahneye yakın ilk üç sıra yüzde 25 daha pahalıdır.
class TiyatroBileti(EtkinlikBileti):

    ON_SIRA_SINIRI = 3
    ON_SIRA_CARPANI = Decimal("1.25")

    def aciklama(self) -> str:
        return f"Tiyatro: {self.etkinlik_adi} | Koltuk {self.koltuk.kod} (sıra {self.koltuk.sira_no})"

    def tur_fiyati(self) -> Decimal:
        if self.koltuk.sira_no <= self.ON_SIRA_SINIRI:
            return self.taban_fiyat * self.ON_SIRA_CARPANI
        return self.taban_fiyat


# [Factory Method kalıbı] Rol: ConcreteProduct
# [Decorator kalıbı] Rol: ConcreteComponent
# Konferansta koltuktan bağımsız tek fiyat vardır; bilete katılım sertifikası dahildir.
class KonferansBileti(EtkinlikBileti):

    def aciklama(self) -> str:
        return (f"Konferans: {self.etkinlik_adi} | Koltuk {self.koltuk.kod} "
                f"| Katılım sertifikası dahil")

    def tur_fiyati(self) -> Decimal:
        return self.taban_fiyat
