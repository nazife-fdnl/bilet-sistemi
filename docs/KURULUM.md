# Kurulum Dokümanı

Bu doküman projeyi bilgisayarınıza indirmeyi, çalıştırmayı ve sık görülen
sorunların çözümünü anlatır.

## 1. Gereksinimler

| Gereksinim | Sürüm | Not |
| --- | --- | --- |
| Python | 3.9 veya üstü | Proje Python 3.9, 3.10 ve 3.13 ile denenmiştir. |
| Git | Herhangi bir güncel sürüm | Yalnızca depoyu indirmek için gerekir. |

Proje yalnızca Python'un standart kütüphanesini kullanır. **Ek paket kurmanız gerekmez**
(`pip install` adımı yoktur).

Kurulu Python sürümünü görmek için:

```bash
python3 --version
```

Windows'ta komut `python3` yerine `python` veya `py` olabilir.

## 2. Projeyi indirme

**Git ile:**

```bash
git clone <depo-adresi>
cd bilet-sistemi
```

`<depo-adresi>` yerine GitHub sayfasındaki yeşil **Code** düğmesinden kopyalanan adresi yazın.

**Git olmadan:** GitHub sayfasında **Code → Download ZIP** ile indirip arşivi açın,
ardından terminalde açılan klasöre girin.

## 3. (İsteğe bağlı) Sanal ortam

Ek paket olmadığı için zorunlu değildir; sistem Python'unu temiz tutmak isterseniz:

```bash
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
```

## 4. Çalıştırma

Proje klasörünün içindeyken:

| Komut | Ne yapar |
| --- | --- |
| `python3 main.py` | Menülü uygulamayı açar; klavyeden kullanılır. Çıkmak için `0`. |
| `python3 main.py --demo` | Menüyü hazır bir kullanıcı senaryosuyla baştan sona çalıştırır (satış, hata, iptal, rapor). |
| `python3 main.py --kaliplar` | Beş tasarım kalıbını doğrudan sınıflarıyla tek tek gösterir. |
| `python3 main.py --help` | Seçenekleri listeler. |

Menü açıldığında şunu görmelisiniz:

```
Etkinlik Bilet Satış ve Rezervasyon Sistemi

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

Örnek kullanım: `3` → etkinlik kodu `K1` → koltuk `B-1-3` → tarife `3` (erken kayıt) →
ekstralar `1,3` (VIP giriş ve sigorta) → onay `E`. Tutar 1045,00 TL olmalıdır.
Menü ve kuralların tamamı: [GEREKSINIMLER.md](GEREKSINIMLER.md).

Testlerin nasıl çalıştırılacağı için [TEST.md](TEST.md) dosyasına bakın.

## 5. Sık görülen sorunlar

| Sorun | Çözüm |
| --- | --- |
| `command not found: python3` | Python kurulu değil veya komut farklı: `python` ya da `py` deneyin; yoksa python.org'dan Python 3.9+ kurun. |
| `ModuleNotFoundError: No module named 'bilet_sistemi'` | Komutu proje klasörünün **içinden** çalıştırın (`main.py` dosyasının bulunduğu klasör). |
| `SyntaxError` veya tür ipuçlarıyla ilgili hata | Python sürümünüz 3.9'dan eski olabilir; `python3 --version` ile kontrol edin. |
| Türkçe karakterler bozuk görünüyor (Windows) | Terminalde `chcp 65001` çalıştırıp yeniden deneyin. |
