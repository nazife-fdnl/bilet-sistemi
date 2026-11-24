"""Hazır senaryolarla çalışan demolar (kalıp değildir)."""

from __future__ import annotations

from datetime import date
from decimal import Decimal
from typing import Optional

from bilet_sistemi.arayuz.cli import KomutSatiriArayuzu, Cikti, senaryo_girdisi
from bilet_sistemi.ekstra import IptalSigortasi, Otopark, VipGiris
from bilet_sistemi.etkinlik import KonserOlusturucu, TiyatroOlusturucu
from bilet_sistemi.fiyat import ErkenKayitIndirimi, KurumsalIndirim, OgrenciIndirimi
from bilet_sistemi.hatalar import GecersizIslemHatasi
from bilet_sistemi.salon import salon_olustur
from bilet_sistemi.uygulama import ornek_gise

# Menü arayüzünü baştan sona dolaşan kullanıcı senaryosu.
KULLANICI_SENARYOSU = [
    "1",                                     # etkinlikleri listele
    "2", "K1",                               # konser salonunun haritası
    "3", "K1", "B-1-3", "3", "1,3", "E",     # VIP blok, erken kayıt, VIP giriş + sigorta
    "3", "T1", "P-2-4", "2", "", "E",        # tiyatro ön sıra, öğrenci
    "4", "F1", "A-1-5",                      # konferans koltuğu tut
    "3", "F1", "A-1-5", "4", "2", "E",       # tutulan koltuğu kurumsal + otopark ile sat
    "4", "K1", "B-1-3",                      # satılmış koltuğu tutmaya çalış → hata
    "6", "1",                                # 1 numaralı satışı iptal et
    "7",                                     # satış raporu
    "2", "K1",                               # iptal sonrası harita
    "0",
]


def kullanici_demosu(cikti: Cikti = print, bugun: Optional[date] = None) -> None:
    """Menü arayüzünü hazır cevaplarla çalıştırır."""
    gise = ornek_gise(bugun)
    arayuz = KomutSatiriArayuzu(gise, senaryo_girdisi(KULLANICI_SENARYOSU, cikti), cikti)
    arayuz.calistir()


def kalip_turu(cikti: Cikti = print) -> None:
    """Beş kalıbı tek tek, doğrudan sınıflarıyla gösterir."""

    def baslik(metin: str) -> None:
        cikti("")
        cikti(f"=== {metin} ===")

    cikti("Etkinlik Bilet Satış ve Rezervasyon Sistemi - Kalıp Turu")

    baslik("1. Salon (Composite)")
    salon = salon_olustur("Kültür Merkezi", {"A": (5, 8), "B": (2, 6)}, vip_bloklar=["B"])
    cikti(str(salon))
    for blok in salon.cocuklar():
        cikti(f"  {blok}")

    baslik("2. Konser biletleri (Factory Method + Strategy)")
    konser = KonserOlusturucu("Rock Gecesi", Decimal("500"))
    b1 = konser.bilet_sat(salon.koltuk_bul("A-3-4"))
    b2 = konser.bilet_sat(salon.koltuk_bul("A-3-5"), OgrenciIndirimi())
    b3 = konser.bilet_sat(salon.koltuk_bul("B-1-1"), ErkenKayitIndirimi(etkinlige_kalan_gun=45))
    for bilet in (b1, b2, b3):
        cikti(f"  {bilet.aciklama()}  [{bilet.fiyat_stratejisi.ad}]  {bilet.fiyat()} TL")

    baslik("3. Tiyatro bileti (aynı salon, farklı ürün)")
    tiyatro = TiyatroOlusturucu("Hamlet", Decimal("300"))
    b4 = tiyatro.bilet_sat(salon.koltuk_bul("A-1-1"), KurumsalIndirim())
    cikti(f"  {b4.aciklama()}  [{b4.fiyat_stratejisi.ad}]  {b4.fiyat()} TL")

    baslik("4. Ekstra hizmetler (Decorator)")
    paket = IptalSigortasi(Otopark(VipGiris(b1)))
    cikti(f"  {paket.aciklama()}")
    cikti(f"  Toplam: {paket.fiyat()} TL")

    baslik("5. Koltuk durumları (State)")
    koltuk = salon.koltuk_bul("A-5-8")
    cikti(f"  {koltuk}")
    koltuk.tut()
    cikti(f"  tut()    -> {koltuk}")
    koltuk.birak()
    cikti(f"  birak()  -> {koltuk}")
    try:
        konser.bilet_sat(salon.koltuk_bul("A-3-4"))
    except GecersizIslemHatasi as hata:
        cikti(f"  Satılmış koltuğa tekrar satış denendi: {hata}")
    salon.koltuk_bul("A-3-4").iptal_et()
    cikti(f"  iptal_et() -> {salon.koltuk_bul('A-3-4')}")

    baslik("6. Salonun son durumu (Composite)")
    cikti(str(salon))
    for blok in salon.cocuklar():
        cikti(f"  {blok}")
