"""State kalıbının somut durumları.

Üç durum birbirine geçiş yaptığı için aynı dosyada tutulur;
ayrı dosyalarda olsalar birbirlerini içe aktarırken döngü oluşurdu.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from bilet_sistemi.durum.koltuk_durumu import KoltukDurumu
from bilet_sistemi.hatalar import GecersizIslemHatasi

if TYPE_CHECKING:
    from bilet_sistemi.salon.koltuk import Koltuk


# [State kalıbı] Rol: ConcreteState
# Boş koltuk: tutulabilir veya doğrudan satılabilir.
class BosDurum(KoltukDurumu):

    @property
    def ad(self) -> str:
        return "Boş"

    def musait_mi(self) -> bool:
        return True

    def tut(self, koltuk: Koltuk) -> None:
        koltuk.durumu_degistir(TutulduDurum())

    def sat(self, koltuk: Koltuk) -> None:
        koltuk.durumu_degistir(SatildiDurum())

    def birak(self, koltuk: Koltuk) -> None:
        raise GecersizIslemHatasi(f"{koltuk.kod}: boş koltuk bırakılamaz, zaten tutulmamış.")

    def iptal_et(self, koltuk: Koltuk) -> None:
        raise GecersizIslemHatasi(f"{koltuk.kod}: boş koltuğun iptal edilecek satışı yok.")


# [State kalıbı] Rol: ConcreteState
# Geçici olarak tutulmuş koltuk: satılabilir veya bırakılabilir.
class TutulduDurum(KoltukDurumu):

    @property
    def ad(self) -> str:
        return "Tutuldu"

    def musait_mi(self) -> bool:
        return False

    def tut(self, koltuk: Koltuk) -> None:
        raise GecersizIslemHatasi(f"{koltuk.kod}: koltuk zaten tutulmuş.")

    def sat(self, koltuk: Koltuk) -> None:
        koltuk.durumu_degistir(SatildiDurum())

    def birak(self, koltuk: Koltuk) -> None:
        koltuk.durumu_degistir(BosDurum())

    def iptal_et(self, koltuk: Koltuk) -> None:
        raise GecersizIslemHatasi(f"{koltuk.kod}: tutulan koltuk henüz satılmadı; iptal yerine bırakın.")


# [State kalıbı] Rol: ConcreteState
# Satılmış koltuk: yalnızca satışı iptal edilebilir.
class SatildiDurum(KoltukDurumu):

    @property
    def ad(self) -> str:
        return "Satıldı"

    def musait_mi(self) -> bool:
        return False

    def tut(self, koltuk: Koltuk) -> None:
        raise GecersizIslemHatasi(f"{koltuk.kod}: satılmış koltuk tutulamaz.")

    def sat(self, koltuk: Koltuk) -> None:
        raise GecersizIslemHatasi(f"{koltuk.kod}: koltuk zaten satılmış.")

    def birak(self, koltuk: Koltuk) -> None:
        raise GecersizIslemHatasi(f"{koltuk.kod}: satılmış koltuk bırakılamaz; iptal edin.")

    def iptal_et(self, koltuk: Koltuk) -> None:
        koltuk.durumu_degistir(BosDurum())
