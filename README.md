# Etkinlik Bilet Satış ve Rezervasyon Sistemi

Depo: <https://github.com/nazife-fdnl/bilet-sistemi>

Konser, tiyatro ve konferans etkinlikleri için menülü bir **bilet gişesi** uygulaması:
salon ve koltuk haritası, koltuk tutma ve bırakma, tarife ve ekstra hizmet seçerek bilet
satışı, satış iptali ve satış raporu. Yazılım Tasarım Kalıpları dersi dönem projesidir.

Sistem beş GoF tasarım kalıbıyla geliştirilmiştir: yaratımsal grupta **Factory Method**,
yapısal grupta **Composite** ve **Decorator**, davranışsal grupta **Strategy** ve **State**.
Kalıplar çerçeve veya kütüphane desteği olmadan elle yazılmış, arayüzler `abc.ABC` ile
açıkça tanımlanmış, her rol kodda `# [Kalıp kalıbı] Rol: RolAdı` yorumuyla işaretlenmiştir.

## Hızlı başlangıç

```bash
python3 main.py              # menülü uygulama
python3 main.py --demo       # hazır kullanıcı senaryosu
python3 main.py --kaliplar   # beş kalıbı tek tek gösteren tur
python3 -m unittest -v       # 90 test
```

Gereksinim: Python 3.9 veya üstü. Ek paket gerekmez.

## Dokümanlar

| Doküman | İçerik |
| --- | --- |
| [docs/GEREKSINIMLER.md](docs/GEREKSINIMLER.md) | Bütün iş kuralları, fiyat hesapları, hata ve arayüz metinleri, gereksinim → test eşlemesi |
| [docs/TASARIM.md](docs/TASARIM.md) | Katmanlar, kalıp haritası, her kalıbın problemi, UML sınıf diyagramı, alternatifi ve bedeli; sıralama diyagramı; kapsam değişiklikleri kaydı; bütün sınıfların imzaları (API özeti) |
| [docs/KURULUM.md](docs/KURULUM.md) | Kurulum, çalıştırma, sık görülen sorunlar |
| [docs/TEST.md](docs/TEST.md) | Testlerin çalıştırılması, test dosyaları, örnek hesaplar |
| [CLAUDE.md](CLAUDE.md) | Projede çalışacak yapay zekâ ajanları için yönerge |

## Kalıp haritası

| Kalıp | Grup | Çözdüğü problem | Roller → Sınıflar |
| --- | --- | --- | --- |
| **Factory Method** | Yaratımsal | Konser, tiyatro ve konferans biletlerinin fiyat kuralları farklı; satış kodu somut bilet sınıflarını bilmeden doğru bileti üretmeli. | Product → `Bilet` · ConcreteProduct → `KonserBileti`, `TiyatroBileti`, `KonferansBileti` · Creator → `EtkinlikOlusturucu` · ConcreteCreator → `KonserOlusturucu`, `TiyatroOlusturucu`, `KonferansOlusturucu` |
| **Composite** | Yapısal | Salon → blok → sıra → koltuk ağacında kapasite ve boş koltuk her seviyeye aynı şekilde sorulabilmeli. | Component → `SalonBileseni` · Leaf → `Koltuk` · Composite → `KoltukGrubu` |
| **Decorator** | Yapısal | VIP giriş, otopark ve iptal sigortası istenen sayıda ve sırada eklenebilmeli; her kombinasyon için sınıf yazılmamalı. | Component → `Bilet` · ConcreteComponent → `KonserBileti`, `TiyatroBileti`, `KonferansBileti` · Decorator → `EkstraHizmet` · ConcreteDecorator → `VipGiris`, `IptalSigortasi`, `Otopark` |
| **Strategy** | Davranışsal | Öğrenci, erken kayıt ve kurumsal indirimler `if/elif` yerine satış anında seçilebilmeli. | Strategy → `FiyatStratejisi` · ConcreteStrategy → `StandartFiyat`, `OgrenciIndirimi`, `ErkenKayitIndirimi`, `KurumsalIndirim` · Context → `EtkinlikBileti` |
| **State** | Davranışsal | Tut, sat, bırak, iptal işlemleri koltuğun durumuna göre değişir; kurallar dağınık `if` yerine durum sınıflarında olmalı. | State → `KoltukDurumu` · ConcreteState → `BosDurum`, `TutulduDurum`, `SatildiDurum` · Context → `Koltuk` |

