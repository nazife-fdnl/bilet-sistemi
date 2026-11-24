"""Bilet gişesi: kalıpları bir araya getirip satış işlemlerini yürüten servis."""

from __future__ import annotations

from collections import OrderedDict
from datetime import date
from decimal import Decimal
from typing import Callable, Dict, List, Optional, Sequence, Tuple, Type

from bilet_sistemi.ekstra import EkstraHizmet, IptalSigortasi, Otopark, VipGiris
from bilet_sistemi.etkinlik import Bilet
from bilet_sistemi.fiyat import (
    ErkenKayitIndirimi,
    FiyatStratejisi,
    KurumsalIndirim,
    OgrenciIndirimi,
    StandartFiyat,
)
from bilet_sistemi.hatalar import BulunamadiHatasi, GecersizIslemHatasi, GecersizSecimHatasi
from bilet_sistemi.para import yuvarla
from bilet_sistemi.salon import Koltuk
from bilet_sistemi.uygulama.etkinlik import Etkinlik
from bilet_sistemi.uygulama.satis import Satis

# Tarife kodu → (gösterilecek ad, stratejiyi üreten fonksiyon).
# Erken kayıt indirimi etkinliğe kalan güne göre çalıştığı için
# fonksiyonlar etkinliği ve bugünün tarihini alır.
TarifeUretici = Callable[[Etkinlik, date], FiyatStratejisi]
TARIFELER: "OrderedDict[str, Tuple[str, TarifeUretici]]" = OrderedDict([
    ("standart", ("Standart", lambda e, bugun: StandartFiyat())),
    ("ogrenci", ("Öğrenci (%30 indirim)", lambda e, bugun: OgrenciIndirimi())),
    ("erken", ("Erken kayıt (30+ gün kala %20 indirim)",
               lambda e, bugun: ErkenKayitIndirimi(e.kalan_gun(bugun)))),
    ("kurumsal", ("Kurumsal (%15 indirim)", lambda e, bugun: KurumsalIndirim())),
])

# Ekstra kodu → (gösterilecek ad, dekoratör sınıfı).
EKSTRALAR: "OrderedDict[str, Tuple[str, Type[EkstraHizmet]]]" = OrderedDict([
    ("vip", ("VIP giriş (+150 TL)", VipGiris)),
    ("otopark", ("Otopark (+75 TL)", Otopark)),
    ("sigorta", ("İptal sigortası (+%10)", IptalSigortasi)),
])


