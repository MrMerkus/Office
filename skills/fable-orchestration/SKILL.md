---
name: fable-orchestration
description: "Delegation policy for kullanıcı's agent stack: the Claude Code main loop owns judgment, Codex (gpt-5.6-luna) does recon and executes written specs through the ~/ofis/ajans lane protocol (emir → worktree → durum/teslim → makbuz). agy was dropped (SOZLESME Karar 8). Claude sub-agents (the Agent tool) are DISABLED in this stack — delegation means Codex only. Load whenever spawning sub-agents, delegating to codex, opening an ajans lane, or planning any fan-out. Türkçe tetikleyiciler: 'paslayalım', 'alt ajana ver', 'codex'e ver', 'şerit aç', 'kim yapsın', 'bunu böl', 'paralel çalıştır'."
---

# Delege politikası — kullanıcının yığını

Yukarı akış sürümü (Avenox) "sınırsız Opus alt katmanı" olan bir düzene göre yazılmıştı.
kullanıcının düzeninde **Claude sınırsız değil, en kıt kaynak o.** Politika ona göre yeniden
kuruldu. 2026-09-10'da doğrulandı; 2026-09-24'te `agy` çıkarıldı ve ajans şerit protokolü
eklendi (SOZLESME Karar 8 ve 9).

Temel yasa: **kıt katman ıvır zıvır iş yapmaz ve kendisi alt ajan olarak çoğaltılmaz.**
Onun tokenı yargı satın alır, hacim değil.

**"Alt ajan" bu yığında yalnızca Codex demektir.** Claude alt ajanı (`Agent` aracı) alt ajan
sayılmaz — en pahalı katmanı kendi içinde kopyalamaktır ve paslamanın bütün amacını ortadan
kaldırır. `agy` (Antigravity/Gemini) 2026-09-23'te bırakıldı; `antigravity-fleet` skill'i
yalnız kayıt için duruyor.

## Katmanlar

| Katman | Ne | Bütçe | Ne için |
|---|---|---|---|
| **Ana döngü** | Claude Code | Aylık AI tavanı — **kıt** | Mimari, spec (emir) yazımı, karar, bütünleştirme, makbuz, son sentez |
| **Alt katman** | Codex (`codex exec`, `gpt-5.6-luna`) | ChatGPT hesabı, ayrı kota | Keşif (read-only) ve spec'i yazılmış icra: uygulama, göç, refactor, test yazımı |
| **Görsel rotası** | ChatGPT web (`gorsel-handoff`) | kullanıcının ChatGPT Go aboneliği | Görsel üretimi; kullanıcı yapıştırır, ana döngü denetler |

Ara katman yok (görsel rotası bir ajan değil, kullanıcının elinden geçen bir döngü). Katman
sayısı arttıkça yönlendirme denetlenemez hale gelir.

