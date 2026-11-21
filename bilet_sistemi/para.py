"""Para tutarları için yardımcı fonksiyon (tasarım kalıbı değildir).

Fiyatlar float yerine Decimal ile tutulur; float 0.1 + 0.2 gibi
işlemlerde küsurat hatası yapar, Decimal yapmaz.
"""

from decimal import ROUND_HALF_UP, Decimal


def yuvarla(tutar: Decimal) -> Decimal:
    """Tutarı kuruş hassasiyetine (iki basamak) yuvarlar."""
    return tutar.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
