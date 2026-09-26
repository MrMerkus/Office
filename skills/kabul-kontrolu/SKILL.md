---
name: kabul-kontrolu
description: Bir işin gerçekten bittiğini, bitiren tarafın raporuna değil ana döngünün kendi ölçümüne dayanarak doğrular. Alanına göre kabul kanıtının ne olduğunu söyler — şeritte değişen dosya, görselde ekran görüntüsü, serviste is-active, üründe düşman koşul. "bitti", "tamamlandı", "hazır", "şerit bitti", "teslim ettim", "yayına aldık", "testler geçti", "servisi kurdum", "çalışıyor", "sorunsuz", "başarılı" dendiğinde veya bir delege şeridi, script, test, kurulum ya da teslimat sonuçlandığında kullan.
---

# Kabul kontrolü

Tek ilke: **"bitti" diyen taraf, "bitti"yi ölçen taraf olamaz.**

Bu kural `🔮 zihin/Kurallar.md` dosyasında yıllardır yazılıydı ve gözlem defterinde **on kez**
delindi (0003, 0004, 0007, 0008, 0010, 0011, 0015, 0020, 0027, 0030). Delinmesinin sebebi
kuralın yokluğu değil, soyutluğuydu: "sonucu ayrıca ölç" cümlesi, elinde `ls` varken `ls`
yapmanı engellemiyor. Bu skill o cümlenin somut karşılığını verir.

## Kabul kanıtı tablosu

İşin alanını bul, karşısındaki kanıtı **kendi elinle** al. Şeridin, script'in ya da aracın
raporu bu sütuna girmez.

| Alan | Kabul kanıtı | Nereden geldi |
| --- | --- | --- |
| Delege şeridi (agy, Codex) | `git diff --stat` ya da değişen dosya listesi. Hiçbir dosya değişmediyse şerit başarısızdır — çıkış kodu ne derse desin | 0007, 0027 |
| Görsel iş | Ana döngünün kendi baktığı ekran görüntüsü. Delege güzelliği ölçemez; brief'e ölçülebilir kısıt yaz ("kenarlardan %12 boşluk") | 0011 |
| Kırılgan ortam (USB, ağ sürücüsü, uzak disk) | Ayır, tekrar tak, geri oku, sağlama topla. `ls` yetmez — o da önbelleği okur | 0015 |
| Kendi script veya testimiz | Ayrıştırılan satırı **say**, beklenenle karşılaştır; 0 satır bir hatadır. Dış komut ayrıştırılırken `NO_COLOR=1`, `TERM=dumb` ver, ANSI dizilerini temizle | 0003, 0004 |
| Test iskelesi | Beklenmedik başarısızlıkta önce iskeleyi doğrula. Taklit edilen fonksiyon yalnızca aynı değeri değil, **aynı akışı** üretmeli (`exit`, `raise`, `return` birbirinin yerine geçmez) | 0003 |
| Gerçek girdiye dayanan özellik | Kabul testi simülasyon yolundan değil, gerçek sensör/veri yolundan geçmeli. Sahte veri gerçek yolu atlıyorsa yeşil test anlamsızdır | 0030 |
| Servis veya daemon kurulumu | Birkaç saniye **sonra** `is-active` ve journal. Etkileşimli ilk onayı servisten önce elle ver; terminalsiz ortamda soru çıkış kodu 0 ile kapanır | 0020 |
| Teslim edilen ürün | Dönüşüm yolunu düşman koşulda dene: reklam engelleyici açık, üçüncü taraf script bloklu, ağ yavaş. Telefon, WhatsApp, form ayrı ayrı tıklanır | 0008 |
| Spec'e yazılan dış gerçek | URL, paket sürümü, API adı yazılmadan **önce** canlı doğrula (`curl -sI`). "Biliyorum" yeterli değil; eğitim verisi yanlış sürüm biçimi hatırlatır | 0010 |

## Ne zaman atlanır

Kabul kontrolü ücretsiz değildir. Geri alınabilir, tek adımlı ve sonucu zaten gözünün önünde
olan işlerde (tek dosya okuma, sohbet, tek satırlık düzenleme) atlanır. Zorunlu olduğu yer:
**sonucu göremediğin** her iş — arka planda çalışan şerit, başka makinede açılan sayfa,
kullanıcının elindeki ürün, kırılgan ortama yazma, uzun süre sonra patlayacak kurulum.

## Sınır

Bu skill hata aramaz, **iddiayı doğrular**. Kabul kanıtı alındıktan sonra kod kalitesi
sorusu ayrı bir iştir.
