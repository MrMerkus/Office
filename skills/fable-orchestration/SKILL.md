---
name: fable-orchestration
description: "Delegation policy for the user's three-tier agent stack: the Claude Code main loop owns judgment, Antigravity/Gemini (agy) does cheap recon and mechanical work, Codex (gpt-5.6-luna) executes written specs. Claude sub-agents (the Agent tool) are DISABLED in this stack — delegation means agy or Codex only. Load whenever spawning sub-agents, delegating to agy or codex, or planning any fan-out. Türkçe tetikleyiciler: 'paslayalım', 'alt ajana ver', 'codex'e ver', 'gemini'ye ver', 'kim yapsın', 'bunu böl', 'paralel çalıştır'."
---

# Delege politikası — kullanıcının yığını

Yukarı akış sürümü (Avenox) "sınırsız Opus alt katmanı" olan bir düzene göre yazılmıştı.
kullanıcının düzeninde **Claude sınırsız değil, en kıt kaynak o.** Politika ona göre yeniden
kuruldu. 2026-09-10'da doğrulandı.

Temel yasa: **kıt katman ıvır zıvır iş yapmaz ve kendisi alt ajan olarak çoğaltılmaz.**
Onun tokenı yargı satın alır, hacim değil.

**"Alt ajan" bu yığında yalnızca iki şey demektir: `agy` ve Codex.** Claude alt ajanı
(`Agent` aracı) alt ajan sayılmaz — en pahalı katmanı kendi içinde kopyalamaktır ve
paslamanın bütün amacını ortadan kaldırır.

## Katmanlar

| Katman | Ne | Bütçe | Ne için |
|---|---|---|---|
| **Ana döngü** | Claude Code (Opus 5) | Aylık AI tavanı — **kıt** | Mimari, spec yazımı, karar, bütünleştirme, son senteze |
| **Ucuz alt katman** | Antigravity (`agy`) → Gemini 3.1 Pro / 3.8 Flash | **Aralık sonuna kadar ayrı abonelik** | Keşif, kod tabanı haritalama, araştırma, inceleme, doğrulama turu |
| **İcra katmanı** | Codex (`codex exec`, `gpt-5.6-luna`) | ChatGPT hesabı, ayrı kota | Spec'i yazılmış icra: uygulama şeritleri, göç, refactor, test yazımı |

Ara katman yok. Üç katman, o kadar. Katman sayısı arttıkça yönlendirme denetlenemez hale gelir.

## Sert kurallar

1. **Claude alt ajanı kapalıdır. `Agent` aracı bu yığında kullanılmaz.** Hiçbir model
   seçeneğiyle, hiçbir "sadece bu sefer" gerekçesiyle değil. İş paslanacaksa
   `antigravity-fleet` skill'i açılır ve şerit `agy`'ye ya da `codex-fleet` üzerinden
   Codex'e gider. Paslanacak kadar büyük değilse ana döngü işi kendi elleriyle yapar.
   Bu kural 2026-09-11'de kullanıcının açık talimatıyla kondu: o gün bir `agy` şeridi izin
   hatasıyla düşünce işi üç Claude alt ajanına dağıtmıştım, tepkisi **"alt ajan olarak
   antigravity ve codex alt ajanlarını kullan manasında dedim"** oldu.
2. **Ucuz iş önce `agy`'ye gider.** Keşif, tarama, "şu dosyalarda ne var", "bu kütüphane
   nasıl kullanılıyor" gibi işler Gemini aboneliğinden karşılanır — o bütçe Aralık sonuna
   kadar zaten ödenmiş durumda ve harcanmazsa kayboluyor.
3. **Ana döngü büyük resmi elinde tutar.** Mimari, sözleşmeye duyarlı tasarım, ince durum
   makineleri, bütünleştirme, çakışma çözümü, son sentez, yargı çağrısı — hepsi burada.
4. **kullanıcıya rapor eden taraf ana döngüdür.** Alt katmanın çıktısı doğrudan kullanıcıya
   dökülmez; süzülür, Türkçeleştirilir, doğrulanır.

