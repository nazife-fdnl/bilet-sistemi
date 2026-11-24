"""Satışa açık bir etkinliğin bilgileri."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from bilet_sistemi.etkinlik import EtkinlikOlusturucu
from bilet_sistemi.salon import KoltukGrubu


@dataclass
class Etkinlik:
    """Bir etkinlik: adı, türü, tarihi, salonu ve bilet oluşturucusu.

    Kalıp rolü değildir; kalıpları kullanan uygulama katmanının veri sınıfıdır.
    Her etkinliğin kendi salon ağacı (Composite) ve kendi bilet oluşturucusu
    (Factory Method) vardır.
    """

    kod: str
    ad: str
    tur: str
    tarih: date
    salon: KoltukGrubu
    olusturucu: EtkinlikOlusturucu

    def kalan_gun(self, bugun: date) -> int:
        """Etkinliğe kaç gün kaldığını döndürür (geçmişse negatif)."""
        return (self.tarih - bugun).days
