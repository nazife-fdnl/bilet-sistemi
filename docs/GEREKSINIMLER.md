# Gereksinim Dokümanı

Bu doküman sistemin **ne yapması gerektiğini** tanımlar. Kod silinse bile bu doküman,
[TASARIM.md](TASARIM.md) (sınıflar, imzalar, kalıplar) ve `tests/` klasöründeki testler
birlikte projeyi aynı davranışla yeniden kurmaya yeter. Kurallardaki her sayı ve metin
testlerde doğrulanır.

Yazım kuralı: Bu dokümanda tutarlar okunaklılık için `1045,00 TL` diye yazılabilir;
**program çıktısında tutarlar `str(Decimal)` biçimindedir, yani noktalıdır: `1045.00 TL`.**
Ters tırnak içindeki metinler programın birebir yazdığı metinlerdir. Bunların dışındaki
satır düzeni (sütun hizaları, liste satırlarının biçimi) serbesttir; testler yalnızca
ters tırnakla verilen parçaları denetler.

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
| Salon | Bloklardan oluşan ağaç: Salon → Blok → Sıra → Koltuk. Salon, blok ve sıra `KoltukGrubu` nesneleridir; `tur` alanı sırasıyla `"Salon"`, `"Blok"`, `"Sıra"`. |
| Blok adı | Tek harf veya kısa ad, örn. `A`. Haritada `Blok A` diye yazılır. |
| Sıra adı | `Blok-SıraNo`, örn. `A-2`. Sıra numarası 1'den başlar. |
| Koltuk kodu | `Blok-Sıra-Numara`, örn. `B-1-3`. Gişe işlemlerinde kodlar büyük/küçük harf ve baştaki/sondaki boşluk duyarsızdır. |
| Koltuk kategorisi | `standart` veya `vip`. Bir blok VIP ise içindeki bütün koltuklar `vip`'tir. |
| Koltuk durumu | `Boş`, `Tutuldu`, `Satıldı` (`Koltuk.durum_adi`). |
| Taban fiyat | Etkinliğin tanımlandığı temel fiyat (TL). |
| Tür fiyatı | Etkinlik türünün kuralı uygulanmış, indirimsiz fiyat. |
| Tarife | Tür fiyatına uygulanan indirim kuralı (kod: `standart`, `ogrenci`, `erken`, `kurumsal`). |
| Ekstra hizmet | Bilete eklenen ücretli hizmet (kod: `vip`, `otopark`, `sigorta`). |
| Satış | Numaralı satış kaydı (`Satis`): `no`, `etkinlik`, `koltuk`, `bilet`, `tutar`, `tarife` (tarifenin **adı**, örn. `"Erken kayıt"`), `ekstralar` (ekstra **kodları** listesi, örn. `["vip", "sigorta"]`), `iptal_edildi`. |

## 3. İş kuralları

### K1. Koltuk durumları

Her koltuk `Boş` başlar. İzin verilen geçişler:

| Durum \ İşlem | `tut()` | `sat()` | `birak()` | `iptal_et()` | `musait_mi()` | `satilabilir_mi()` |
| --- | --- | --- | --- | --- | --- | --- |
| **Boş** | → Tutuldu | → Satıldı | hata | hata | True | True |
| **Tutuldu** | hata | → Satıldı | → Boş | hata | False | True |
| **Satıldı** | hata | hata | hata | → Boş | False | False |

"hata" = `GecersizIslemHatasi`. Mesajlar (`{kod}` koltuk kodu):

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
  üst seviye, alt seviyelerin toplamıdır. Tek koltuğun kapasitesi 1, `Boş` ise boş sayısı 1'dir.
- "Boş" sayılan koltuk yalnızca `Boş` durumundakidir (tutulan koltuk boş sayılmaz).
- Gruba sonradan bileşen eklenebilir (`ekle`) ve çıkarılabilir (`cikar`). `cikar` yalnızca
  doğrudan çocuklar için geçerlidir; olmayan bileşen için `ValueError` verir (listeden silme).