Dosyalar, alternatifler, bedeller ve diyagramlar: [docs/TASARIM.md](docs/TASARIM.md).

## Örnek oturum (kısaltılmış)

```
Seçiminiz: 3
Etkinlik kodu (ör. K1): K1
Açıkhava Sahnesi  |  boş 56 / 56
Blok B (vip)  boş 16 / 16
         1  2  3  4  5  6  7  8
  B-1    .  .  .  .  .  .  .  .
Koltuk kodu (ör. A-1-5): B-1-3
Tarife no: 3
Ekstra no(lar): 1,3

Bilet : Konser: Rock Gecesi | Koltuk B-1-3 (vip) + VIP giriş + İptal sigortası
Tutar : 1045.00 TL
Onaylıyor musunuz? (E/H): E
Satış tamamlandı. Satış no: 1  Tutar: 1045.00 TL
```

## Proje yapısı

```
bilet-sistemi/
├── bilet_sistemi/
│   ├── durum/        State: koltuk durumları
│   ├── salon/        Composite: salon ağacı (Koltuk aynı zamanda State Context'i)
│   ├── etkinlik/     Factory Method: biletler ve oluşturucular (EtkinlikBileti Strategy Context'i)
│   ├── fiyat/        Strategy: fiyat kuralları
│   ├── ekstra/       Decorator: ekstra hizmetler
│   ├── uygulama/     BiletGisesi, Etkinlik, Satis, örnek veri (kalıp yok)
│   ├── arayuz/       Menülü arayüz, koltuk haritası, demolar (kalıp yok)
│   ├── hatalar.py    Ortak hata sınıfları
│   └── para.py       Decimal yuvarlama
├── tests/            90 unittest (her kalıp + gişe + arayüz + kalıp yapısı)
├── docs/             Gereksinim, tasarım, kurulum, test dokümanları
├── CLAUDE.md         Ajan yönergesi (AGENTS.md aynı yere yönlendirir)
└── main.py           Giriş noktası
```

## Kaynaklar

- Gamma, E., Helm, R., Johnson, R., Vlissides, J. — *Design Patterns: Elements of Reusable Object-Oriented Software* (Addison-Wesley, 1994). Kalıp ve rol adları (GoF).
- Freeman, E., Robson, E. — *Head First Design Patterns* (O'Reilly). Ders kitabı; kalıpların anlatımı için başvurulmuştur.
- Harici açık kaynak kütüphane kullanılmamıştır; yalnızca Python standart kütüphanesi (`abc`, `argparse`, `dataclasses`, `datetime`, `decimal`, `typing`, `unittest`).

## Yapay zekâ kullanımı

Projede yapay zekâ asistanı **Claude** (Anthropic) kullanılmıştır. Asistanın katkısı:

- Konu ve kalıp seçimi: problem önerisi, beş kalıbın probleme eşlenmesi (Builder yerine Factory Method kararı dahil).
- Kod: kalıp sınıfları, uygulama katmanı ve menülü arayüzün taslakları.
- Testler ve dokümanlar: birim testleri, gereksinim, tasarım, kurulum ve test dokümanları.
- Gözden geçirme: ayrı yapay zekâ ajanlarıyla projenin dokümanlardan yeniden kurulması ve
  ders kriterlerine göre değerlendirilmesi; bulunan hatalar düzeltildi.

Kod tarafımdan incelenmiş ve çalıştırılmıştır.
