---
name: basla
description: Küme seçimi — hangi iş kümesiyle başlanacağını belirler. Ne yapmak istediğini sorup doğru kümeye yönlendirir; küme kendisi çalışmaz, yalnızca yönlendirir. "nereden başlayalım", "hangi kümeyi kullanalım", "ne yapmalıyız", "başlayalım", "hangi skilleri kullanacağız", "elimizde ne var" dendiğinde veya iş tanımı belirsizken kullan.
---

# Başla — küme seçimi

Bu skill iş yapmaz. Doğru kümeyi bulur ve **onay alıp** ona devreder.

## Kümeler

| Küme | Ne zaman | İçinde ne var |
|---|---|---|
| **`site`** | Müşteriye website, arayüz, sayfa yapılırken | impeccable · ui-ux-pro-max · frontend-ui-engineering · shipping-and-launch |
| **`kod`** | Gerçek bir yazılım işi yazılırken | spec-driven · test-driven · incremental · git-workflow · debugging |
| **`arastirma`** | Video, karar veya öğrenme için bilgi toplanırken | last30days · watch · source-driven |
| **`temizlik`** | Biriken karmaşa atılırken | ponytail ailesi · code-simplification |
| **`karar`** | Tıkanıldığında, seçim yapılamadığında | council · idea-refine · interview-me · doubt-driven |

## Nasıl seçilir

kullanıcının cümlesi hangi kümeye düşüyorsa onu öner — **tek cümlelik soruyla**:

> "Bu iş `<küme>` kümesine giriyor. Açayım mı?"

Belirsizse tahmin etme, sor: *"Ne yapmak istiyorsun — sayfa mı, kod mu, araştırma mı?"*

Hiçbir kümeye girmiyorsa küme açma. Bazı işler tek skill ister, bazıları hiç skill istemez.
Küme açmamak da bir cevaptır.

## Kapsam dışı kalanlar

`security-and-hardening`, `performance-optimization`, `observability-and-instrumentation`,
`api-and-interface-design`, `ci-cd-and-automation`, `constraint-driven-development`,
`deprecation-and-migration`, `planning-and-task-breakdown` — bunlar nadir kullanılıyor ve
kümeye girmedi. İhtiyaç doğduğunda tek tek çağrılır.

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
