"""State kalıbının durum arayüzü."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:  # Yalnızca tür denetimi için; çalışma anında döngüsel içe aktarmayı önler.
    from bilet_sistemi.salon.koltuk import Koltuk


# [State kalıbı] Rol: State
# Koltuğun bulunabileceği her durumun uyması gereken ortak arayüz.
# Koltuk (Context) bir işlem istendiğinde işi o anki durum nesnesine devreder.
class KoltukDurumu(ABC):

    @property
    @abstractmethod
    def ad(self) -> str:
        """Durumun kullanıcıya gösterilecek adı."""

    @abstractmethod
    def musait_mi(self) -> bool:
        """Koltuk bu durumdayken satışa açık mı?"""

    @abstractmethod
    def satilabilir_mi(self) -> bool:
        """Koltuk bu durumdayken satılabilir mi? (Boş ve Tutuldu: evet)"""

    @abstractmethod
    def tut(self, koltuk: Koltuk) -> None:
        """Koltuğu geçici olarak ayırır."""

    @abstractmethod
    def sat(self, koltuk: Koltuk) -> None:
        """Koltuğun satışını tamamlar."""

    @abstractmethod
    def birak(self, koltuk: Koltuk) -> None:
        """Geçici ayırmayı kaldırır."""

    @abstractmethod
    def iptal_et(self, koltuk: Koltuk) -> None:
        """Satışı iptal eder, koltuğu yeniden satışa açar."""
