"""Sistem genelinde kullanılan hata sınıfları."""


class BiletSistemiHatasi(Exception):
    """Sistemdeki tüm özel hataların ortak atası."""


class GecersizIslemHatasi(BiletSistemiHatasi):
    """Bir nesnenin o anki durumunda yapılamayacak bir işlem istendiğinde fırlatılır.

    Örnek: satılmış bir koltuğu tekrar tutmaya çalışmak.
    """


class BulunamadiHatasi(BiletSistemiHatasi):
    """Kodu verilen etkinlik, koltuk veya satış bulunamadığında fırlatılır."""


class GecersizSecimHatasi(BiletSistemiHatasi):
    """Tanımlı olmayan bir tarife veya ekstra hizmet seçildiğinde fırlatılır."""