**Codex aboneliği henüz açık değil** (motor inşasında, PLAN adım 5'te açılır). Açılana kadar
Codex adımlarını ana döngü yapar ve bunu **söyleyerek** yapar; kabul ölçütü değişmez.

## Sert kurallar

1. **Claude alt ajanı kapalıdır. `Agent` aracı bu yığında kullanılmaz.** Hiçbir model
   seçeneğiyle, hiçbir "sadece bu sefer" gerekçesiyle değil. İş paslanacaksa ajans şeridi
   açılır ve Codex `codex-fleet` üzerinden çalışır. Paslanacak kadar büyük değilse ana döngü
   işi kendi elleriyle yapar. Bu kural 2026-09-11'de kullanıcının açık talimatıyla kondu: o gün
   bir şerit izin hatasıyla düşünce işi üç Claude alt ajanına dağıtmıştım, tepkisi **"alt
   ajan olarak antigravity ve codex alt ajanlarını kullan manasında dedim"** oldu.
2. **Her Codex işi şeritten geçer** (aşağıdaki protokol). Şeritsiz, emirsiz `codex exec`
   yalnız tek seferlik salt-okuma sorusu için kabul edilir.
3. **Ana döngü büyük resmi elinde tutar.** Mimari, sözleşmeye duyarlı tasarım, ince durum
   makineleri, bütünleştirme, çakışma çözümü, son sentez, yargı çağrısı — hepsi burada.
4. **kullanıcıya rapor eden taraf ana döngüdür.** Alt katmanın çıktısı doğrudan kullanıcıya
   dökülmez; süzülür, Türkçeleştirilir, doğrulanır.

## Ajans şerit protokolü (SOZLESME Karar 9, PLAN "Şerit protokolü")

Alt ajanlar `~/ofis/ajans/` karargâhından emirle çalışır. **Ajans yönetim yeridir, iş yeri
değil:** emir, durum, teslim ve makbuz orada; kod ofisteki projenin git worktree'sinde yazılır.
Yarım şerit asıl projeyi bozamaz. Düzenin ayrıntısı `~/ofis/ajans/CLAUDE.md`'de.

1. **Emir.** Ana döngü `ajans/seritler/<YYYY-AA-GG>-<ad>/emir.md` yazar: ne, hangi proje,
   hangi worktree, kabul ölçütü, dokunabileceği yollar, hangi rol. `pano.md`'ye satır ekler.
2. **Rol.** Emir `ajans/kadro/<rol>.md`'den bir rolü brief olarak verir: kaşif (yalnız okur),
   kodcu (yalnız kendi worktree'si), denetçi (okur + test), tasarımcı (kendi worktree'si).
   Her rolün okuma/yazma/komut yetkisi dosyasında yazılıdır.
3. **Worktree.** `ajans/serit-ac.sh` worktree açar ve Codex'i orada çalıştırır. Tek şerit,
   tek iş. Codex oturumları `BEYIN_INVOKED_BY=codex-serit` ile işaretlenir; oturum sayılmaz,
   hafıza hook'ları bunları ana oturum gibi işlemez.
4. **Durum / teslim.** Codex `durum.md` (nerede kaldı, takıldığı yer) ve `teslim.md` (ne
   yaptı, hangi dosyalar, hangi komutla doğrulanır) yazar. **Beyne yazmaz, `🔐 kasa/`yı okumaz.**
5. **Makbuz.** Ana döngü kendi ölçümüyle `makbuz.md` keser (`kabul-kontrolu`). Makbuzsuz
   şerit açık sayılır. Kabul edilen değişiklik asıl dala alınır, klasör `arsiv/`e taşınır.

**Kapı-0 önkoşulu:** ilk gerçek şeritten önce en küçük Kapı kodda olmalı — dönüşte değişen
yollar rolün beyaz listesiyle karşılaştırılır, kasa yolu reddedilir, ihlalde makbuz kırmızı.
Kadro dosyasındaki yetki düzyazısı tek başına kapı sayılmaz. Kapı Codex'i kesemiyorsa ilk
şeritler kullanıcının elle onayı ve Codex'in sandbox yazma sınırıyla açılır (PLAN durma kuralı).

## Delegeyi seçme

- **Codex kaşif rolü (`--sandbox read-only`) — bağlam toplamanın varsayılanı.** Keşif, kod
  tabanı haritalama, "şu dosyalarda ne var", inceleme turu. Teslim edilen *anlayış*tır,
  değişiklik değil. Küçük keşfi ana döngü kendi `grep`/`ls`'iyle yapar; şerit açmaz.
- **Codex kodcu / tasarımcı rolü (`gpt-5.6-luna`, `high`) — icranın varsayılanı.** Takıntılı
  bir talimat uygulayıcısı: kıt katmana yakın yetenekli ama yaratıcı değil. Doğaçlama yapmaz,
  **icra eder.** Dikkatle yazılmış, ayrıntılı, açık bir emir ver; onu tavizsiz ve hassas
  biçimde öğütür. Ayrıntı için `codex-fleet` skill'i.
- **ChatGPT web (`gorsel-handoff` skill'i) — görsel üretiminin varsayılanı.** kullanıcının
  ChatGPT Go aboneliği; ne Claude ne Codex kotasından yer. Ana döngü promptu ve yükleme
  paketini hazırlar, kullanıcı web arayüzüne yapıştırıp sonucu klasöre indirir, ana döngü
  kontrol listesiyle denetleyip onay ya da düzeltme promptu verir. Karakter kartı, sahne,
  simge konsepti, afiş — **her görsel iş önce buraya düşünülür.** Sınırı: PNG verir, SVG
  vermez; vektör gerekiyorsa ChatGPT konsepti üretir, SVG çizimi Codex tasarımcı şeridine
  gider. Codex `gpt-image-2` bunun yedeğidir, varsayılanı değil. Bu satır 2026-09-15'te
  kullanıcının talimatıyla eklendi: simge işini doğrudan Codex'e verdim, kota doldu —
  `gorsel-handoff` hiç akla gelmedi. kullanıcı: *"bunu da buna dahil et yoksa sürekli
  unutacaksın."*
- **Claude alt ajanı — yok. Üçüncü bir seçenek değil.** Yargı ağırlıklı iş paslanmaz;
  ana döngünün kendi işidir.

Pratik kural: **bağlam toplama → Codex kaşif (ya da küçükse ana döngü); icra (ana döngü emri
yazdıktan sonra) → Codex kodcu/tasarımcı; görsel → `gorsel-handoff`; yargı / sentez / emir
yazımı / makbuz → ana döngünün kendisi.** Bir Codex şeridinin kalitesi emrinin kalitesiyle
sınırlıdır — tokenı emre yatır, şeridi kendin yapmaya değil.

## Brief'teki genel kural her dosyaya uygulanır

Delege brief'teki kuralı harfiyen ve **dokunduğu bütün dosyalara** uygular. 2026-09-14'te ofis
şablonu spec'ine vault'un "her markdown dosyası ~500 kelimenin altında" kuralı yazıldı; Gemini
Flash kopyaladığı skill'leri de kırptı (`codex-fleet` 5513→403, `antigravity-fleet` 1105→435
kelime). Söz dizimi temiz geçtiği için ancak boyut karşılaştırmasıyla görüldü.

- Kopyalama / genelleştirme şeridinde brief açıkça **"içeriği kısaltma, yalnızca şu ifadeleri
  değiştir"** der; genel yazım kuralları yalnızca delegenin **yeni yazdığı** dosyalar için verilir.
- Kabul kontrolüne **kaynakla kelime/bayt karşılaştırması** eklenir (`wc -w` önce/sonra).
- Metin dönüştürme deterministikse (ifade değiştirme, iz silme) modele değil **script'e**
  yaptırılır; model yalnızca script'in yakalayamadığını işaretler.

## Brief'e yalnızca kullanıcının söylediği bağlam girer (0021)

Delege konuşmayı görmez. Brief'te ne yazıyorsa onu **gerçek** sanar ve bütün çıktıyı ona göre
kurar; yanlış bir varsayım tek satırdan girip raporun tamamını bozar.

2026-09-14'te kullanıcı "2 düzgün salon var" dedi. Bundan "orta büyüklükte şehir" çıkarıp brief'e
yazdım; şerit elemeyi "salon nadir" varsayımıyla yaptı. kullanıcı İstanbul'daydı — yani eleme
baştan yanlış eksende yapılmıştı.

- Brief'e giren bağlam **alıntıdır**, çıkarım değil. Kullanıcının kurduğu cümleye sadık kal.
- Bir çıkarım gerçekten gerekiyorsa brief'te **varsayım olarak işaretlenir** ("varsayım: şehir
  büyük; yanlışsa raporun başında söyle"), böylece şerit onu sorgulayabilir.
- Emin değilsen brief'i daraltmak yerine **kullanıcıya tek soru sor**; yanlış varsayımla dönen bir
  şeridi yeniden çalıştırmak, sorulacak sorudan pahalıdır.

## Aynı depoya iki taraf dokunmaz, kritik parça önce çalışır (0005, 0012)

- **Geçmişi yeniden yazan işte (rebase, force-push, filter-branch) o depoya tek taraf dokunur.**
  Paralel oturum aynı depoda geçmişi yeniden yazınca yayın geri düştü. İkinci şerit açılacaksa
  ayrı worktree'de çalışır, birleştirme ana döngüde ff-merge ile yapılır.
- **Kota işin ortasında dolabilir.** Dört iş birden kesildiğinde hiçbiri bitmemiş olur. Çok
  parçalı bir filoda **kritik parça ilk sıraya alınır**; kesinti olursa elde en azından o
  bulunur. Kotanın ne zaman yenileneceği kullanıcıya söylenir, tahmin edilmez.

## Codex kapalıysa

Şeritler arıza yüzünden düşebilir: izin hatası, dolan kota, abonelik yok. Bu durumda doğru
refleks **işi Claude alt ajanına çekmek değildir.**

1. **Dur ve kullanıcıya söyle**: Codex neden kapalı, elinde ne kaldı, önündeki seçenekler neler.
   Devam kararı onun.
2. İş küçükse ya da abonelik henüz açılmamışsa ana döngü kendi yapabilir, ama bunu
   **söyleyerek** yapar — sessizce pahalı katmana geçmek yasak.
3. Yarım kalan şerit sıfırdan başlamaz; `durum.md` ve logdaki somut birikim yeni emre devredilir.

## Zorluk ekseni

Yönlendirme ekseni **zorluk**, sadece keşif-mi-icra-mı değil.

- **Basit, sınırları belli iş → Codex `medium`.** Şablonlu düzenlemeler, mevcut bir örüntünün
  kopyası, var olan bir hattın üstünden giden işler.
- **Zor veya hassasiyet isteyen iş → Codex `high`/`xhigh`, eksiksiz emirle.** Doğruluğa
  duyarlı yollar, güvenlik kritik değişiklikler, en geniş yüzeyler.
- **Denetçi / inceleme şeritleri en yüksek Codex presetinde kalır**, incelediği şey
  ne kadar küçük olursa olsun.

Filo şeridi dağıtırken efor ve rolü şerit başına emre yaz; böylece fırlatma mekanik olur,
spawn anında yönlendirme kararı verilmez.

## Doğrulama borcu

Alt katmanın "bitti" demesi bir **iddiadır, kanıt değil.** Ana döngü kabul kontrolünü
kendisi çalıştırır (hedefli test / typecheck / dosyayı okuma) ve makbuzu ancak ondan sonra
keser — bütünleştirmeden önce. Bu, kullanıcının `gptpro-handoff`'tan da bildiği kural: dış
modelin her bulgusu canlı kodda doğrulanır.

## İstisnalar

- kullanıcı kapsamlı bir iş için model adını açıkça söylerse, **o iş için** ona uy, sonra
  politikaya dön.
- kullanıcı oturum başına her şeyi ezebilir; aksi söylenmedikçe bu politika geçerlidir.
- **Claude alt ajanı yasağının istisnası yoktur.** Yukarıdaki iki madde bu kuralı açmaz;
  yalnızca kullanıcının kendisi doğrudan "Claude alt ajanı çalıştır" derse **o oturum boyunca**
  açılır.
