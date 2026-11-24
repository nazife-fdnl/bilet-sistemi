"""Tamamlanmış bir bilet satışının kaydı."""

from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal
from typing import List

from bilet_sistemi.etkinlik import Bilet
from bilet_sistemi.salon import Koltuk
from bilet_sistemi.uygulama.etkinlik import Etkinlik


@dataclass
class Satis:
    """Bir satışın kaydı.

    Kalıp rolü değildir. 'bilet' alanı ekstralarla sarılmış (Decorator) bilet
    olabileceğinden koltuğa bilet üzerinden değil, bu kayıttaki 'koltuk'
    alanından ulaşılır. 'tutar' satış anında sabitlenir; fiyat kuralları
    sonradan değişse bile geçmiş satışın tutarı ve raporlar değişmez.
    """

    no: int
    etkinlik: Etkinlik
    koltuk: Koltuk
    bilet: Bilet
    tutar: Decimal
    tarife: str
    ekstralar: List[str] = field(default_factory=list)
    iptal_edildi: bool = False
