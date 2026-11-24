"""Uygulamanın açılışta yüklediği örnek etkinlikler."""

from __future__ import annotations

from datetime import date, timedelta
from decimal import Decimal
from typing import Optional

from bilet_sistemi.etkinlik import KonferansOlusturucu, KonserOlusturucu, TiyatroOlusturucu
from bilet_sistemi.salon import salon_olustur
from bilet_sistemi.uygulama.etkinlik import Etkinlik
from bilet_sistemi.uygulama.gise import BiletGisesi


def ornek_gise(bugun: Optional[date] = None) -> BiletGisesi:
    """Üç örnek etkinlikle dolu bir gişe döndürür.

    Etkinlik tarihleri 'bugun' tarihine göre belirlenir; böylece erken kayıt
    indirimi her zaman aynı şekilde davranır: konser ve konferans 30 günden
    uzakta (indirim geçerli), tiyatro 30 günden yakında (indirim geçersiz).
    """
    bugun = bugun or date.today()
    etkinlikler = [
        Etkinlik(
            kod="K1",
            ad="Rock Gecesi",
            tur="Konser",
            tarih=bugun + timedelta(days=45),
            salon=salon_olustur("Açıkhava Sahnesi", {"A": (4, 10), "B": (2, 8)}, vip_bloklar=["B"]),
            olusturucu=KonserOlusturucu("Rock Gecesi", Decimal("500")),
        ),
        Etkinlik(
            kod="T1",
            ad="Hamlet",
            tur="Tiyatro",
            tarih=bugun + timedelta(days=20),
            salon=salon_olustur("Şehir Tiyatrosu", {"P": (6, 8)}),
            olusturucu=TiyatroOlusturucu("Hamlet", Decimal("300")),
        ),
        Etkinlik(
            kod="F1",
            ad="Yazılım Mimarisi Zirvesi",
            tur="Konferans",
            tarih=bugun + timedelta(days=60),
            salon=salon_olustur("Kongre Salonu", {"A": (5, 10)}),
            olusturucu=KonferansOlusturucu("Yazılım Mimarisi Zirvesi", Decimal("200")),
        ),
    ]
    return BiletGisesi(etkinlikler, bugun=bugun)
