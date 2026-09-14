---
name: gorsel-handoff
description: Yarı otomatik görsel üretim döngüsü. Claude prompt ve yükleme paketini hazırlar, kullanıcı ChatGPT web arayüzüne (Go planı) yapıştırıp sonucu klasöre indirir, Claude dönen görseli kontrol listesiyle denetleyip onay ya da düzeltme promptu verir. Avenoxskills gptpro-handoff deseninden uyarlandı. "görsel üretelim", "karakter kartı", "chatgpt'ye görsel yaptıralım", "prompt hazırla", "görsel geldi bak", "şu görseli denetle" dendiğinde kullan.
---

# Görsel handoff döngüsü

ChatGPT web arayüzü ajan değildir: dosya sistemi yok, sadece yapıştırılan prompt ve
yüklenen görselleri görür. Otomasyon **yapılmaz** (OpenAI kullanım koşulları otomatik
kullanımı yasaklar; tarayıcı sürmek Claude kotasını yakar). Köprü kullanıcı'dır.
Codex `gpt-image-2` yalnızca yedektir, kotası küçüktür.

**Kural: model önerir, Claude denetler, onayı kullanıcı verir.** Hiçbir görsel denetimsiz
kullanılmaz, hiçbir aşama kullanıcının "tamam"ı olmadan geçilmez.

## Döngü

1. **Paket hazırla.** `<proje>/uretim/<asama>/<NN>-<ad>/` klasörü açılır. İçine
   `prompt.md` (yapıştırılacak metin, tek blok) ve `yukle/` (yüklenecek görseller,
   `1-...png`, `2-...png` diye numaralı) konur. Projenin kalıcı tarifleri
   (ör. `karakterler.md`) prompta **kopyalanır**, model başka dosya göremez.
2. **kullanıcıya ver.** Mesajda: hangi dosyaları hangi sırayla yükleyeceği, prompt dosyasının
   yolu ve promptun kendisi (kopyalaması kolay olsun diye kod bloğunda). Tek seferde bir görsel.
3. **kullanıcı sonucu koyar.** İndirdiği görseli aynı klasöre `sonuc-<n>.png` olarak atar.
4. **Denetle.** Görsel açılıp aşağıdaki kontrol listesiyle tek tek geçilir. Sonuç
   `denetim.md`'ye yazılır: her madde ✅/❌ ve kısa not.
5. **Karar.** Hepsi ✅ ise kullanıcıya gösterilir, onay istenir. ❌ varsa düzeltme promptu
   yazılır (aynı sohbette devam için) ve 2. adıma dönülür. **3 düzeltmede tutmazsa**
   yeni sohbette baştan, prompt yeniden kurulur — uzayan sohbet modeli kilitler.
6. **Günlük.** `uretim/gunluk.md`'ye tek satır: tarih, paket, deneme no, sonuç, gözlenen
   limit/hata. Go planının gerçek limitleri böyle öğrenilir ve bu skill'e işlenir.

## Prompt kalıbı (gpt-image için)

Sıra önemlidir: **kullanım → sahne → özne → ayrıntılar → stil → palet → kısıtlar.**

```
Kullanım: <masaüstü duvar kağıdı 16:9 | karakter referans sayfası | ...>
Yüklenen görseller: 1 = <rolü, ör. kompozisyon eskizi>, 2 = <rolü, ör. onaylı karakter kartı>
Sahne: <yer, zaman, hava, ışık>
Özne: <kim, duruş, kadraj, ekrandaki konumu>
Ayrıntılar: <kıyafet, silah, ifade — tarif dosyasından aynen>
Stil: <kelimeyle; sanatçı/eser adı verilmez, referans görsel yüklenmez>
Palet: <renk adları + hex>
Kısıtlar: yazı yok, filigran yok, imza yok; <eskizde yok sayılacaklar>; <negatif alan isteği>
```

- Eskiz yüklenirse rolü açıkça yazılır: "kompozisyon ve duruş için; çizgi kalitesini kopyalama".
- Düzeltme promptu **yalnızca değişecek şeyi** söyler: "Sadece X'i değiştir; Y ve Z aynen kalsın."
- Başkasına ait stil referans görselleri **yüklenmez**; stil kelimeyle tarif edilir.
- (2026-09-13 ölçüldü) Aynı sohbette düzeltme kimliği korur; "ilk sürümdeki yüze dön, son
  sürümdeki elbiseyi koru" gibi **sürüm birleştirme** tek turda tuttu. Tek düzeltmede 3 istek
  verilince model birini atladı → isteği 2 ile sınırla, en önemlisini başa yaz.
- "Tatlı/cute" kelimesi modeli çocuksu yüze itiyor; olgun karakterde "soft, calm, graceful" yaz.

## Denetim kontrol listesi

1. **Kimlik:** Tarif dosyasındaki her madde (saç, göz, yüz tipi, boy oranı, kıyafet, aksesuar) doğru mu?
2. **Tutarlılık:** Onaylı karakter kartıyla aynı kişi mi? (kart varsa)
3. **Kompozisyon:** Eskizdeki yerleşim, yön ve kadraj korunmuş mu?
4. **Palet:** Sadece izin verilen renkler mi; vurgu rengi yalnızca izin verilen yerlerde mi?
5. **Proje kuralları:** ör. rüzgâr yönü, negatif alan (UI'nin binmeyeceği boşluk).
6. **Teknik:** oran/çözünürlük hedefe yetiyor mu; yazı, filigran, bozuk el/parmak, fazla uzuv yok mu?
7. **His:** kullanıcının tarif ettiği karakter/atmosfer bu mu? (Son söz kullanıcının.)

## Doğrulanmamış varsayımlar (ilk denemelerde ölçülecek)

- 2026-09-13 ölçüldü: yatay 3:2 istenince ChatGPT (Go) **1536x1024 PNG** verdi, ilk denemede
  limit mesajı çıkmadı. 16:9 istenince **1672x941** (≈16:9) verdi; 1920x1080 için ~1,15x
  büyütme gerekir. İlk 6 görselde limit mesajı çıkmadı. (Eski not:) 3:2 gelirse üst/alt kırpma payı
  bırakılması istenir, sonra `magick` ile 16:9'a kırpılıp büyütülür.
- Go planının günlük görsel ve yükleme limiti bilinmiyor → `gunluk.md` doldukça buraya yazılır.
