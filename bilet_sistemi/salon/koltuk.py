"""Salondaki tek bir koltuk."""

from __future__ import annotations

from bilet_sistemi.durum import BosDurum, KoltukDurumu


# [State kalıbı] Rol: Context
# Koltuk kendi durumunu bir KoltukDurumu nesnesinde tutar ve
# tut / sat / bırak / iptal işlemlerini o nesneye devreder.
# Böylece "hangi durumda hangi işlem yapılabilir" kuralları
# if/elif zincirleri yerine durum sınıflarının içinde yer alır.
class Koltuk:

    def __init__(self, kod: str, sira_no: int, kategori: str = "standart") -> None:
        self.kod = kod
        self.sira_no = sira_no
        self.kategori = kategori
        self._durum: KoltukDurumu = BosDurum()

    @property
    def durum_adi(self) -> str:
        return self._durum.ad

    def musait_mi(self) -> bool:
        return self._durum.musait_mi()

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
