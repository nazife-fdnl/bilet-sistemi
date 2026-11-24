# Gereksinim Dokümanı

Bu doküman sistemin **ne yapması gerektiğini** tanımlar. Kod silinse bile bu doküman,
[TASARIM.md](TASARIM.md) ve `tests/` klasöründeki testler birlikte projeyi aynı davranışla
yeniden kurmaya yeter. Kurallardaki her sayı testlerde doğrulanır.

## 1. Amaç ve kapsam

Konser, tiyatro ve konferans etkinlikleri için bilet satan bir **gişe uygulaması**.
Görevli; etkinlikleri listeler, salonun koltuk haritasını görür, koltuk tutar veya bırakır,
tarife ve ekstra hizmet seçerek bilet satar, satışı iptal eder ve satış raporu alır.

- Tek kullanıcılı, menülü komut satırı uygulamasıdır.
- Veriler bellekte tutulur; program kapanınca satışlar silinir (kalıcı kayıt kapsam dışıdır).
- Python 3.9+ ve yalnızca standart kütüphane kullanılır.

## 2. Kavramlar

| Kavram | Tanım |
| --- | --- |
| Salon | Bloklardan oluşan ağaç: Salon → Blok → Sıra → Koltuk. |
| Koltuk kodu | `Blok-Sıra-Numara`, örn. `B-1-3`. Kodlar büyük/küçük harf ve baştaki/sondaki boşluk duyarsızdır. |
| Koltuk kategorisi | `standart` veya `vip`. Bir blok VIP ise içindeki bütün koltuklar `vip`'tir. |
| Koltuk durumu | `Boş`, `Tutuldu`, `Satıldı`. |
| Taban fiyat | Etkinliğin tanımlandığı temel fiyat (TL). |
| Tür fiyatı | Etkinlik türünün kuralı uygulanmış, indirimsiz fiyat. |
| Tarife | Tür fiyatına uygulanan indirim kuralı. |
| Ekstra hizmet | Bilete eklenen ücretli hizmet. |
| Satış | Numaralı satış kaydı: etkinlik, koltuk, bilet, tarife adı, ekstra kodları, iptal bilgisi. |

## 3. İş kuralları

### K1. Koltuk durumları

Her koltuk `Boş` başlar. İzin verilen geçişler:

| Durum \ İşlem | `tut()` | `sat()` | `birak()` | `iptal_et()` | Satışa açık mı (`musait_mi`) |
| --- | --- | --- | --- | --- | --- |
| **Boş** | → Tutuldu | → Satıldı | hata | hata | Evet |
| **Tutuldu** | hata | → Satıldı | → Boş | hata | Hayır |
| **Satıldı** | hata | hata | hata | → Boş | Hayır |

"hata" = `GecersizIslemHatasi`, mesaj koltuk koduyla başlar. Mesajlar:

| Durum | İşlem | Mesaj |
| --- | --- | --- |
| Boş | birak | `{kod}: boş koltuk bırakılamaz, zaten tutulmamış.` |
| Boş | iptal_et | `{kod}: boş koltuğun iptal edilecek satışı yok.` |
| Tutuldu | tut | `{kod}: koltuk zaten tutulmuş.` |
| Tutuldu | iptal_et | `{kod}: tutulan koltuk henüz satılmadı; iptal yerine bırakın.` |
| Satıldı | tut | `{kod}: satılmış koltuk tutulamaz.` |
| Satıldı | sat | `{kod}: koltuk zaten satılmış.` |
| Satıldı | birak | `{kod}: satılmış koltuk bırakılamaz; iptal edin.` |

### K2. Salon

- Kapasite ve boş koltuk sayısı salon, blok, sıra ve tek koltuk için aynı yöntemle sorulur;
  üst seviye, alt seviyelerin toplamıdır. Tek koltuğun kapasitesi 1, boşsa boş sayısı 1'dir.
- "Boş" sayılan koltuk yalnızca `Boş` durumundakidir (tutulan koltuk boş sayılmaz).
- Salona sonradan yeni blok veya koltuk eklenebilir.
- `salon_olustur(ad, {blok: (sıra_sayısı, sıra_başına_koltuk)}, vip_bloklar)` ağacı kurar.
  Sıra adı `Blok-Sıra` (örn. `A-2`), sıra numarası 1'den başlar.

### K3. Tür fiyatı (etkinlik türüne göre)