- Bir grup kendi içine (doğrudan veya alt gruplarının içine) eklenemez:
  `{grup}: bir grup kendi içine eklenemez.` Aynı bileşen bir gruba iki kez eklenemez:
  `{grup}: {bileşen} zaten bu grupta.` (ikisi de `GecersizIslemHatasi`). Tekrar denetimi
yalnızca doğrudan çocuklara bakar; kendi içine ekleme denetimi bütün alt ağaca bakar.
- `KoltukGrubu.koltuk_bul(kod)` koltuk yoksa **`None`** döndürür; gişe bunu `BulunamadiHatasi`'na çevirir (K10).
- `salon_olustur(ad, {blok: (sıra_sayısı, sıra_başına_koltuk)}, vip_bloklar)` ağacı kurar
  (blok sırası sözlük sırasıdır).
- Metin gösterimleri: `str(KoltukGrubu)` = `{tur}({ad}, {boş}/{kapasite} boş)`, örn.
  `Salon(Kültür Merkezi, 49/52 boş)`; `str(Koltuk)` = `Koltuk({kod}, {durum})`, örn. `Koltuk(A-5-8, Tutuldu)`.

### K3. Tür fiyatı (etkinlik türüne göre)

| Tür | Kural |
| --- | --- |
| Konser | VIP koltuk: taban × 2,0. Standart koltuk: taban. |
| Tiyatro | Sıra no ≤ 3: taban × 1,25. Diğer sıralar: taban. |
| Konferans | Her koltuk taban fiyat. |

Bilet açıklamaları (`aciklama()`):
- Konser: `Konser: {etkinlik} | Koltuk {kod} ({kategori})`
- Tiyatro: `Tiyatro: {etkinlik} | Koltuk {kod} (sıra {sıra_no})`
- Konferans: `Konferans: {etkinlik} | Koltuk {kod} | Katılım sertifikası dahil`

### K4. Tarifeler (tür fiyatına uygulanır)

Tablo sırası menüdeki sıradır (menü no = sıra).

| Menü no | Kod | Ad (`strateji.ad`, `Satis.tarife`) | Menüde görünen | Kural |
| --- | --- | --- | --- | --- |
| 1 | `standart` | `Standart` | `Standart` | İndirim yok. Tarife verilmezse varsayılan budur. |
| 2 | `ogrenci` | `Öğrenci` | `Öğrenci (%30 indirim)` | %30 indirim. |
| 3 | `erken` | `Erken kayıt` | `Erken kayıt (30+ gün kala %20 indirim)` | Etkinliğe **en az 30 gün** kaldıysa %20 indirim; daha azsa indirim yok. |
| 4 | `kurumsal` | `Kurumsal` | `Kurumsal (%15 indirim)` | %15 indirim. |

Tarife bir biletin üzerinde sonradan değiştirilebilir (`bilet.fiyat_stratejisi = ...`); fiyat yeni tarifeye göre hesaplanır.

### K5. Ekstra hizmetler (tarifeden sonra eklenir, indirime girmez)

| Menü no | Kod | Menüde görünen | Açıklamaya eklenen | Ücret |
| --- | --- | --- | --- | --- |
| 1 | `vip` | `VIP giriş (+150 TL)` | ` + VIP giriş` | +150 TL |
| 2 | `otopark` | `Otopark (+75 TL)` | ` + Otopark` | +75 TL |
| 3 | `sigorta` | `İptal sigortası (+%10)` | ` + İptal sigortası` | Sardığı tutarın %10'u |

- Ekstralar seçildiği **sırayla** eklenir; aynı ekstra birden fazla eklenebilir.
- Sıra sigorta ücretini değiştirir: `sigorta` en sonda ise önceki ekstraları da sigortalar.
  Örnek (500 TL bilet): `vip, sigorta` → (500 + 150) × 1,10 = 715; `sigorta, vip` → 500 × 1,10 + 150 = 700.
- Çok sayıda ekstra iç içe eklendiğinde de hesap hızlıdır (her katman içteki fiyatı bir kez sorar).

