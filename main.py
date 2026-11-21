"""Sistemin örnek kullanımını gösteren demo programı.

Beş tasarım kalıbını tek bir satış senaryosunda birlikte çalıştırır.
Çalıştırmak için:  python3 main.py
"""

from decimal import Decimal

from bilet_sistemi.ekstra import IptalSigortasi, Otopark, VipGiris
from bilet_sistemi.etkinlik import KonserOlusturucu, TiyatroOlusturucu
from bilet_sistemi.fiyat import ErkenKayitIndirimi, KurumsalIndirim, OgrenciIndirimi
from bilet_sistemi.hatalar import GecersizIslemHatasi
from bilet_sistemi.salon import salon_olustur


def baslik(metin: str) -> None:
    print()
    print(f"=== {metin} ===")


def main() -> None:
    print("Etkinlik Bilet Satış ve Rezervasyon Sistemi - Demo")

    # Composite: salon → blok → sıra → koltuk ağacı
    baslik("1. Salon (Composite)")
    salon = salon_olustur("Kültür Merkezi", {"A": (5, 8), "B": (2, 6)}, vip_bloklar=["B"])
    print(salon)
    for blok in salon.cocuklar():
        print(f"  {blok}")

    # Factory Method: etkinlik türü kendi biletini üretir
    # Strategy: fiyat kuralı bilete dışarıdan verilir
    baslik("2. Konser biletleri (Factory Method + Strategy)")
    konser = KonserOlusturucu("Rock Gecesi", Decimal("500"))
    b1 = konser.bilet_sat(salon.koltuk_bul("A-3-4"))
    b2 = konser.bilet_sat(salon.koltuk_bul("A-3-5"), OgrenciIndirimi())
    b3 = konser.bilet_sat(salon.koltuk_bul("B-1-1"), ErkenKayitIndirimi(etkinlige_kalan_gun=45))
    for bilet in (b1, b2, b3):
        print(f"  {bilet.aciklama()}  [{bilet.fiyat_stratejisi.ad}]  {bilet.fiyat()} TL")

    baslik("3. Tiyatro bileti (aynı salon, farklı ürün)")
    tiyatro = TiyatroOlusturucu("Hamlet", Decimal("300"))
    b4 = tiyatro.bilet_sat(salon.koltuk_bul("A-1-1"), KurumsalIndirim())
    print(f"  {b4.aciklama()}  [{b4.fiyat_stratejisi.ad}]  {b4.fiyat()} TL")

    # Decorator: ekstralar biletin etrafına sarılır
    baslik("4. Ekstra hizmetler (Decorator)")
    paket = IptalSigortasi(Otopark(VipGiris(b1)))
    print(f"  {paket.aciklama()}")
    print(f"  Toplam: {paket.fiyat()} TL")

    # State: koltuk durumları ve geçersiz işlemler
    baslik("5. Koltuk durumları (State)")
    koltuk = salon.koltuk_bul("A-5-8")
    print(f"  {koltuk}")
    koltuk.tut()
    print(f"  tut()    -> {koltuk}")
    koltuk.birak()
    print(f"  birak()  -> {koltuk}")
    try:
        konser.bilet_sat(salon.koltuk_bul("A-3-4"))
    except GecersizIslemHatasi as hata:
        print(f"  Satılmış koltuğa tekrar satış denendi: {hata}")
    salon.koltuk_bul("A-3-4").iptal_et()
    print(f"  iptal_et() -> {salon.koltuk_bul('A-3-4')}")

    baslik("6. Salonun son durumu (Composite)")
    print(salon)
    for blok in salon.cocuklar():
        print(f"  {blok}")


if __name__ == "__main__":
    main()