| Tür | Kural |
| --- | --- |
| Konser | VIP koltuk: taban × 2,0. Standart koltuk: taban. |
| Tiyatro | Sıra no ≤ 3: taban × 1,25. Diğer sıralar: taban. |
| Konferans | Her koltuk taban fiyat. Açıklamada "Katılım sertifikası dahil" yazar. |

Bilet açıklamaları:
- Konser: `Konser: {etkinlik} | Koltuk {kod} ({kategori})`
- Tiyatro: `Tiyatro: {etkinlik} | Koltuk {kod} (sıra {sıra_no})`
- Konferans: `Konferans: {etkinlik} | Koltuk {kod} | Katılım sertifikası dahil`

### K4. Tarifeler (tür fiyatına uygulanır)

| Kod | Ad | Kural |
| --- | --- | --- |
| `standart` | Standart | İndirim yok. Tarife verilmezse varsayılan budur. |
| `ogrenci` | Öğrenci | %30 indirim. |
| `erken` | Erken kayıt | Etkinliğe **en az 30 gün** kaldıysa %20 indirim; daha azsa indirim yok. |
| `kurumsal` | Kurumsal | %15 indirim. |

Tarife bir biletin üzerinde sonradan değiştirilebilir; fiyat yeni tarifeye göre hesaplanır.

### K5. Ekstra hizmetler (tarifeden sonra eklenir, indirime girmez)

| Kod | Açıklamaya eklenen | Ücret |
| --- | --- | --- |
| `vip` | `+ VIP giriş` | +150 TL |
| `otopark` | `+ Otopark` | +75 TL |
| `sigorta` | `+ İptal sigortası` | Sardığı tutarın %10'u |

- Ekstralar seçildiği **sırayla** eklenir; aynı ekstra birden fazla eklenebilir.
- Sıra sigorta ücretini değiştirir: `sigorta` en sonda ise önceki ekstraları da sigortalar.
  Örnek (500 TL bilet): `vip, sigorta` → (500 + 150) × 1,10 = 715; `sigorta, vip` → 500 × 1,10 + 150 = 700.

### K6. Fiyat hesabı ve yuvarlama

`fiyat = yuvarla( tarife( tür_fiyatı ) )`, sonra her ekstra için `fiyat = yuvarla( fiyat + ekstra_ücreti )`.
Tutarlar `Decimal` ile hesaplanır; `yuvarla` iki basamağa, yarımlar yukarı (ROUND_HALF_UP).

### K7. Satış

- Satış yalnızca `Boş` veya `Tutuldu` koltuğa yapılır; sonunda koltuk `Satıldı` olur.
- Satış numaraları 1'den başlar, her başarılı satışta 1 artar; iptal numarayı geri vermez.
- Tarife veya ekstra kodu geçersizse (`GecersizSecimHatasi`) **koltuk satılmaz, kayıt oluşmaz.**
- Satılmış koltuğa satış `GecersizIslemHatasi` verir, kayıt oluşmaz.
- **Fiyat teklifi** satış yapmadan aynı fiyatı hesaplar; koltuğun durumunu değiştirmez.

### K8. İptal

- Satış iptal edilince koltuk `Boş` olur, kayıt `iptal_edildi = True` işaretlenir.
- İptal edilmiş satış tekrar iptal edilemez (`GecersizIslemHatasi`).
- İptal edilen koltuk yeniden satılabilir.

### K9. Rapor

- Toplam ciro ve etkinlik özeti yalnızca **geçerli** (iptal edilmemiş) satışları sayar.
- Etkinlik özeti her etkinlik için `(etkinlik, bilet sayısı, ciro)` verir, etkinlik sırasıyla.
- Satış listesi istenirse iptal edilenleri de gösterir.

### K10. Hatalar

| Hata | Ne zaman |
| --- | --- |
| `GecersizIslemHatasi` | Koltuk durumunda yapılamayan işlem, iptal edilmiş satışı tekrar iptal. |
| `BulunamadiHatasi` | Olmayan etkinlik (`'{kod}' kodlu etkinlik yok.`), koltuk, satış (`{no} numaralı satış yok.`). |
| `GecersizSecimHatasi` | Tanımsız tarife veya ekstra, menüde geçersiz numara. |

Hepsi `BiletSistemiHatasi`'ndan türer.

## 4. Örnek veri (`ornek_gise(bugun)`)

