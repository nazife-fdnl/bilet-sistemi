"""Salon ağacını kurmak için yardımcı fonksiyon.

Bu dosya bir tasarım kalıbı değildir; yalnızca demo ve testlerde
salonu tek satırda oluşturmayı kolaylaştırır.
"""

from __future__ import annotations

from typing import Dict, Iterable, Tuple

from bilet_sistemi.salon.koltuk import Koltuk
from bilet_sistemi.salon.koltuk_grubu import KoltukGrubu


def salon_olustur(
    ad: str,
    bloklar: Dict[str, Tuple[int, int]],
    vip_bloklar: Iterable[str] = (),
) -> KoltukGrubu:
    """Salon → blok → sıra → koltuk ağacını kurar.

    bloklar: blok adı → (sıra sayısı, sıra başına koltuk sayısı)
    vip_bloklar: koltukları "vip" kategorisinde olacak blokların adları
    Koltuk kodları "Blok-Sıra-Numara" biçimindedir, örn. "A-2-5".
    """
    vip = set(vip_bloklar)
    salon = KoltukGrubu(ad, "Salon")
    for blok_adi, (sira_sayisi, koltuk_sayisi) in bloklar.items():
        blok = KoltukGrubu(blok_adi, "Blok")
        kategori = "vip" if blok_adi in vip else "standart"
        for sira_no in range(1, sira_sayisi + 1):
            sira = KoltukGrubu(f"{blok_adi}-{sira_no}", "Sıra")
            for numara in range(1, koltuk_sayisi + 1):
                sira.ekle(Koltuk(f"{blok_adi}-{sira_no}-{numara}", sira_no, kategori))
            blok.ekle(sira)
        salon.ekle(blok)
    return salon
