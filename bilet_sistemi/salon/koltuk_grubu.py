"""Composite kalıbının bileşik nesnesi: salon, blok veya sıra."""

from __future__ import annotations

from typing import List, Optional

from bilet_sistemi.salon.bilesen import SalonBileseni
from bilet_sistemi.salon.koltuk import Koltuk


# [Composite kalıbı] Rol: Composite
# Başka bileşenleri (alt gruplar veya koltuklar) içeren düğüm.
# Salon → blok → sıra → koltuk ağacındaki salon, blok ve sıra bu sınıftır;
# aralarındaki fark yalnızca 'tur' alanıdır.
# Hesaplamaları kendisi yapmaz, çocuklarına sorup sonuçları toplar.
class KoltukGrubu(SalonBileseni):

    def __init__(self, ad: str, tur: str) -> None:
        self._ad = ad
        self.tur = tur  # Örn. "Salon", "Blok", "Sıra"
        self._cocuklar: List[SalonBileseni] = []

    @property
    def ad(self) -> str:
        return self._ad

    def ekle(self, bilesen: SalonBileseni) -> None:
        self._cocuklar.append(bilesen)

    def cikar(self, bilesen: SalonBileseni) -> None:
        self._cocuklar.remove(bilesen)

    def cocuklar(self) -> List[SalonBileseni]:
        return list(self._cocuklar)

    def kapasite(self) -> int:
        return sum(cocuk.kapasite() for cocuk in self._cocuklar)

    def bos_koltuk_sayisi(self) -> int:
        return sum(cocuk.bos_koltuk_sayisi() for cocuk in self._cocuklar)

    def koltuklar(self) -> List[Koltuk]:
        sonuc: List[Koltuk] = []
        for cocuk in self._cocuklar:
            sonuc.extend(cocuk.koltuklar())
        return sonuc

    def koltuk_bul(self, kod: str) -> Optional[Koltuk]:
        """Kodu verilen koltuğu bu grubun içinde arar; yoksa None döner."""
        for koltuk in self.koltuklar():
            if koltuk.kod == kod:
                return koltuk
        return None

    def __repr__(self) -> str:
        return f"{self.tur}({self.ad}, {self.bos_koltuk_sayisi()}/{self.kapasite()} boş)"
