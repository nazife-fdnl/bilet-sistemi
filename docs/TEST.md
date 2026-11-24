# Test Dokümanı

Testler Python'un standart `unittest` modülüyle yazılmıştır; ek paket gerekmez.
Her tasarım kalıbının kendi test dosyası, ayrıca gişe (uçtan uca), arayüz ve kalıp yapısı
testleri vardır. Testler [GEREKSINIMLER.md](GEREKSINIMLER.md)'deki kuralları doğrular.

## 1. Bütün testleri çalıştırma

Proje klasörünün içindeyken:

```bash
python3 -m unittest -v
```

Beklenen sonucun sonu (süre değişebilir):

```
----------------------------------------------------------------------
Ran 81 tests in 0.012s

OK
```

`OK` yazısı bütün testlerin geçtiğini gösterir. Başarısız bir test olursa
`FAILED (failures=1)` gibi bir satır ve hatanın ayrıntısı yazılır.

## 2. Tek bir dosyayı veya testi çalıştırma

```bash
python3 -m unittest tests.test_durum -v                                   # yalnızca State testleri
python3 -m unittest tests.test_gise.SatisTestleri.test_tiyatro_ogrenci   # tek bir test
```

## 3. Test dosyaları

| Dosya | Kapsam | Test | Ne doğrulanıyor |
| --- | --- | --- | --- |
| `tests/test_durum.py` | State | 9 | Boş → Tutuldu → Satıldı geçişleri; geçersiz işlemlerin `GecersizIslemHatasi` vermesi |
| `tests/test_salon.py` | Composite | 6 | Kapasite ve boş koltuğun her seviyede toplanması; tek koltuk ile grubun aynı arayüzü kullanması; ağaca blok eklenmesi |
| `tests/test_etkinlik.py` | Factory Method | 6 | Her oluşturucunun kendi bilet türünü üretmesi; konser, tiyatro, konferans fiyat kuralları; satılmış koltuğa bilet verilmemesi |
| `tests/test_fiyat.py` | Strategy | 8 | Dört tarife; stratejinin tür fiyatından sonra uygulanması; çalışma anında değiştirilmesi |
| `tests/test_ekstra.py` | Decorator | 7 | Ekstraların fiyata ve açıklamaya eklenmesi; iç içe ve tekrarlı sarma; sarma sırasının etkisi; indirimin ekstralara uygulanmaması |
| `tests/test_gise.py` | Uygulama (uçtan uca) | 25 | Örnek veri; satış, fiyat teklifi, tutma/bırakma, iptal, rapor; geçersiz seçimde koltuğun satılmaması; hata türleri |
| `tests/test_arayuz.py` | Arayüz | 13 | Menü akışları, onay, hata mesajları, koltuk haritası, `--demo` ve `--kaliplar` senaryoları |
| `tests/test_kalip_yapisi.py` | Kalıp yapısı | 7 | Arayüzlerin soyut `abc.ABC` olması, somut sınıfların doğru arayüzden türemesi, rol yorumlarının kodda bulunması |
| **Toplam** | | **81** | |

## 4. Örnek senaryolar ve beklenen değerler

Testlerdeki hesaplar, sonuçları elle kontrol edebilmeniz için:

| Senaryo | Hesap | Beklenen |
| --- | --- | --- |
| Konser, standart koltuk | 500 | 500,00 TL |
| Konser, VIP koltuk | 500 × 2 | 1000,00 TL |
| Konser VIP, erken kayıt, VIP giriş + sigorta | ((500 × 2 × 0,80) + 150) × 1,10 | 1045,00 TL |
| Tiyatro 2. sıra, öğrenci | 300 × 1,25 × 0,70 | 262,50 TL |
| Tiyatro 2. sıra, erken kayıt (20 gün kala, indirim yok) | 300 × 1,25 | 375,00 TL |
| Konferans, kurumsal + otopark | 200 × 0,85 + 75 | 245,00 TL |
| Sigorta en dışta: Sigorta(VIP(500 TL)) | (500 + 150) × 1,10 | 715,00 TL |
| Sigorta içte: VIP(Sigorta(500 TL)) | 500 × 1,10 + 150 | 700,00 TL |
| `--demo` senaryosu sonunda toplam ciro | 262,50 + 245,00 (1045,00 iptal) | 507,50 TL |

## 5. Elle (manuel) test senaryosu

`python3 main.py` ile:

1. `1` → üç etkinlik listelenir.
2. `4`, `F1`, `A-1-5` → "A-1-5 koltuğu tutuldu."; `2`, `F1` → haritada `T` görünür.
3. `3`, `F1`, `A-1-5`, `4`, `2`, `E` → "Satış tamamlandı. Satış no: 1  Tutar: 245.00 TL".
4. `4`, `F1`, `A-1-5` → "Hata: A-1-5: satılmış koltuk tutulamaz."
5. `6`, `1` → satış iptal edilir; `7` → satış "İPTAL", toplam ciro 0.00 TL.
6. `0` → "Güle güle!"

## 6. Yeni test eklemek

1. İlgili `tests/test_*.py` dosyasını açın.
2. Sınıfın içine adı `test_` ile başlayan bir metot ekleyin.
3. `self.assertEqual`, `self.assertTrue` veya `self.assertRaises` ile beklenen sonucu yazın.
4. `python3 -m unittest -v` ile çalıştırın.