### K6. Fiyat hesabı ve yuvarlama

`fiyat = yuvarla( tarife( tür_fiyatı ) )`, sonra her ekstra için
`fiyat = yuvarla( iç_fiyat + ekstra_ücreti(iç_fiyat) )`. Sigorta ücreti ayrıca yuvarlanmaz;
yalnızca toplam yuvarlanır. Tutarlar `Decimal` ile hesaplanır; `yuvarla` iki basamağa,
yarımlar yukarı (ROUND_HALF_UP).

### K7. Satış

- Satış yalnızca `Boş` veya `Tutuldu` koltuğa yapılır; sonunda koltuk `Satıldı` olur.
- Etkinlik tarihi geçmişse (`kalan_gun < 0`) satış yapılmaz:
  `{etkinlik} etkinliği geçmişte kaldı; bilet satılamaz.` (`GecersizIslemHatasi`).
- `satin_al` denetim sırası: etkinlik → koltuk → etkinlik tarihi → tarife → ekstralar → satış
  (`bilet_sat`, koltuk durumu). İlk başarısız denetimin hatası fırlatılır.
- `fiyat_teklifi` tarih ve satılabilirlik denetimi yapmaz; satılmış koltuk uyarısını
  (`koltuk satılamaz (durum: …)`) arayüz, tarife sormadan önce verir.
- Satış numaraları 1'den başlar, her başarılı satışta 1 artar; iptal numarayı geri vermez.
- Tarife veya ekstra kodu geçersizse (`GecersizSecimHatasi`) **koltuk satılmaz, kayıt oluşmaz.**
- Satılmış koltuğa satış `GecersizIslemHatasi` verir, kayıt oluşmaz.
- Satışın **tutarı satış anında sabitlenir** (`Satis.tutar`); fiyat kuralları sonradan değişse de geçmiş satış ve rapor değişmez.
- **Fiyat teklifi** satış yapmadan aynı fiyatı hesaplar; koltuğun durumunu değiştirmez.

### K8. İptal

- Satış iptal edilince koltuk `Boş` olur, kayıt `iptal_edildi = True` işaretlenir.
- İptal edilmiş satış tekrar iptal edilemez: `{no} numaralı satış zaten iptal edilmiş.` (`GecersizIslemHatasi`).
- İptal edilen koltuk yeniden satılabilir.

### K9. Rapor

- Toplam ciro ve etkinlik özeti yalnızca **geçerli** (iptal edilmemiş) satışları sayar.
- Etkinlik özeti her etkinlik için `(etkinlik, bilet sayısı, ciro)` verir, etkinlik sırasıyla.
- Satış listesi istenirse iptal edilenleri de gösterir.

### K10. Hatalar

Hepsi `BiletSistemiHatasi`'ndan türer. Mesajlarda `{kod}` kullanıcının yazdığı kodun
baştaki/sondaki boşlukları silinmiş, harfleri **değiştirilmemiş** hâlidir; `{etkinlik}` etkinlik
adıdır (`Etkinlik.ad`).

| Hata | Mesaj | Ne zaman |
| --- | --- | --- |
| `GecersizIslemHatasi` | K1, K2, K7, K8'deki mesajlar | Durumda yapılamayan işlem, geçersiz ağaç ekleme, geçmiş etkinlik, ikinci iptal |
| `BulunamadiHatasi` | `'{kod}' kodlu etkinlik yok.` | Olmayan etkinlik kodu |
| `BulunamadiHatasi` | `{etkinlik} salonunda '{kod}' kodlu koltuk yok.` | Olmayan koltuk kodu (gişe) |
| `BulunamadiHatasi` | `{no} numaralı satış yok.` | Olmayan satış no |
| `GecersizSecimHatasi` | `'{kod}' diye bir tarife yok.` | Tanımsız tarife kodu |
| `GecersizSecimHatasi` | `'{kod}' diye bir ekstra hizmet yok.` | Tanımsız ekstra kodu |
| `GecersizSecimHatasi` | Bölüm 5'teki menü mesajları | Menüde geçersiz numara |

