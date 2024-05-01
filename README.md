# Knight Online ASAS Macro Programı (Güncellenmiş Versiyon)

Knight Online oyunu için tasarlanmış bu gelişmiş makro programı, oyuncuların otomatik saldırı, can (HP) ve mana (MP) yenileme, ve destek (minor) becerilerini kullanarak oyun içindeki performanslarını artırmalarını sağlar. Güncellenmiş versiyonu ile daha kapsamlı özellikler ve kullanıcı dostu bir arayüz sunulmaktadır.

### Özellikler

- **Otomatik Saldırı (Attack) Özelliği:** Karakterin düşmanlara karşı belirlenen tuş kombinasyonlarıyla otomatik olarak saldırı becerilerini kullanmasını sağlar.
- **Can ve Mana Yenileme:** HP ve MP seviyeleri belirli bir eşiğin altına düştüğünde, otomatik olarak ilgili tuşlara basarak can ve mana yenileme işlemi gerçekleştirilir.
- **Otomatik Destek (Minor) Özelliği:** Karakterin canını hızlı bir şekilde yenilemesini sağlayan minor becerilerinin otomatik olarak kullanılmasını sağlar.
- **Karakter Sınıfına Özel Stratejiler:** Asas, BP/Warrior, ve Okçu karakter sınıfları için özel saldırı ve destek stratejileri.
- **Kontrol Kolaylığı:** Caps Lock tuşu ile makro programı etkinleştirilip devre dışı bırakılabilir, bu sayede oyun içi kontrol esnekliği sağlanır.
- **Kullanıcı Arayüzü:** Programın durumunu gösteren renkli gösterge ve daima üstte kalma özelliği ile kullanıcı dostu bir arayüz.

### Kurulum ve Başlatma

1. **Python Kurulumu:** Program, Python programlama dilinde yazılmıştır. Bilgisayarınızda Python'un yüklü olduğundan emin olun.
2. **Gerekli Kütüphanelerin Kurulumu:** Programın çalışması için `pynput`, `pyautogui`, `tkinter`, `threading`, `time`, `ctypes`, ve `PIL` kütüphanelerinin yüklenmesi gerekmektedir. Bu kütüphaneleri yüklemek için terminal veya komut istemcisine `pip install pynput pyautogui Pillow` gibi komutlar yazabilirsiniz. Alternatif olarak sanal ortam yaratıp gerekli modülleri `pip install -r requirements.txt` komutuyla yükleyebilirsiniz. Program Windows işletim sistemini desteklemektedir.
3. **Makro Kodunun Çalıştırılması:** Makro kodunu bir Python dosyasına yapıştırın ve Python yorumlayıcısı ile çalıştırın.

## Kullanım Talimatları

1. **Makro Programını Başlatın:** Programı çalıştırdığınızda, otomatik olarak dinlemeye başlar.
2. **Otomatik Modu Etkinleştirme/Kapatma:** Caps Lock tuşunu açık konuma getirerek otomatik saldırı ve destek modlarını etkinleştirebilirsiniz. Caps Lock tuşunu kapatarak bu modları devre dışı bırakabilirsiniz.
3. **Karakter Sınıfını Seçme:** Arayüzdeki radyo butonları aracılığıyla karakter sınıfınızı seçin. Bu seçim, makronun saldırı ve destek stratejilerini belirler.
4. **Asas Tuş dizilimi:** 1 lightfeet, 2-3-4-5-6-7 saldırı, 8-9-0 minor mana.
5. **BP/Warrior Tuş dizilimi:** 2 atack 7 mana 8 can pot.
6.  **Okçu Tuş dizilimi:** 2 5li ok 3 3lü ok 7 mana 8 can pot.

Bu güncellenmiş versiyon, kullanıcıların oyun içinde daha etkin ve verimli olmalarını sağlamak üzere tasarlanmıştır. Makro kullanımı oyunun kuralları ve topluluk anlaşmalarına bağlı olarak değişebileceğinden, kullanımından önce ilgili kuralları gözden geçirmeniz önerilir.