## Delegeyi seçme

- **`agy` (Gemini) — bağlam toplamanın varsayılanı.** Keşif, kod tabanı haritalama,
  araştırma taraması, inceleme, doğrulama turu — kısacası brief'in gevşek olabildiği ve
  teslim edilenin *anlayış* olduğu iş. Belirsizlikle iyi başa çıkar: hedefi ver, araziyi
  kendi çıkarsın. Ayrıntı için `antigravity-fleet` skill'i.
- **Codex (`gpt-5.6-luna`, `high`) — icranın varsayılanı.** Takıntılı bir talimat
  uygulayıcısı: kıt katmana yakın yetenekli ama yaratıcı değil. Doğaçlama yapmaz, **icra
  eder.** Dikkatle yazılmış, ayrıntılı, açık bir spec ver; onu tavizsiz ve hassas biçimde
  öğütür. Kullanım: uygulama şeritleri, göçler, refactor'lar, tanımlı sözleşmeye karşı test
  yazımı. Ayrıntı için `codex-fleet` skill'i.
- **Claude alt ajanı — yok. Üçüncü bir seçenek değil.** Yargı ağırlıklı iş paslanmaz;
  ana döngünün kendi işidir.

Pratik kural: **bağlam toplama → `agy`; icra (ana döngü spec'i yazdıktan sonra) → Codex;
yargı / sentez / spec yazımı → ana döngünün kendisi.** Bir Codex şeridinin kalitesi
spec'inin kalitesiyle sınırlıdır — tokenı brief'e yatır, şeridi kendin yapmaya değil.

## Bir katman kapalıysa

Şeritler arıza yüzünden düşebilir: `agy` izin hatası verebilir, Codex kotası dolabilir.
Bu durumda doğru refleks **işi Claude alt ajanına çekmek değildir.**

1. Diğer ucuz katmanı dene: `agy` düştüyse Codex, Codex düştüyse `agy`.
2. İkisi de kapalıysa **dur ve kullanıcıya söyle**: hangi katmanın neden kapalı olduğunu,
   elinde ne kaldığını ve önündeki seçenekleri yaz. Devam kararı onun.
3. İş küçükse ana döngü kendi yapabilir, ama bunu **söyleyerek** yapar — sessizce
   pahalı katmana geçmek yasak.

## Zorluk ekseni

Yönlendirme ekseni **zorluk**, sadece keşif-mi-icra-mı değil.

- **Basit, sınırları belli iş → `agy`.** Hafif icra da buna dahil: şablonlu düzenlemeler,
  mevcut bir örüntünün kopyası, var olan bir hattın üstünden giden işler.
- **Zor veya hassasiyet isteyen iş → Codex `high`/`xhigh`, eksiksiz spec ile.** Doğruluğa
  duyarlı yollar, güvenlik kritik değişiklikler, en geniş yüzeyler.
- **Kapı bekçisi / inceleme şeritleri en yüksek Codex presetinde kalır**, incelediği şey
  ne kadar küçük olursa olsun.

Filo şeridi dağıtırken adaptörü şerit başına spec'e yaz; böylece fırlatma mekanik olur,
spawn anında yönlendirme kararı verilmez.

## Doğrulama borcu

Alt katmanın "bitti" demesi bir **iddiadır, kanıt değil.** Ana döngü kabul kontrolünü
kendisi çalıştırır (hedefli test / typecheck / dosyayı okuma) — bütünleştirmeden önce.
Bu, kullanıcının `gptpro-handoff`'tan da bildiği kural: dış modelin her bulgusu canlı kodda
doğrulanır.

## İstisnalar

- kullanıcı kapsamlı bir iş için model adını açıkça söylerse, **o iş için** ona uy, sonra
  politikaya dön.
- kullanıcı oturum başına her şeyi ezebilir; aksi söylenmedikçe bu politika geçerlidir.
- **Claude alt ajanı yasağının istisnası yoktur.** Yukarıdaki iki madde bu kuralı açmaz;
  yalnızca kullanıcının kendisi doğrudan "Claude alt ajanı çalıştır" derse açılır.
