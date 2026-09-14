# Türkçe Tetikleyiciler

Skill'lerin `description` alanına eklenen Türkçe tetikleyici ifadelerin kaynak kaydıdır. Dış repolardan güncellenen skill'lerin tetikleyicilerini korumak için kullanılır.

## Kullanım

```bash
python3 ${OFIS:-$HOME/ofis}/araclar/turkce-tetikleyiciler.py
```

Betik her skill'in `description` alanının sonuna ilgili ifadeleri ekler:
`Türkçe tetikleyiciler: "ifade1", "ifade2".`

---

## Yama Tablosu

<!-- FORMAT: skill-adı :: tetikleyici1 | tetikleyici2 | tetikleyici3 -->

```yama
api-and-interface-design :: api tasarla | arayüz sözleşmesi | endpoint ekle | modüller arası sınır
browser-testing-with-devtools :: tarayıcıda test et | sayfayı aç bak | konsolda hata var mı | ekran görüntüsü al
ci-cd-and-automation :: otomatikleştir | pipeline kur | derleme hattı | her push'ta çalışsın
code-simplification :: sadeleştir | basitleştir | bunu temizle | daha okunur yap | karışık olmuş
constraint-driven-development :: kalite çıtası | kural koy | standart belirle | testleri atlama
council :: konsey | konseyi çağır | tartışalım | fikir alalım | ne düşünüyorlar
debugging-and-error-recovery :: hata var | çalışmıyor | bozuldu | neden patladı | bu hatayı çöz | niye böyle oluyor
deprecation-and-migration :: taşı | eskisini kaldır | göç ettir | sürüm yükselt | bunu emekliye ayır
doubt-driven-development :: emin misin | kontrol et | doğrula | bir daha bak | acaba doğru mu
frontend-ui-engineering :: arayüz yap | sayfa yap | buton ekle | form yap | responsive olsun
git-workflow-and-versioning :: commit at | dal aç | sürüm çıkar | pull request | çakışma çöz
idea-refine :: fikri geliştir | bu fikri düşün | fikri keskinleştir | olur mu bu
impeccable :: tasarla | tasarımı düzelt | güzelleştir | sayfayı elden geçir | çirkin durmuş | daha iyi görünsün
incremental-implementation :: parça parça yap | adım adım ilerle | küçük küçük | tek seferde yapma
interview-me :: mülakat yap | bana sor | ne istediğimi çıkar | soru sor bana
last30days :: son 30 gün | ne konuşuluyor | insanlar ne diyor | güncel durum | gündemde ne var
observability-and-instrumentation :: log ekle | izleme koy | ne olduğunu göremiyorum | metrik ekle
performance-optimization :: yavaş | hızlandır | performans sorunu | neden bu kadar sürüyor
planning-and-task-breakdown :: planla | adımlara ayır | işi böl | nereden başlayalım | sıraya koy
ponytail :: en basit çözüm | sade tut | abartma | gereksiz şey yapma | fazla kurma | kısa yoldan
ponytail-audit :: ne silebiliriz | fazlalık var mı | şişmiş mi | gereksizleri bul
ponytail-debt :: neyi erteledik | kestirmeleri göster | borç listesi
ponytail-gain :: ne kazandırdı | ölçüyü göster | kâr hanesi
ponytail-help :: ponytail nasıl | hangi komutlar var
ponytail-review :: fazlalık incelemesi | gereksiz kod var mı | sadeleşir mi
security-and-hardening :: güvenlik | güvenli mi | açık var mı | sızıntı riski | anahtar sızmış mı
shipping-and-launch :: yayınla | canlıya al | dağıt | çıkışa hazır mı | son kontrol
source-driven-development :: dokümana bak | resmi kaynak | kaynağı doğrula | belgede ne yazıyor
spec-driven-development :: şartname yaz | önce planla | ne yapacağımızı yaz | gereksinimleri çıkar
test-driven-development :: test yaz | önce test | testle doğrula | bu çalışıyor mu kanıtla
ui-ux-pro-max :: renk paleti | font seç | tasarım sistemi | arayüz standardı | hangi renkler
using-agent-skills :: hangi skill | skill var mı | ne kullanmalıyız | elimizde ne var
watch :: videoyu izle | şu videoya bak | videoda ne anlatıyor | transkript çıkar
```