| Kod | Tür | Ad | Tarih | Salon | Bloklar | Taban |
| --- | --- | --- | --- | --- | --- | --- |
| K1 | Konser | Rock Gecesi | bugün + 45 gün | Açıkhava Sahnesi | A: 4 sıra × 10 (standart), B: 2 × 8 (VIP) — 56 koltuk | 500 TL |
| T1 | Tiyatro | Hamlet | bugün + 20 gün | Şehir Tiyatrosu | P: 6 × 8 — 48 koltuk | 300 TL |
| F1 | Konferans | Yazılım Mimarisi Zirvesi | bugün + 60 gün | Kongre Salonu | A: 5 × 10 — 50 koltuk | 200 TL |

Tarihler `bugun`e göre verildiği için erken kayıt indirimi konser ve konferansta geçerli,
tiyatroda geçersizdir. `bugun` verilmezse sistem tarihi kullanılır.

## 5. Kullanıcı arayüzü

`python3 main.py` menüyü açar:

| No | İşlem | Sorduğu bilgiler |
| --- | --- | --- |
| 1 | Etkinlikleri listele | — (kod, tür, ad, tarih, kalan gün, boş/kapasite) |
| 2 | Salon ve koltuk haritası | etkinlik kodu |
| 3 | Bilet satın al | etkinlik kodu → (harita gösterilir) → koltuk kodu → tarife no (1-4) → ekstra no'ları (virgülle, boş = yok) → teklif gösterilir → onay `E`/`H` |
| 4 | Koltuk tut | etkinlik kodu, koltuk kodu |
| 5 | Tutulan koltuğu bırak | etkinlik kodu, koltuk kodu |
| 6 | Satış iptal et | satış no |
| 7 | Satışlar ve rapor | — (iptaller dahil liste, etkinlik özeti, toplam ciro) |
| 0 | Çıkış | — |

- Koltuk haritası simgeleri: `.` boş, `T` tutuldu, `X` satıldı; blok başlığında kategori ve boş/kapasite.
- Hatalar `Hata: {mesaj}` olarak yazılır, program menüye döner (çökmez).
- Menüde 0-7 dışı seçim: `Geçersiz seçim, 0-7 arası bir sayı girin.`
- Tarife numarası geçersiz: `1-4 arası bir tarife numarası girin.`
- Ekstra numarası geçersiz: `'{parça}' geçerli bir ekstra numarası değil.`
- Satış no sayı değil: `Satış numarası bir sayı olmalı.`
- Onay `E` değilse: `Satın alma iptal edildi.`, satış yapılmaz.
- Girdi bittiğinde (EOF) veya `0` seçilince `Güle güle!` yazıp çıkar.

Diğer çalıştırma biçimleri:
- `python3 main.py --demo`: Menüyü hazır bir kullanıcı senaryosuyla çalıştırır (3 satış, 1 hatalı işlem, 1 iptal, rapor; toplam ciro 507,50 TL).
- `python3 main.py --kaliplar`: Beş kalıbı doğrudan sınıflarıyla tek tek gösterir.

## 6. Kalıp gereksinimleri (ders kuralları)

- En az dört GoF kalıbı; yaratımsal, yapısal ve davranışsal gruplardan en az biri.
  Bu projede: Factory Method, Composite, Decorator, Strategy, State.
- Her rol ayrı ve anlamlı adlandırılmış bir sınıfla karşılanır; arayüzler `abc.ABC` ile yazılır.
- Kalıplar elle yazılır (çerçeve veya kütüphanenin hazır kalıbı sayılmaz).
- Her rol, kodda `# [Kalıp adı kalıbı] Rol: RolAdı` biçiminde yorumla işaretlenir.
- Ayrıntılar: [TASARIM.md](TASARIM.md).

## 7. Gereksinim → test eşlemesi

| Kural | Test dosyası |
| --- | --- |
| K1 | `tests/test_durum.py`, `tests/test_gise.py` |
| K2 | `tests/test_salon.py`, `tests/test_arayuz.py` (harita) |
| K3 | `tests/test_etkinlik.py` |
| K4 | `tests/test_fiyat.py`, `tests/test_gise.py` |
| K5, K6 | `tests/test_ekstra.py`, `tests/test_gise.py` |
| K7, K8, K9, K10 | `tests/test_gise.py` |
| Bölüm 4 | `tests/test_gise.py` (`OrnekVeriTestleri`) |
| Bölüm 5 | `tests/test_arayuz.py` |
| Bölüm 6 | `tests/test_kalip_yapisi.py` |
