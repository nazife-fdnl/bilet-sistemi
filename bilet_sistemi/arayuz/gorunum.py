"""Ekrana yazılacak metinleri hazırlayan yardımcı fonksiyonlar (kalıp değildir)."""

from __future__ import annotations

from typing import List

from bilet_sistemi.salon import Koltuk, KoltukGrubu

DURUM_SIMGELERI = {"Boş": ".", "Tutuldu": "T", "Satıldı": "X"}


def koltuk_simgesi(koltuk: Koltuk) -> str:
    return DURUM_SIMGELERI.get(koltuk.durum_adi, "?")


def koltuk_haritasi(salon: KoltukGrubu) -> str:
    """Salonu blok ve sıra sıra çizer: '.' boş, 'T' tutuldu, 'X' satıldı."""
    satirlar: List[str] = [
        f"{salon.ad}  |  boş {salon.bos_koltuk_sayisi()} / {salon.kapasite()}",
        "Simgeler: . boş   T tutuldu   X satıldı",
    ]
    for blok in salon.cocuklar():
        if not isinstance(blok, KoltukGrubu):
            continue
        koltuklar = blok.koltuklar()
        kategori = koltuklar[0].kategori if koltuklar else "-"
        satirlar.append("")
        satirlar.append(f"Blok {blok.ad} ({kategori})  boş {blok.bos_koltuk_sayisi()} / {blok.kapasite()}")
        sutun_sayisi = max((len(s.koltuklar()) for s in blok.cocuklar()), default=0)
        satirlar.append("        " + " ".join(f"{n:>2}" for n in range(1, sutun_sayisi + 1)))
        for sira in blok.cocuklar():
            simgeler = " ".join(f"{koltuk_simgesi(k):>2}" for k in sira.koltuklar())
            satirlar.append(f"  {sira.ad:<5} {simgeler}")
    return "\n".join(satirlar)
