---
name: karar
description: Karar verme kümesi. Tıkanıldığında, seçenekler arasında sıkışıldığında, bir fikrin sağlamlığı test edileceğinde kullanılır; içindeki skilleri tek tek onay alarak çağırır. "karar veremiyorum", "hangisini seçelim", "tıkandım", "konseyi çağır", "tartışalım", "bu fikir olur mu", "emin değilim", "ne yapmalıyım" dendiğinde kullan.
---

# Karar kümesi

Tıkanma anı. kullanıcı bir seçim yapamıyor ya da bir fikrin sağlam olup olmadığını bilmiyor.

## Sıra ve skiller

| Durum | Skill | Ne zaman sorulur |
|---|---|---|
| Çok yönlü, ağır bir karar | `council` | Karar geri dönülmezse veya çok değişken varsa |
| Fikir henüz bulanık | `idea-refine` | Ortada karar değil, ham fikir varsa |
| Ne istendiği net değil | `interview-me` | kullanıcının kendi isteği bile belirsizse |
| Verilen karar sağlam mı | `doubt-driven-development` | Karar verildi ama emin olunamıyorsa |

## Konsey hakkında iki uyarı

**Konsey pahalıdır.** Her üye ayrı bir bağlam yükler. Dört üye küçük bir kararı çözmez, sadece
kotayı yer. Üye sayısı kararın ağırlığına göre seçilir ve kullanıcıya söylenir.

**Konseyin çıktısı karar değildir.** Konsey girdi üretir; kararı kullanıcı verir. Sonuç vault'a
"karar verildi" diye yazılmaz — *"analiz şunu buldu, tavsiye şu yönde, karar kullanıcıda"* diye
yazılır.

## Devir önerileri

- Karar verildi, uygulanacak → **`kod`** veya **`site`**
- Karar için bilgi eksik → **`arastirma`**

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
