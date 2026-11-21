"""Bilete eklenebilen ekstra hizmetler."""

from __future__ import annotations

from abc import abstractmethod
from decimal import Decimal

from bilet_sistemi.etkinlik.bilet import Bilet
from bilet_sistemi.para import yuvarla


# [Decorator kalıbı] Rol: Decorator
# Bir bileti sarar ve onunla aynı arayüzü (Bilet) sunar. Açıklama ve fiyat
# isteklerini sardığı bilete iletir, sonuca kendi katkısını ekler.
# Dekoratörler iç içe sarılabildiği için ekstralar istenen sayıda ve
# sırada birleştirilebilir: Otopark(VipGiris(bilet)).
# (Component rolünü Bilet arayüzü, ConcreteComponent rolünü KonserBileti,
# TiyatroBileti ve KonferansBileti üstlenir.)
class EkstraHizmet(Bilet):

    def __init__(self, bilet: Bilet) -> None:
        self._bilet = bilet

    @property
    @abstractmethod
    def hizmet_adi(self) -> str:
        """Açıklamaya eklenecek hizmet adı."""

    @abstractmethod
    def hizmet_ucreti(self) -> Decimal:
        """Bu hizmetin bilet fiyatına eklenecek ücreti."""

    def aciklama(self) -> str:
        return f"{self._bilet.aciklama()} + {self.hizmet_adi}"

    def fiyat(self) -> Decimal:
        return yuvarla(self._bilet.fiyat() + self.hizmet_ucreti())


# [Decorator kalıbı] Rol: ConcreteDecorator
# Ayrı kapıdan, sıra beklemeden giriş: sabit 150 TL.
class VipGiris(EkstraHizmet):

    UCRET = Decimal("150")

    @property
    def hizmet_adi(self) -> str:
        return "VIP giriş"

    def hizmet_ucreti(self) -> Decimal:
        return self.UCRET


# [Decorator kalıbı] Rol: ConcreteDecorator
# Etkinliğe gidilemezse para iadesi: sardığı tutarın yüzde 10'u.
# Ücreti sabit değil, içindeki biletin (ve önceki ekstraların) fiyatına bağlıdır.
class IptalSigortasi(EkstraHizmet):

    ORAN = Decimal("0.10")

    @property
    def hizmet_adi(self) -> str:
        return "İptal sigortası"

    def hizmet_ucreti(self) -> Decimal:
        return self._bilet.fiyat() * self.ORAN


# [Decorator kalıbı] Rol: ConcreteDecorator
# Etkinlik alanındaki otoparkta bir araçlık yer: sabit 75 TL.
class Otopark(EkstraHizmet):

    UCRET = Decimal("75")

    @property
    def hizmet_adi(self) -> str:
        return "Otopark"

    def hizmet_ucreti(self) -> Decimal:
        return self.UCRET
