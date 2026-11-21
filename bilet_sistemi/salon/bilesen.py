"""Composite kalıbının ortak bileşen arayüzü."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from bilet_sistemi.salon.koltuk import Koltuk


# [Composite kalıbı] Rol: Component
# Salon, blok, sıra ve tek koltuk aynı arayüzü paylaşır.
# Böylece "kaç boş koltuk var?" sorusu tek bir koltuğa da
# bütün salona da aynı şekilde sorulabilir.
class SalonBileseni(ABC):

    @property
    @abstractmethod
    def ad(self) -> str:
        """Bileşenin adı veya kodu."""

    @abstractmethod
    def kapasite(self) -> int:
        """Bu bileşenin içindeki toplam koltuk sayısı."""

    @abstractmethod
    def bos_koltuk_sayisi(self) -> int:
        """Bu bileşenin içindeki satışa açık koltuk sayısı."""

    @abstractmethod
    def koltuklar(self) -> List[Koltuk]:
        """Bu bileşenin içindeki bütün koltuklar, düz bir liste olarak."""
