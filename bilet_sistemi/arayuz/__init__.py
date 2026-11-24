"""Kullanıcı arayüzü: menülü komut satırı ve demolar (kalıp rolü üstlenmez)."""

from bilet_sistemi.arayuz.cli import KomutSatiriArayuzu, senaryo_girdisi
from bilet_sistemi.arayuz.demo import KULLANICI_SENARYOSU, kalip_turu, kullanici_demosu
from bilet_sistemi.arayuz.gorunum import koltuk_haritasi

__all__ = [
    "KomutSatiriArayuzu", "senaryo_girdisi", "koltuk_haritasi",
    "KULLANICI_SENARYOSU", "kullanici_demosu", "kalip_turu",
]
