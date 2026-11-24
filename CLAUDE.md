# Ajan Yönergesi (CLAUDE.md)

Bu depo, Yazılım Tasarım Kalıpları dersi için yazılmış bir **etkinlik bilet satış sistemidir**.
Projeyi düzeltecek, yeniden kuracak veya değerlendirecek bir yapay zekâ ajanı için yazılmıştır.

## Önce okuyun

1. [docs/GEREKSINIMLER.md](docs/GEREKSINIMLER.md): Sistemin davranışı, bütün iş kuralları ve sayılar (K1-K10), arayüz metinleri.
2. [docs/TASARIM.md](docs/TASARIM.md): Katmanlar, beş kalıbın rolleri, sınıf ve dosya adları, alternatifler ve bedeller.
3. `tests/`: Çalıştırılabilir şartname. Kod doğruysa 81 testin hepsi geçer.

## Komutlar

```bash
python3 -m unittest -v        # bütün testler (beklenen: Ran 81 tests ... OK)
python3 main.py --demo        # uçtan uca kullanıcı senaryosu, son satır "Güle güle!"
python3 main.py --kaliplar    # beş kalıbın tek tek gösterimi
python3 main.py               # etkileşimli menü
```

## Kurallar

- **Python 3.9 uyumlu** yazın: `X | Y` tür birleşimi, `match`, `list[int]` gibi çalışma anı
  generic'leri kullanmayın; `typing.List`, `Optional` ve `from __future__ import annotations` kullanın.
- **Yalnızca standart kütüphane.** Ek paket eklemeyin.
- Para tutarları `Decimal`; yuvarlama `bilet_sistemi.para.yuvarla` (2 basamak, ROUND_HALF_UP).
- **Kalıp yapısını koruyun:** Her rol ayrı ve adlandırılmış bir sınıftır, arayüzler `abc.ABC`
  ile yazılır, kalıp yerine lambda veya `if/elif` kullanılmaz.
- Her rol sınıfının üstünde şu biçimde bir yorum bulunur (`tests/test_kalip_yapisi.py` denetler):
  `# [State kalıbı] Rol: ConcreteState`.
- Sınıf, metot ve dosya adları Türkçedir ve [docs/TASARIM.md](docs/TASARIM.md)'deki adlarla aynı kalmalıdır;
  testler bu adları içe aktarır.
- Hata mesajları ve arayüz metinleri [docs/GEREKSINIMLER.md](docs/GEREKSINIMLER.md)'deki metinlerle birebir aynı olmalıdır.

## Dosya → kalıp

| Dosya | İçerik |
| --- | --- |
| `bilet_sistemi/durum/koltuk_durumu.py` | State: `KoltukDurumu` |
| `bilet_sistemi/durum/durumlar.py` | State: `BosDurum`, `TutulduDurum`, `SatildiDurum` |
| `bilet_sistemi/salon/bilesen.py` | Composite: `SalonBileseni` |
| `bilet_sistemi/salon/koltuk.py` | Composite Leaf + State Context: `Koltuk` |
| `bilet_sistemi/salon/koltuk_grubu.py` | Composite: `KoltukGrubu` |
| `bilet_sistemi/salon/duzen.py` | Yardımcı: `salon_olustur` |
| `bilet_sistemi/etkinlik/bilet.py` | Factory Method Product'ları + Strategy Context (`EtkinlikBileti`) |
| `bilet_sistemi/etkinlik/olusturucu.py` | Factory Method Creator'ları |
| `bilet_sistemi/fiyat/strateji.py` | Strategy |
| `bilet_sistemi/ekstra/hizmet.py` | Decorator |
| `bilet_sistemi/uygulama/` | `Etkinlik`, `Satis`, `BiletGisesi`, `TARIFELER`, `EKSTRALAR`, `ornek_gise` |
| `bilet_sistemi/arayuz/` | `KomutSatiriArayuzu`, `senaryo_girdisi`, `koltuk_haritasi`, demolar |
| `bilet_sistemi/hatalar.py`, `bilet_sistemi/para.py` | Ortak hatalar, Decimal yuvarlama |

## Bir değişikliği nasıl eklemeli

[docs/TASARIM.md](docs/TASARIM.md) bölüm 6'daki tabloyu izleyin. Örnek: yeni indirim için
`fiyat/strateji.py`'ye `FiyatStratejisi`'nden türeyen bir sınıf ekleyin, rol yorumunu yazın,
`uygulama/gise.py`'deki `TARIFELER`'e bir satır ekleyin, `tests/test_fiyat.py`'ye test yazın.