class BiletGisesi:
    """Etkinlikleri ve satışları yöneten uygulama servisi.

    Kalıp rolü değildir; kullanıcı arayüzü yalnızca bu sınıfla konuşur.
    İçeride kalıplar şöyle kullanılır:
      - koltuk bulma ve doluluk:      Composite (Etkinlik.salon)
      - bilet üretimi:                Factory Method (Etkinlik.olusturucu)
      - tarife:                       Strategy (TARIFELER)
      - ekstralar:                    Decorator (EKSTRALAR)
      - tut / sat / bırak / iptal:    State (Koltuk)
    """

    def __init__(self, etkinlikler: Sequence[Etkinlik], bugun: Optional[date] = None) -> None:
        self._etkinlikler: Dict[str, Etkinlik] = OrderedDict((e.kod, e) for e in etkinlikler)
        self._bugun = bugun
        self._satislar: List[Satis] = []
        self._sonraki_no = 1

    # --- Sorgular ---

    @property
    def bugun(self) -> date:
        return self._bugun or date.today()

    def etkinlikler(self) -> List[Etkinlik]:
        return list(self._etkinlikler.values())

    def etkinlik_bul(self, kod: str) -> Etkinlik:
        etkinlik = self._etkinlikler.get(kod.strip().upper())
        if etkinlik is None:
            raise BulunamadiHatasi(f"'{kod}' kodlu etkinlik yok.")
        return etkinlik

    def koltuk_bul(self, etkinlik_kodu: str, koltuk_kodu: str) -> Koltuk:
        etkinlik = self.etkinlik_bul(etkinlik_kodu)
        koltuk = etkinlik.salon.koltuk_bul(koltuk_kodu.strip().upper())
        if koltuk is None:
            raise BulunamadiHatasi(f"{etkinlik.ad} salonunda '{koltuk_kodu}' kodlu koltuk yok.")
        return koltuk

    def satislar(self, iptaller_dahil: bool = False) -> List[Satis]:
        if iptaller_dahil:
            return list(self._satislar)
        return [s for s in self._satislar if not s.iptal_edildi]

    def satis_bul(self, no: int) -> Satis:
        for satis in self._satislar:
            if satis.no == no:
                return satis
        raise BulunamadiHatasi(f"{no} numaralı satış yok.")

    # --- Fiyat ---

    def strateji_olustur(self, etkinlik: Etkinlik, tarife: str) -> FiyatStratejisi:
        if tarife not in TARIFELER:
            raise GecersizSecimHatasi(f"'{tarife}' diye bir tarife yok.")
        _, uretici = TARIFELER[tarife]
        return uretici(etkinlik, self.bugun)

    @staticmethod
    def ekstralari_ekle(bilet: Bilet, ekstralar: Sequence[str]) -> Bilet:
        """Seçilen ekstraları verilen sırayla biletin etrafına sarar (Decorator)."""
        for kod in ekstralar:
            if kod not in EKSTRALAR:
                raise GecersizSecimHatasi(f"'{kod}' diye bir ekstra hizmet yok.")
            _, dekorator = EKSTRALAR[kod]
            bilet = dekorator(bilet)
        return bilet

    def fiyat_teklifi(self, etkinlik_kodu: str, koltuk_kodu: str,
                      tarife: str = "standart", ekstralar: Sequence[str] = ()) -> Bilet:
        """Satış yapmadan, koltuğun durumunu değiştirmeden fiyat hesaplar."""
        etkinlik = self.etkinlik_bul(etkinlik_kodu)
        koltuk = self.koltuk_bul(etkinlik_kodu, koltuk_kodu)
        bilet = etkinlik.olusturucu.bilet_olustur(koltuk, self.strateji_olustur(etkinlik, tarife))
        return self.ekstralari_ekle(bilet, ekstralar)

    # --- İşlemler ---

    def satin_al(self, etkinlik_kodu: str, koltuk_kodu: str,
                 tarife: str = "standart", ekstralar: Sequence[str] = ()) -> Satis:
        """Bilet satar. Koltuk boş veya tutulmuş olmalıdır."""
        etkinlik = self.etkinlik_bul(etkinlik_kodu)
        koltuk = self.koltuk_bul(etkinlik_kodu, koltuk_kodu)
        strateji = self.strateji_olustur(etkinlik, tarife)
        # Ekstra kodları satıştan önce denetlenir; geçersizse koltuk satılmaz.
        for kod in ekstralar:
            if kod not in EKSTRALAR:
                raise GecersizSecimHatasi(f"'{kod}' diye bir ekstra hizmet yok.")
        bilet = etkinlik.olusturucu.bilet_sat(koltuk, strateji)
        bilet = self.ekstralari_ekle(bilet, ekstralar)
        satis = Satis(self._sonraki_no, etkinlik, koltuk, bilet, strateji.ad, list(ekstralar))
        self._sonraki_no += 1
        self._satislar.append(satis)
        return satis

    def koltuk_tut(self, etkinlik_kodu: str, koltuk_kodu: str) -> Koltuk:
        koltuk = self.koltuk_bul(etkinlik_kodu, koltuk_kodu)
        koltuk.tut()
        return koltuk

    def koltuk_birak(self, etkinlik_kodu: str, koltuk_kodu: str) -> Koltuk:
        koltuk = self.koltuk_bul(etkinlik_kodu, koltuk_kodu)
        koltuk.birak()
        return koltuk

    def satis_iptal(self, no: int) -> Satis:
        satis = self.satis_bul(no)
        if satis.iptal_edildi:
            raise GecersizIslemHatasi(f"{no} numaralı satış zaten iptal edilmiş.")
        satis.koltuk.iptal_et()
        satis.iptal_edildi = True
        return satis

    # --- Rapor ---

    def toplam_ciro(self) -> Decimal:
        return yuvarla(sum((s.tutar for s in self.satislar()), Decimal("0")))

    def etkinlik_ozeti(self) -> List[Tuple[Etkinlik, int, Decimal]]:
        """Her etkinlik için (etkinlik, satılan bilet sayısı, ciro)."""
        ozet = []
        for etkinlik in self.etkinlikler():
            satislar = [s for s in self.satislar() if s.etkinlik is etkinlik]
            ciro = yuvarla(sum((s.tutar for s in satislar), Decimal("0")))
            ozet.append((etkinlik, len(satislar), ciro))
        return ozet
