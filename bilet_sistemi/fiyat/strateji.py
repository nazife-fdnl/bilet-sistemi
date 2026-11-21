"""Fiyat hesaplama kuralları."""

from __future__ import annotations

from abc import ABC, abstractmethod
from decimal import Decimal


# [Strategy kalıbı] Rol: Strategy
# Bir bilet tutarına uygulanacak fiyat kuralının ortak arayüzü.
# Her indirim türü bu arayüzü uygulayan ayrı bir sınıftır; bilet (Context)
# hangi kuralın seçildiğini bilmeden yalnızca uygula() metodunu çağırır.
class FiyatStratejisi(ABC):

    @property
    @abstractmethod
    def ad(self) -> str:
        """Tarifenin kullanıcıya gösterilecek adı."""

    @abstractmethod
    def uygula(self, tutar: Decimal) -> Decimal:
        """Verilen tutara bu kuralı uygular ve yeni tutarı döndürür."""


# [Strategy kalıbı] Rol: ConcreteStrategy
# İndirimsiz tam tarife; strateji verilmezse varsayılan budur.
class StandartFiyat(FiyatStratejisi):

    @property
    def ad(self) -> str:
        return "Standart"

    def uygula(self, tutar: Decimal) -> Decimal:
        return tutar


# [Strategy kalıbı] Rol: ConcreteStrategy
# Öğrencilere yüzde 30 indirim.
class OgrenciIndirimi(FiyatStratejisi):

    ORAN = Decimal("0.30")

    @property
    def ad(self) -> str:
        return "Öğrenci"

    def uygula(self, tutar: Decimal) -> Decimal:
        return tutar * (1 - self.ORAN)


# [Strategy kalıbı] Rol: ConcreteStrategy
# Etkinliğe en az 30 gün kala alınan biletlere yüzde 20 indirim.
class ErkenKayitIndirimi(FiyatStratejisi):

    ORAN = Decimal("0.20")
    GEREKEN_GUN = 30

    def __init__(self, etkinlige_kalan_gun: int) -> None:
        self.etkinlige_kalan_gun = etkinlige_kalan_gun

    @property
    def ad(self) -> str:
        return "Erken kayıt"

    def uygula(self, tutar: Decimal) -> Decimal:
        if self.etkinlige_kalan_gun >= self.GEREKEN_GUN:
            return tutar * (1 - self.ORAN)
        return tutar


# [Strategy kalıbı] Rol: ConcreteStrategy
# Şirket adına alınan biletlere yüzde 15 indirim.
class KurumsalIndirim(FiyatStratejisi):

    ORAN = Decimal("0.15")

    @property
    def ad(self) -> str:
        return "Kurumsal"

    def uygula(self, tutar: Decimal) -> Decimal:
        return tutar * (1 - self.ORAN)
