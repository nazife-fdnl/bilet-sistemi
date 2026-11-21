# Kurulum Dokümanı

Bu doküman projeyi bilgisayarınıza indirmeyi, çalıştırmayı ve sık görülen
sorunların çözümünü anlatır.

## 1. Gereksinimler

| Gereksinim | Sürüm | Not |
| --- | --- | --- |
| Python | 3.9 veya üstü | Proje Python 3.9.6 ve 3.10 ile denenmiştir. |
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

```bash
python3 main.py
```

Demo programı beş tasarım kalıbını tek bir senaryoda çalıştırır: salonu kurar,
farklı tarifelerle bilet satar, ekstra hizmet ekler ve koltuk durumlarını gösterir.
Çıktının başı şöyle görünmelidir:

```
Etkinlik Bilet Satış ve Rezervasyon Sistemi - Demo

=== 1. Salon (Composite) ===
Salon(Kültür Merkezi, 52/52 boş)
  Blok(A, 40/40 boş)
  Blok(B, 12/12 boş)
```

Testlerin nasıl çalıştırılacağı için [TEST.md](TEST.md) dosyasına bakın.

## 5. Sık görülen sorunlar

| Sorun | Çözüm |
| --- | --- |
| `command not found: python3` | Python kurulu değil veya komut farklı: `python` ya da `py` deneyin; yoksa python.org'dan Python 3.9+ kurun. |
| `ModuleNotFoundError: No module named 'bilet_sistemi'` | Komutu proje klasörünün **içinden** çalıştırın (`main.py` dosyasının bulunduğu klasör). |
| `SyntaxError` veya tür ipuçlarıyla ilgili hata | Python sürümünüz 3.9'dan eski olabilir; `python3 --version` ile kontrol edin. |
| Türkçe karakterler bozuk görünüyor (Windows) | Terminalde `chcp 65001` çalıştırıp yeniden deneyin. |
