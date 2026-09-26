---
name: site
description: Website ve arayüz işleri kümesi. Müşteriye site yapma, sayfa tasarlama, arayüz düzeltme, yayına alma işlerini kapsar; içindeki skilleri tek tek onay alarak çağırır. "site yapalım", "sayfa yapalım", "arayüz yapalım", "müşteri işi", "tasarlayalım", "sayfayı düzeltelim", "yayına alalım" dendiğinde kullan.
---

# Site kümesi

Müşteriye website yapma ve arayüz işleri. kullanıcı arada website yapıp satıyor — bu küme o iş için.

## Sıra ve skiller

| Aşama | Skill | Ne zaman sorulur |
|---|---|---|
| Görsel yön, renk, font kararı | `ui-ux-pro-max` | Sıfırdan başlıyorsak veya yön belirsizse |
| Sayfayı tasarlama, elden geçirme | `impeccable` | Ortada bir sayfa varsa veya yapılacaksa |
| Erişilebilirlik, responsive, bileşen | `frontend-ui-engineering` | Kod yazılacaksa |
| Yayın öncesi kontrol | `shipping-and-launch` | Teslim yaklaşınca |

Hepsini sırayla çalıştırma. İş hangisini gerektiriyorsa **onu sor**.

## Her sayfa işinin sonu: ekran görüntüsüyle bak

"Kod doğru" yetmez. Sayfa yazılınca veya değişince masaüstü (1280px) ve mobil (390px)
ekran görüntüsü alınır ve **açılıp bakılır**; bu adım onay sorulmadan yapılır, küme kuralı
değil kalite kapısıdır. 2026-09-10'da üç örnek sitede koddan görünmeyen üç kusur (fotoğraf
üstünde okunan yazı, gökyüzünde kaybolan nav, butonla çakışan rozet) yalnızca bununla
yakalandı.

Chrome bu makinede **flatpak** (`com.google.Chrome`); Playwright ve chrome-devtools MCP'leri onu
bulamaz, "Chrome yok" denmez. Komut ve tuzaklar (`--filesystem=host`, `/tmp`'ye yazamama,
WebGL için `--enable-unsafe-swiftshader`) `browser-testing-with-devtools` skill'inde; 3B
içermeyen sayfada yedek yol `firefox --headless --screenshot out.png --window-size=390,2400 <url>`.

## kullanıcıya özgü not

Bu küme müşteri işi için açılıyor, yani çıktı teslim edilecek. İki şey her seferinde sorulur:
kimin için yapılıyor ve ne zaman teslim edilecek. Cevaplar `.devir.md` dosyasına yazılır.

## Devir önerileri

- Tasarım oturdu, asıl kod yazılacak → **`kod`**
- Sayfa şişti, sadeleşmesi lazım → **`temizlik`**
- İki tasarım yönü arasında karar verilemiyor → **`karar`**

## Devir notu

Küme açılırken çalışılan klasörde `.devir.md` varsa **önce onu oku** — önceki kümenin ne
bulduğu, nerede bıraktığı orada yazar. Aynı şeyi kullanıcıya iki kez anlattırma.

Küme kapanırken `.devir.md` dosyasına üç satır bırak:

```
## <küme adı> — <tarih>
Ne yapıldı: <tek cümle>
Nerede kaldı: <tek cümle>
Sıradaki: <öneri>
```

## İki kesin kural

**1 · Küme içindeki skiller kendiliğinden çalışmaz.** Bir skill uygun göründüğünde önce sor:
*"<skill> uygun görünüyor, kullanayım mı?"* Onay gelmeden yükleme. Kümeyi onaylamak,
içindeki skillerin hepsini onaylamak değildir.

**2 · Küme değişimi kendiliğinden olmaz.** İş başka bir kümenin alanına girdiğinde dur ve sor:
*"<durum>. `<küme>` kümesine geçeyim mi?"* Onay gelmeden geçme.

Sebep ikisinde de aynı: kullanıcının kotası sınırlı ve zincirleme çalışan bir düzen, o tek cümle
söylerken bütçesini sessizce yer. Kontrol onda kalır.
