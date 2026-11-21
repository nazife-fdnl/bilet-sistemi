# Test Dokümanı

Testler Python'un standart `unittest` modülüyle yazılmıştır; ek paket gerekmez.
Her tasarım kalıbının kendi test dosyası vardır.

## 1. Bütün testleri çalıştırma

Proje klasörünün içindeyken:

```bash
python3 -m unittest -v
```

Beklenen sonucun sonu:

```
----------------------------------------------------------------------
Ran 36 tests in 0.001s

OK
```

`OK` yazısı bütün testlerin geçtiğini gösterir. Başarısız bir test olursa
`FAILED (failures=1)` gibi bir satır ve hatanın ayrıntısı yazılır.

## 2. Tek bir kalıbın testlerini çalıştırma

```bash
python3 -m unittest tests.test_durum -v      # yalnızca State testleri
```

## 3. Test dosyaları

| Dosya | Kalıp | Test sayısı | Ne doğrulanıyor |
| --- | --- | --- | --- |
| `tests/test_durum.py` | State | 9 | Koltuğun Boş → Tutuldu → Satıldı geçişleri; geçersiz işlemlerin (ör. satılmış koltuğu tekrar tutmak) `GecersizIslemHatasi` vermesi |
| `tests/test_salon.py` | Composite | 6 | Kapasite ve boş koltuk sayısının salon, blok ve sıra seviyelerinde doğru toplanması; tek koltuk ile grubun aynı arayüzü kullanması; ağaca yeni blok eklenebilmesi |
| `tests/test_etkinlik.py` | Factory Method | 6 | Her oluşturucunun kendi bilet türünü üretmesi; konser (VIP), tiyatro (ön sıra) ve konferans (tek fiyat) kuralları; satılmış koltuğa bilet verilmemesi |
| `tests/test_fiyat.py` | Strategy | 8 | Standart, öğrenci, erken kayıt ve kurumsal tarifeler; stratejinin etkinlik kuralından sonra uygulanması; stratejinin çalışma anında değiştirilebilmesi |
| `tests/test_ekstra.py` | Decorator | 7 | Ekstraların fiyata ve açıklamaya eklenmesi; iç içe ve tekrarlı sarma; sarma sırasının sigorta ücretini değiştirmesi; indirimin ekstra ücretlere uygulanmaması |
| **Toplam** | | **36** | |

## 4. Örnek senaryolar ve beklenen değerler

Testlerde kullanılan bazı hesaplar, sonuçları elle kontrol edebilmeniz için:

| Senaryo | Hesap | Beklenen |
| --- | --- | --- |
| Konser, standart koltuk | 500 | 500,00 TL |
| Konser, VIP koltuk | 500 × 2 | 1000,00 TL |
| Tiyatro, 1. sıra, öğrenci | 300 × 1,25 × 0,70 | 262,50 TL |
| Konser + VIP giriş + otopark | 500 + 150 + 75 | 725,00 TL |
| Sigorta en dışta: Sigorta(VIP(bilet)) | (500 + 150) × 1,10 | 715,00 TL |
| Sigorta içte: VIP(Sigorta(bilet)) | 500 × 1,10 + 150 | 700,00 TL |

## 5. Yeni test eklemek

1. İlgili `tests/test_*.py` dosyasını açın.
2. Sınıfın içine adı `test_` ile başlayan bir metot ekleyin.
3. `self.assertEqual`, `self.assertTrue` veya `self.assertRaises` ile beklenen sonucu yazın.
4. `python3 -m unittest -v` ile çalıştırın.
