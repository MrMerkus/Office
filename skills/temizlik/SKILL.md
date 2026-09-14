---
name: temizlik
description: Sadeleştirme kümesi. Biriken karmaşayı atma, gereksiz kodu bulma, fazlalık inceleme işlerini kapsar; içindeki skilleri tek tek onay alarak çağırır. "sadeleştirelim", "temizleyelim", "fazlalık var mı", "ne silebiliriz", "karışmış", "şişmiş", "gereksizleri atalım" dendiğinde kullan.
---

# Temizlik kümesi

Biriken karmaşayı atmak. kullanıcı fazla kurmaktan hoşlanmıyor — bu küme o eğilimin panzehiri.

## Sıra ve skiller

| İhtiyaç | Skill | Ne zaman sorulur |
|---|---|---|
| Yazılan koddaki fazlalık | `ponytail-review` | Yeni bir değişiklik incelenecekse |
| Tüm depodaki fazlalık | `ponytail-audit` | Genel bir tarama isteniyorsa |
| Okunurluk için yeniden düzenleme | `code-simplification` | Kod çalışıyor ama karışıksa |
| Ertelenen kestirmeler | `ponytail-debt` | "Neyi sonraya bırakmıştık" soruluyorsa |

## Değişmez kural

**Silme kararı kullanıcınındır.** Bu küme neyin gereksiz olduğunu gösterir, kendiliğinden silmez.
Sınıflandırma yapılır, gerekçe yazılır, karar ona bırakılır.

## Devir önerileri

- Sadeleşti, değişiklik kaydedilecek → **`kod`**
- Sayfa sadeleşti, yayına gidiyor → **`site`**

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
