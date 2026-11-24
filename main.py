"""Etkinlik Bilet Satış ve Rezervasyon Sistemi - giriş noktası.

Kullanım:
    python3 main.py             Menülü uygulamayı başlatır (klavyeden kullanılır).
    python3 main.py --demo      Menüyü hazır bir kullanıcı senaryosuyla çalıştırır.
    python3 main.py --kaliplar  Beş tasarım kalıbını tek tek gösteren turu çalıştırır.
"""

import argparse

from bilet_sistemi.arayuz import KomutSatiriArayuzu, kalip_turu, kullanici_demosu
from bilet_sistemi.uygulama import ornek_gise


def main() -> None:
    ayristirici = argparse.ArgumentParser(description="Etkinlik Bilet Satış ve Rezervasyon Sistemi")
    grup = ayristirici.add_mutually_exclusive_group()
    grup.add_argument("--demo", action="store_true", help="hazır kullanıcı senaryosunu çalıştır")
    grup.add_argument("--kaliplar", action="store_true", help="tasarım kalıplarını tek tek göster")
    secenekler = ayristirici.parse_args()

    if secenekler.demo:
        kullanici_demosu()
    elif secenekler.kaliplar:
        kalip_turu()
    else:
        KomutSatiriArayuzu(ornek_gise()).calistir()


if __name__ == "__main__":
    main()
