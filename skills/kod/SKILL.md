---
name: kod
description: Yazılım yazma kümesi. Gerçek bir projede kod yazma, hata çözme, sürüm yönetimi işlerini kapsar; içindeki skilleri tek tek onay alarak çağırır. "kod yazalım", "bunu kodlayalım", "yazılım işi", "hata var çözelim", "commit atalım", "test yazalım", "projeye başlayalım" dendiğinde kullan.
---

# Kod kümesi

Gerçek bir yazılım işi. kullanıcı yazılımı çıraklık yöntemiyle öğreniyor — bu küme hem işi bitirmeli
hem öğretmeli.

## Sıra ve skiller

| Aşama | Skill | Ne zaman sorulur |
|---|---|---|
| Ne yapılacağını yazmak | `spec-driven-development` | Yeni proje veya büyük değişiklikse |
| Testle doğrulamak | `test-driven-development` | Mantık yazılıyorsa veya hata düzeltiliyorsa |
| Parça parça teslim | `incremental-implementation` | İş birden fazla dosyaya dokunuyorsa |
| Hata kökünü bulmak | `debugging-and-error-recovery` | Bir şey çalışmıyorsa |
| Commit, dal, sürüm | `git-workflow-and-versioning` | Değişiklik kaydedilecekse |

**İki satırlık bir düzeltme için bu akışın tamamını başlatma.** Küçük iş küçük kalır.

## kullanıcıya özgü not

Öğrenme hedefi var. Kod yazıldıktan sonra *neden öyle yazıldığı* tek cümleyle söylenir — ama
ders anlatımına dönüşmez. Sorarsa açılır.

## Devir önerileri

- Kod çalışıyor ama fazlalık birikti → **`temizlik`**
- Nasıl yapılacağı bilinmiyor, kaynak lazım → **`arastirma`**
- İki yaklaşım arasında sıkışıldı → **`karar`**
- Kod bitti, arayüz tarafı kaldı → **`site`**

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