## 4. Örnek veri (`ornek_gise(bugun)`)

| Kod | Tür | Ad | Tarih | Salon | Bloklar | Taban |
| --- | --- | --- | --- | --- | --- | --- |
| K1 | Konser | Rock Gecesi | bugün + 45 gün | Açıkhava Sahnesi | A: 4 sıra × 10 (standart), B: 2 × 8 (VIP) — 56 koltuk | 500 TL |
| T1 | Tiyatro | Hamlet | bugün + 20 gün | Şehir Tiyatrosu | P: 6 × 8 — 48 koltuk | 300 TL |
| F1 | Konferans | Yazılım Mimarisi Zirvesi | bugün + 60 gün | Kongre Salonu | A: 5 × 10 — 50 koltuk | 200 TL |

`Etkinlik.tur` tam olarak `"Konser"`, `"Tiyatro"` veya `"Konferans"`tır.
Tarihler `bugun`e göre verildiği için erken kayıt indirimi konser ve konferansta geçerli,
tiyatroda geçersizdir. `bugun` verilmezse sistem tarihi kullanılır.

## 5. Kullanıcı arayüzü

`python3 main.py` önce `Etkinlik Bilet Satış ve Rezervasyon Sistemi` yazar, sonra menüyü gösterir:

```
========= BİLET GİŞESİ =========
1) Etkinlikleri listele
2) Salon ve koltuk haritası
3) Bilet satın al
4) Koltuk tut
5) Tutulan koltuğu bırak
6) Satış iptal et
7) Satışlar ve rapor
0) Çıkış
================================
Seçiminiz:
```

| No | İşlem | Sorular (sırasıyla) | Başarı çıktısı |
| --- | --- | --- | --- |
| 1 | Etkinlikleri listele | — | Her etkinlik için kod, tür, ad, tarih (ISO), kalan gün, `boş/kapasite` |
| 2 | Salon ve koltuk haritası | `Etkinlik kodu (ör. K1): ` | `{ad} ({tür})` satırı ve koltuk haritası |
| 3 | Bilet satın al | `Etkinlik kodu (ör. K1): ` → (harita) → `Koltuk kodu (ör. A-1-5): ` → tarife listesi, `Tarife no: ` → ekstra listesi, `Ekstra no(lar): ` (virgülle; boş = yok) → teklif → `Onaylıyor musunuz? (E/H): ` | Teklif: `Bilet : {açıklama}` ve `Tutar : {tutar} TL`; onaydan sonra `Satış tamamlandı. Satış no: {no}  Tutar: {tutar} TL` |
| 4 | Koltuk tut | `Etkinlik kodu (ör. K1): `, `Koltuk kodu: ` | `{kod} koltuğu tutuldu.` |
| 5 | Tutulan koltuğu bırak | `Etkinlik kodu (ör. K1): `, `Koltuk kodu: ` | `{kod} koltuğu bırakıldı, yeniden satışta.` |
| 6 | Satış iptal et | `İptal edilecek satış no: ` | `{no} numaralı satış iptal edildi, {kod} koltuğu yeniden satışta.` |
| 7 | Satışlar ve rapor | — | Satış yoksa `Henüz satış yok.`; varsa her satış (iptaller dahil, durum `Geçerli` / `İPTAL`); `Etkinlik bazında:` özeti; `Toplam ciro: {tutar} TL` |
| 0 | Çıkış | — | `Güle güle!` |

Satın almada koltuk satılamaz durumdaysa (`Satıldı`) teklif verilmez, tarife sorulmaz:
`{kod}: koltuk satılamaz (durum: Satıldı).` (`GecersizIslemHatasi`). Onay cevabı büyük/küçük
harf duyarsızdır; `E` dışındaki her cevapta `Satın alma iptal edildi.` yazılır, satış yapılmaz.

**Hatalı girişler.** Her hatalı giriş `Hata: {mesaj}` olarak yazılır, **o işlem sona erer ve
ana menüye dönülür** (soru tekrar sorulmaz, program çökmez). Menü mesajları:

