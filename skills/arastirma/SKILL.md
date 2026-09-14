---
name: arastirma
description: Bilgi toplama kümesi. Video, karar veya öğrenme için kaynak toplama, güncel durumu öğrenme, video izleme işlerini kapsar; içindeki skilleri tek tek onay alarak çağırır. "araştıralım", "bilgi toplayalım", "ne konuşuluyor", "güncel durum ne", "şu videoya bakalım", "kaynak bulalım", "bunu öğrenelim" dendiğinde kullan.
---

# Araştırma kümesi

Bilgi toplama. kullanıcı video çekiyor, karar veriyor ve öğreniyor — üçü de kaynak istiyor.

## Sıra ve skiller

| İhtiyaç | Skill | Ne zaman sorulur |
|---|---|---|
| İnsanlar bu konuda ne diyor | `last30days` | Güncel algı, tartışma veya trend soruluyorsa |
| Bir videoda ne anlatılıyor | `watch` | Elde bir video bağlantısı varsa |
| Resmî doküman ne diyor | `source-driven-development` | Teknik doğruluk gerekiyorsa |

## Değişmez kural

**İngilizce kaynak kullanıcıya çevrilerek sunulur.** Ham İngilizce metin aktarılmaz; bulgular
Türkçe özetlenir, gerekirse alıntı çevrilir.

## Araştırma bitiş ölçütü

Araştırma kendi kendine bitmez, bitirilir. Toplanan bilgi bir karara veya çıktıya bağlanmıyorsa
durulur. *"Bir şey daha bakayım"* araştırmanın değil, ertelemenin cümlesidir.

## Devir önerileri

- Bilgi toplandı, seçim yapılacak → **`karar`**
- Öğrenilen şey uygulanacak → **`kod`**

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
