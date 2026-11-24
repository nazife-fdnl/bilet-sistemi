"""Salondaki tek bir koltuk."""

from __future__ import annotations

from typing import List

from bilet_sistemi.durum import BosDurum, KoltukDurumu
from bilet_sistemi.salon.bilesen import SalonBileseni


# [Composite kalıbı] Rol: Leaf
# Salon ağacının en alt elemanı; içinde başka bileşen yoktur.
#
# [State kalıbı] Rol: Context
# Koltuk kendi durumunu bir KoltukDurumu nesnesinde tutar ve
# tut / sat / bırak / iptal işlemlerini o nesneye devreder.
# Böylece "hangi durumda hangi işlem yapılabilir" kuralları
# if/elif zincirleri yerine durum sınıflarının içinde yer alır.
class Koltuk(SalonBileseni):

    def __init__(self, kod: str, sira_no: int, kategori: str = "standart") -> None:
        self.kod = kod
        self.sira_no = sira_no
        self.kategori = kategori
        self._durum: KoltukDurumu = BosDurum()

    # --- Composite (Leaf) metotları ---

    @property
    def ad(self) -> str:
        return self.kod

    def kapasite(self) -> int:
        return 1

    def bos_koltuk_sayisi(self) -> int:
        return 1 if self.musait_mi() else 0

    def koltuklar(self) -> List[Koltuk]:
        return [self]

    # --- State (Context) metotları ---

    @property
    def durum_adi(self) -> str:
        return self._durum.ad

    def musait_mi(self) -> bool:
        return self._durum.musait_mi()

    def satilabilir_mi(self) -> bool:
        return self._durum.satilabilir_mi()

    def tut(self) -> None:
        self._durum.tut(self)

    def sat(self) -> None:
        self._durum.sat(self)

    def birak(self) -> None:
        self._durum.birak(self)

    def iptal_et(self) -> None:
        self._durum.iptal_et(self)

    def durumu_degistir(self, yeni_durum: KoltukDurumu) -> None:
        """Durum nesneleri geçiş yaparken bu metodu çağırır."""
        self._durum = yeni_durum

    def __repr__(self) -> str:
        return f"Koltuk({self.kod}, {self.durum_adi})"
