"""Menülü, etkileşimli komut satırı arayüzü."""

from __future__ import annotations

from typing import Callable, Iterable, Iterator, List

from bilet_sistemi.arayuz.gorunum import koltuk_haritasi
from bilet_sistemi.hatalar import BiletSistemiHatasi, GecersizSecimHatasi
from bilet_sistemi.uygulama import EKSTRALAR, TARIFELER, BiletGisesi

Girdi = Callable[[str], str]
Cikti = Callable[[str], None]

MENU = """
========= BİLET GİŞESİ =========
1) Etkinlikleri listele
2) Salon ve koltuk haritası
3) Bilet satın al
4) Koltuk tut
5) Tutulan koltuğu bırak
6) Satış iptal et
7) Satışlar ve rapor
0) Çıkış
================================"""


class KomutSatiriArayuzu:
    """Kullanıcıdan komut alıp BiletGisesi'ne ileten arayüz (kalıp rolü değildir).

    'girdi' ve 'cikti' dışarıdan verilebildiği için testlerde ve demo
    modunda klavye yerine hazır bir senaryo kullanılabilir.
    """

    def __init__(self, gise: BiletGisesi, girdi: Girdi = input, cikti: Cikti = print) -> None:
        self.gise = gise
        self._girdi = girdi
        self._yaz = cikti

    # --- Ana döngü ---

    def calistir(self) -> None:
        self._yaz("Etkinlik Bilet Satış ve Rezervasyon Sistemi")
        islemler = {
            "1": self.etkinlikleri_listele,
            "2": self.salon_haritasi,
            "3": self.bilet_satin_al,
            "4": self.koltuk_tut,
            "5": self.koltuk_birak,
            "6": self.satis_iptal,
            "7": self.rapor,
        }
        while True:
            self._yaz(MENU)
            try:
                secim = self._sor("Seçiminiz: ")
            except EOFError:
                break
            if secim == "0":
                break
            islem = islemler.get(secim)
            if islem is None:
                self._yaz("Geçersiz seçim, 0-7 arası bir sayı girin.")
                continue
            try:
                islem()
            except BiletSistemiHatasi as hata:
                self._yaz(f"Hata: {hata}")
            except EOFError:
                break
        self._yaz("Güle güle!")

    def _sor(self, soru: str) -> str:
        return self._girdi(soru).strip()

    def _etkinlik_sor(self):
        return self.gise.etkinlik_bul(self._sor("Etkinlik kodu (ör. K1): "))

    # --- Menü işlemleri ---

    def etkinlikleri_listele(self) -> None:
        self._yaz("\nKod  Tür        Etkinlik                    Tarih       Kalan gün  Boş/Kapasite")
        for e in self.gise.etkinlikler():
            self._yaz(f"{e.kod:<4} {e.tur:<10} {e.ad:<27} {e.tarih.isoformat()}  "
                      f"{e.kalan_gun(self.gise.bugun):>9}  {e.salon.bos_koltuk_sayisi():>3}/{e.salon.kapasite()}")

    def salon_haritasi(self) -> None:
        etkinlik = self._etkinlik_sor()
        self._yaz(f"\n{etkinlik.ad} ({etkinlik.tur})")
        self._yaz(koltuk_haritasi(etkinlik.salon))

    def bilet_satin_al(self) -> None:
        etkinlik = self._etkinlik_sor()
        self._yaz(koltuk_haritasi(etkinlik.salon))
        koltuk_kodu = self._sor("Koltuk kodu (ör. A-1-5): ")
        self.gise.koltuk_bul(etkinlik.kod, koltuk_kodu)

        tarife = self._listeden_sec("Tarife", list(TARIFELER.items()))
        ekstralar = self._ekstra_sec()

        teklif = self.gise.fiyat_teklifi(etkinlik.kod, koltuk_kodu, tarife, ekstralar)
        self._yaz(f"\nBilet : {teklif.aciklama()}")
        self._yaz(f"Tutar : {teklif.fiyat()} TL")
        if self._sor("Onaylıyor musunuz? (E/H): ").upper() != "E":
            self._yaz("Satın alma iptal edildi.")
            return
        satis = self.gise.satin_al(etkinlik.kod, koltuk_kodu, tarife, ekstralar)
        self._yaz(f"Satış tamamlandı. Satış no: {satis.no}  Tutar: {satis.tutar} TL")

    def koltuk_tut(self) -> None:
        etkinlik = self._etkinlik_sor()
        koltuk = self.gise.koltuk_tut(etkinlik.kod, self._sor("Koltuk kodu: "))
        self._yaz(f"{koltuk.kod} koltuğu tutuldu.")

    def koltuk_birak(self) -> None:
        etkinlik = self._etkinlik_sor()
        koltuk = self.gise.koltuk_birak(etkinlik.kod, self._sor("Koltuk kodu: "))
        self._yaz(f"{koltuk.kod} koltuğu bırakıldı, yeniden satışta.")

    def satis_iptal(self) -> None:
        metin = self._sor("İptal edilecek satış no: ")
        if not metin.isdigit():
            raise GecersizSecimHatasi("Satış numarası bir sayı olmalı.")
        satis = self.gise.satis_iptal(int(metin))
        self._yaz(f"{satis.no} numaralı satış iptal edildi, {satis.koltuk.kod} koltuğu yeniden satışta.")

    def rapor(self) -> None:
        satislar = self.gise.satislar(iptaller_dahil=True)
        if not satislar:
            self._yaz("Henüz satış yok.")
        else:
            self._yaz("\nNo  Etkinlik                  Koltuk  Tarife        Tutar      Durum")
            for s in satislar:
                durum = "İPTAL" if s.iptal_edildi else "Geçerli"
                self._yaz(f"{s.no:<3} {s.etkinlik.ad[:24]:<25} {s.koltuk.kod:<7} {s.tarife:<12} "
                          f"{str(s.tutar):>9} TL  {durum}")
        self._yaz("\nEtkinlik bazında:")
        for etkinlik, adet, ciro in self.gise.etkinlik_ozeti():
            self._yaz(f"  {etkinlik.kod} {etkinlik.ad:<27} {adet:>3} bilet  {str(ciro):>9} TL")
        self._yaz(f"Toplam ciro: {self.gise.toplam_ciro()} TL")

    # --- Seçim yardımcıları ---

    def _listeden_sec(self, baslik: str, secenekler: list) -> str:
        self._yaz(f"\n{baslik}:")
        for i, (_, (ad, _)) in enumerate(secenekler, start=1):
            self._yaz(f"  {i}) {ad}")
        metin = self._sor(f"{baslik} no: ")
        if not metin.isdigit() or not 1 <= int(metin) <= len(secenekler):
            raise GecersizSecimHatasi(f"1-{len(secenekler)} arası bir {baslik.lower()} numarası girin.")
        return secenekler[int(metin) - 1][0]

    def _ekstra_sec(self) -> List[str]:
        secenekler = list(EKSTRALAR.items())
        self._yaz("\nEkstra hizmetler (birden fazlası virgülle, yoksa boş bırakın):")
        for i, (_, (ad, _)) in enumerate(secenekler, start=1):
            self._yaz(f"  {i}) {ad}")
        metin = self._sor("Ekstra no(lar): ")
        if not metin:
            return []
        kodlar = []
        for parca in metin.split(","):
            parca = parca.strip()
            if not parca.isdigit() or not 1 <= int(parca) <= len(secenekler):
                raise GecersizSecimHatasi(f"'{parca}' geçerli bir ekstra numarası değil.")
            kodlar.append(secenekler[int(parca) - 1][0])
        return kodlar


def senaryo_girdisi(adimlar: Iterable[str], cikti: Cikti = print) -> Girdi:
    """Klavye yerine hazır cevapları sırayla veren girdi fonksiyonu.

    Her cevabı soru ile birlikte ekrana yazar; böylece demo çıktısı
    gerçek bir kullanıcı oturumu gibi okunur. Cevaplar bitince EOFError verir.
    """
    kalan: Iterator[str] = iter(adimlar)

    def girdi(soru: str) -> str:
        try:
            cevap = next(kalan)
        except StopIteration:
            raise EOFError from None
        cikti(f"{soru}{cevap}")
        return cevap

    return girdi