| Durum | Yazılan |
| --- | --- |
| Menüde 0-7 dışı seçim | `Geçersiz seçim, 0-7 arası bir sayı girin.` (`Hata:` öneki yok) |
| Tarife numarası 1-4 dışı veya sayı değil | `Hata: 1-4 arası bir tarife numarası girin.` |
| Ekstra numarası 1-3 dışı veya sayı değil | `Hata: '{parça}' geçerli bir ekstra numarası değil.` |
| Satış no sayı değil | `Hata: Satış numarası bir sayı olmalı.` |

"Sayı" yalnızca ASCII rakamlardır (`0-9`); `²` gibi karakterler sayı sayılmaz.
Girdi bittiğinde (EOF) veya Ctrl-C'de program `Güle güle!` yazıp çıkar.

**Koltuk haritası** (`koltuk_haritasi(salon)`), örnek (`.` boş, `T` tutuldu, `X` satıldı):

```
Kongre Salonu  |  boş 49 / 50
Simgeler: . boş   T tutuldu   X satıldı

Blok A (standart)  boş 49 / 50
         1  2  3  4  5  6  7  8  9 10
  A-1    .  .  .  .  T  .  .  .  .  .
  A-2    .  .  .  .  .  .  .  .  .  .
```

Her sıra satırı sıra adıyla başlar ve ardından yalnızca simgeler gelir. Blok başlığındaki
kategori bloğun ilk koltuğunun kategorisidir.

### Demo modları

`python3 main.py --demo` menüyü `ornek_gise()` ile şu cevaplarla çalıştırır
(`KULLANICI_SENARYOSU`): listele; K1 haritası; **K1 B-1-3** erken kayıt + VIP giriş + sigorta
(1045.00, satış 1); **T1 P-2-4** öğrenci (262.50, satış 2); F1 A-1-5 tut; **F1 A-1-5** kurumsal +
otopark (245.00, satış 3); K1 B-1-3 tutmayı dene → `Hata: B-1-3: satılmış koltuk tutulamaz.`;
satış 1'i iptal et; rapor (`Toplam ciro: 507.50 TL`); K1 haritası; `0`.
Cevaplar `senaryo_girdisi` ile soruyla birlikte ekrana yazılır (`Seçiminiz: 1`).

`python3 main.py --kaliplar` beş kalıbı doğrudan sınıflarıyla gösterir:
1. `salon_olustur("Kültür Merkezi", {"A": (5, 8), "B": (2, 6)}, vip_bloklar=["B"])` (52 koltuk) yazdırılır.
2. `KonserOlusturucu("Rock Gecesi", Decimal("500"))` ile A-3-4 standart (500.00), A-3-5 öğrenci (350.00), B-1-1 erken kayıt 45 gün (800.00) satılır.
3. `TiyatroOlusturucu("Hamlet", Decimal("300"))` ile A-1-1 kurumsal satılır (300 × 1,25 × 0,85 = 318.75).
4. A-3-4 bileti `IptalSigortasi(Otopark(VipGiris(bilet)))` ile sarılır: `Toplam: 797.50 TL`.
5. A-5-8 tutulup bırakılır; satılmış A-3-4'e tekrar satış denenir (hata yazdırılır); A-3-4 iptal edilir.
6. Son durum: `Salon(Kültür Merkezi, 49/52 boş)`.

## 6. Kalıp gereksinimleri (ders kuralları)

- En az dört GoF kalıbı; yaratımsal, yapısal ve davranışsal gruplardan en az biri.
  Bu projede: Factory Method, Composite, Decorator, Strategy, State.
- Her rol ayrı ve anlamlı adlandırılmış bir sınıfla karşılanır; arayüzler `abc.ABC` ile yazılır.
- Kalıplar elle yazılır (çerçeve veya kütüphanenin hazır kalıbı sayılmaz).
- Her rol, kodda `# [Kalıp adı kalıbı] Rol: RolAdı` biçiminde yorumla işaretlenir.
- Ayrıntılar ve bütün imzalar: [TASARIM.md](TASARIM.md).

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
