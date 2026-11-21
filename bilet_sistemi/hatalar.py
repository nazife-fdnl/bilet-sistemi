"""Sistem genelinde kullanılan hata sınıfları."""


class BiletSistemiHatasi(Exception):
    """Sistemdeki tüm özel hataların ortak atası."""


class GecersizIslemHatasi(BiletSistemiHatasi):
    """Bir nesnenin o anki durumunda yapılamayacak bir işlem istendiğinde fırlatılır.

    Örnek: satılmış bir koltuğu tekrar tutmaya çalışmak.
    """
