---
name: antigravity-fleet
description: "DEPRECATED — agy bırakıldı (SOZLESME Karar 8, 2026-09-23); tetiklenmez. Keşif ve icra Codex'te (codex-fleet), delege politikası fable-orchestration'da."
---

# Antigravity Fleet — ucuz katman koşucusu

> **DEPRECATED (2026-09-24).** `agy` bırakıldı (SOZLESME Karar 8, 2026-09-23). Bu dosya
> yalnız kayıt için duruyor; şerit açmak için kullanılmaz. Katmandan bağımsız dersler
> `codex-fleet` SKILL.md'deki "Dersler" bölümüne taşındı.

`agy`, Google Antigravity'nin CLI'ı. kullanıcının yığınında **ucuz alt katman**: Gemini
aboneliği Aralık sonuna kadar ayrı bir bütçeden ödenmiş durumda, harcanmazsa kayboluyor.
Buradan geçen her iş Claude ve Codex kotasından **düşmez**.

Katman politikası `fable-orchestration` skill'inde. Bu dosya o politikanın `agy` ayağının
nasıl çalıştırılacağı.

## Bu bir icra skill'i, yorum skill'i değil

Çağrıldığında Bash aracıyla **gerçekten `agy` çalıştırırsın.** kullanıcının kendi eliyle
koşacağı komut yazmazsın. 10 saniyeden uzun sürecek her iş `run_in_background: true`
ile arka plana gider; harness bitince haber verir.

## Doğrulanmış gerçekler (2026-09-10, bu makinede ölçüldü)

- Sürüm: `agy` **1.1.22**, yolu `~/.local/bin/agy`.
- **`-p` bayrağı bitişik yazılır: `-p='prompt'`.** Ayrı yazılırsa `agy` bir sonraki kelimeyi
  prompt sanır ve gerçek promptu **sessizce yutar**. Hata mesajı:
  *"-p took \"--model\" as its prompt"*. Bu en kolay düşülen tuzak.
- Ölçülen süreler: tek cümlelik yanıt ~13 sn, dosya okuyup rapor eden iş ~42 sn.
- **Print modu izin İSTER ve headless'ta otomatik reddeder.** (2026-09-10'da düzeltildi;
  buradaki eski madde "izin sormaz" diyordu, yanlıştı.) Araç izni olmayan şerit sessizce
  yarıda kalır: model "şimdi dosyayı yazıyorum" der ve çıkar, çıkış kodu 0'dır, log kısacıktır.
  Hata satırı `jetski: no output produced — a tool required the "<araç>" permission`.
  İzinler `~/.gemini/antigravity-cli/settings.json` içinde `permissions.allow` listesinde
  durur: `read_url(*)` web erişimi, `write_file(*)` / `edit_file(*)` / `create_file(*)`
  dosya yazma, `command(*)` kabuk. kullanıcı bu izinleri 2026-09-10'da açtı.
- **Yazma izni açık olduğu için fren yok.** Kapsamı `cd` ve `--add-dir` ile daraltmak, ve
  yazmasını istemediğin şeridin brief'ine "READ ONLY" yazmak senin işin.
- **`agy` kendi settings.json'ını yeniden yazabiliyor**; elle eklenen kurallar
  sadeleşebilir (`read_url` + `read_url(*)` → tek `read_url(*)`). Şerit sessizce yarıda
  kalıyorsa önce bu dosyaya bak.
- **Dosya yazacak şeritte `--mode accept-edits` kullan.**
- **`--print-timeout` varsayılanı 5 dakika ve uzun işlerde yetmiyor.** Aşınca
  `print timeout after 5m0s with turn in progress` yazıp yarıda keser. Site yazımı gibi
  uzun işlerde `--print-timeout 25m` ver, dıştaki `timeout`'u ondan büyük tut.
- 3 paralel şerit sorunsuz koştu, çakışma yok. Süreç başına ~220 MB RSS: `agy` ince bir
  istemci, ağır iş sunucu tarafında. RAM burada darboğaz değil.
- Modeller (`agy models`, 2026-09-12'de doğrulandı): `gemini-3.8-flash-high` / `-medium` /
  `-low`, `gemini-3.7-flash-high` / `-medium` / `-low`, `gemini-3.6-flash-high` /
  `-medium` / `-low`, `gemini-3.1-pro-high` / `-low`, `claude-sonnet-4-6`,
  `claude-opus-4-6-thinking`, `gpt-oss-120b-medium`.

## Şerit açmadan önce kotaya bak

`codexbar usage --provider antigravity` (CodexBar CLI ≥ 0.60.2) iki havuzu ayrı gösterir:
**Gemini** ve **Claude/GPT** (Opus 4.6 ve Sonnet 4.6 bu havuzdan yer), her biri için 5 saatlik
ve haftalık kalan yüzde. Kota dolu modelde şerit çıkış kodu 0 ile sessizce düşer; bu yüzden
Claude/GPT havuzu %0 ise sıraya doğrudan Gemini'den başlanır. (2026-09-14: eski CodexBar
CSRF anahtarı yüzünden okuyamıyordu, 0.60.2 düzeltti.)

## Gemini CLI bu aboneliği kullanamaz

2026-09-14'te denendi: Gemini CLI 0.59.0'da "Sign in with Google" bireysel hesaplar için
kapalı (*"This client is no longer supported for Gemini Code Assist for individuals… migrate to
the Antigravity suite"*). Gemini aboneliği yalnızca Antigravity (IDE + `agy`) üzerinden
kullanılır. Gemini CLI ancak API anahtarı (dar ücretsiz limit, sonra token başına ücret) veya
Vertex AI (ücretli) ile çalışır; bu yüzden ucuz katman ve toplu alt ajan işi için alternatif
değildir.

## Varsayılan model sırası

kullanıcı bu sırayı 2026-09-19'da yeniden koydu (önceki sıra 2026-09-12, Opus başta).
**Şerit açarken listenin başından başlanır, başarısız olan veya kotası dolan modelde bir
alt sıraya inilir.**

| Sıra | Model kimliği | Ne için |
|---|---|---|
| 1 | `claude-sonnet-4-6` | Varsayılan, araştırma dahil her şerit. |
| 2 | `claude-opus-4-6-thinking` | Sonnet düştüğünde ya da kotası bittiğinde. |
| 3 | `gemini-3.8-flash-high` | Claude/GPT havuzu boşsa; toplu, mekanik taramalar. |
| 4 | `gemini-3.7-flash-high` | Üstteki üçü düştüğünde. |
| 5+ | Gerisi serbest | `gemini-3.6-flash-*`, `gpt-oss-120b-medium` — duruma göre seçilir. |

**Neden Sonnet başta (2026-09-19, Minecraft mod araştırması):** aynı araştırmada 4 Gemini
Flash şeridi uydurma bir mod ("Techno-Magic World"), başka modlara çıkan mcmod.cn
adresleri, şişik indirme sayıları ve yanlış sürümler üretti; Sonnet (Claude Code alt
ajanı olarak, ~100K token) uydurmasız döndü, iki iddiası elle doğrulandı. kullanıcı: *"hem agy
limitleri daha iyi gider hem de gemini'nin boklukları ile yorulmayız."* Sonnet ve Opus
`agy`'de aynı **Claude/GPT havuzundan** yer; o havuz haftalık dolarsa sıra Gemini'ye iner.
Gemini şeridinin çıktısı kararı taşıyorsa örneklem doğrulaması iki satırla sınırlı kalmaz.

**`gemini-3.1-pro-*` kullanılmaz** (kullanıcının kararı, 2026-09-14). PilotHUD oturumunda uzun,
çok adımlı iki şeritte (harita araştırması, harita JS entegrasyonu) hiçbir şey yazmadan
çıkış kodu 0 ile sessizce düştü; aynı işleri `gemini-3.8-flash-high` bitirdi. İnceleme ve
push şeritleri dahil hiçbir şeride verilmez.

**Sessiz düşme Flash'ta da oluyor (2026-09-14 ölçümü).** Aynı oturumda 3.8 Flash 12
şeritten 3'ünde hiçbir şey yazmadan, log boş ve çıkış kodu 0 ile kapandı. Düşenler hem
paralel hem tek başına çalışan şeritlerdi, sebep bulunamadı. 3.7 Flash devralınan 3
şeridin hepsini bitirdi. Sonuç: **çıkış kodu 0 ve boş log "bitti" demek değildir**; her
şeritten sonra `git status`, beklenen dosyanın varlığı veya log uzunluğu kontrol edilir,
boşsa iş 3.7 Flash'a devredilir.

### Yarım kalan şerit birikimiyle devredilir

kullanıcının 2026-09-12 kuralı: **bir şerit yarıda kalırsa iş sıfırdan yeniden başlatılmaz.**
Şerit zaman aşımı, izin hatası, dolan kota veya başarısız indirme yüzünden düştüğünde önce
logu okunur, oradaki somut birikim — bulunan adresler, denenip başarısız olan URL'ler ve
döndükleri HTTP kodları, doğrulanmış sürüm numaraları, kısmen inen dosyaların yolu ve
boyutu — sıradaki modelin brief'ine "önceki şerit şuraya kadar geldi" başlığı altında
aynen yazılır. Gerekçe: düşen şerit kotadan zaten ödendi, ve şeritler çoğunlukla son
adımda düşer — yani zor kısım genelde çözülmüş olur.

Bu sıra, skill'in eski "Antigravity içindeki Claude modellerini kullanma" kuralını
**iptal eder.** Gerekçe: `agy` içinden çağrılan Claude, Gemini aboneliğinden ödenir ve
Claude Code kotasına dokunmaz — yani ucuz katmanın amacı Claude'dan kaçınmak değil,
**Claude Code kotasının dışında kalmaktır.**

## Kilitli varsayılanlar

| Ayar | Değer | Ne zaman değiştir |
|---|---|---|
| Model | `claude-sonnet-4-6` | Yukarıdaki varsayılan model sırasına bak. Claude/GPT havuzu boşsa → `gemini-3.8-flash-high`. Model düşerse sırada bir alta in. |
| Çıktı | `--output-format text` | Çıktıyı script'le işleyeceksen `json`. |
| Kapsam | `-C` yerine `cd <dir>` + `--add-dir <dir>` | Şerit birden fazla klasör görecekse `--add-dir` tekrarlanır. |
| Zaman aşımı | `timeout 240` sar | Ağır tarama → 600. `--print-timeout` varsayılanı 5 dk. |
| Arka plan | >10 sn ise `run_in_background: true` | Kısa doğrulama sorusu ön planda kalabilir. |

## Tek şerit — temel komut

```bash
cd <ÇALIŞMA_DİZİNİ> && timeout 240 agy \
  --model claude-sonnet-4-6 \
  --add-dir <ÇALIŞMA_DİZİNİ> \
  --output-format text \
  -p='<KENDİ KENDİNE YETEN BRIEF>' 2>&1 | tail -40
```

`-p='...'` bitişik. Prompt tek tırnak içinde; içinde tek tırnak varsa `-p="..."` kullan.

## Salt-okuma şeridi (keşif — varsayılan kullanım)

Print modunun freni olmadığı için, **yazmasını istemediğin her şeritte briefe açıkça yaz.**
Bu bir öneri değil, tek koruma katmanı:

```bash
cd ~/ofis/<proje> && timeout 300 agy --model claude-sonnet-4-6 \
  --add-dir ~/ofis/<proje> --output-format text \
  -p='READ ONLY. Do not create, edit or delete any file. Do not run any command that writes.
Map this codebase: entry points, main modules, how they connect. Report as a short outline.' \
  2>&1 | tail -60
```

## Paralel filo

Bağımsız işler tek mesajda, hepsi `run_in_background: true` ile aynı anda fırlatılır.
Her şeridin logu ayrı dosyaya gider:

```bash
cd <DIR> && timeout 300 agy --model gemini-3.8-flash-high --add-dir <DIR> \
  --output-format text -p='<A ŞERİDİNİN BRIEF'İ>' > /tmp/agy-lane-A.log 2>&1
```

- **Şerit tavanı 4** (mutlak üst sınır 6). RAM değil, kotanın ve okunabilirliğin sınırı;
  altı logu birden süzmek zaten insan işi olmaktan çıkıyor.
- **Yazan şeritler ayrı klasörlerde durur.** Aynı dosyaya iki şerit yazarsa birbirini ezer.
  Aynı depoda eşzamanlı yazma gerekiyorsa `codex-fleet`'teki worktree deseni buraya da
  aynen uygulanır: şerit başına `git worktree`, şerit başına tek commit.
- **Brief şeridin bütün sözleşmesidir.** Delege senin konuşmanı görmez: hedef, sahip
  olduğu dosyalar, dokunmayacağı dosyalar, kabul kontrolü ve rapor biçimi briefte yazar.
- **"Bitti" bir iddiadır, kanıt değil.** Kabul kontrolünü sen çalıştır.
- Logu dakikalardır büyümeyen şerit ölmüştür; aynı briefle yeniden fırlat.

### Sözleşme dosyası deseni (2026-09-15, PilotHUD'da 4 kez tekrarlandı, çakışma sıfır)

Aynı projeye birden fazla yazan şerit gidecekse brief'ler tek tek yazılmaz; önce ana döngü
bir **sözleşme dosyası** yazar (`$SCRATCHPAD/sozlesme-<iş>.md`), her şeridin brief'i
"önce bu dosyayı oku" diye başlar. Sözleşmede dört bölüm olur:

1. **Sahiplik tablosu:** şerit → sahip olduğu dosyalar → dokunmayacağı dosyalar (ve sahibi).
2. **Arayüz sözleşmesi:** şeritlerin birbirine dayandığı adlar — DOM id'leri, fonksiyon
   imzaları, CSS sınıfları, olay adları. Biri adı değiştirirse diğeri kırılır; burada kilitlenir.
3. **Kabul kontrolü:** her şeridin bitti saymak için çalıştıracağı komut.
4. **Git kuralı:** yazan şeritler **commit ve push atmaz**. En sonda tek bir test şeridi
   (başsız tarayıcı veya test komutu) hepsini doğrular, tek commit atar, push eder.

### Yedekli şerit (2026-09-15, iki denemede üç kopyadan yalnızca biri bitti)

Şeritler sessizce düşüyor ve kota iş ortasında doluyor. Kritik bir işte aynı brief **2-3
kopya**, **farklı model karışımıyla** (ör. 3.8 Flash high + 3.7 Flash high + 3.7 Flash medium)
aynı anda fırlatılabilir. kullanıcı "yedekli aç" derse veya iş tek şeride güvenilmeyecek kadar
önemliyse kullanılır; varsayılan değildir, kota yer.

- **Salt okuma kopyası:** her kopya ayrı rapor dosyasına yazar (`rapor-A.md`, `rapor-B.md`).
- **Kod değiştiren kopya:** `git worktree add ../<iş>-A -b yedek/A` — her kopya kendi
  worktree'sinde kendi dalına tek commit atar. Ana döngü bitenleri karşılaştırır, en temizini
  `git merge --ff-only yedek/<X>` ile alır, sonra `git worktree remove` + dal silme.

### Kırılgan hedefe yazma (2026-09-12, USB bellek arızası)

İndirme ve doğrulama **sağlam diskte** yapılır (sağlama toplamı alınır); USB bellek, SD kart,
ağ sürücüsü gibi kırılgan hedefe yalnızca son adımda kopyalanır ve **geri okunarak** doğrulanır.
Hedef düşerse maliyet "baştan indir" değil "son kopyayı tekrarla" olur.

## Ne buraya gitmez

- Mimari kararı, spec yazımı, sözleşmeye duyarlı tasarım → ana döngü.
- Spec'i yazılmış hassas icra, doğruluk kritik refactor → `codex-fleet`.
- kullanıcının kişisel dosyaları: `🔐 kasa/`, telefondaki `Girdiler` günlüğü ve
  kişisel şifre dosyaları **hiçbir şeride verilmez** — ne `--add-dir` ile, ne brief içinde.

## Güncel bilgi araştırmasında sınırlar (2026-09-15 ölçümü)

- **3.6 Flash yeni şey aramıyor.** "2025-2026 modellerini bul, her iddiaya link koy" briefiyle
  iki turda da yalnızca bildiği eski sayfaları (Qwen2.5, Gemma 3) açıp doğruladı; 2026
  modellerini hiç bulmadı. Güncel liste gerekiyorsa şeride değil doğrudan kaynağa bak
  (ör. Hugging Face API `huggingface.co/api/models?author=X&sort=createdAt&direction=-1`).
- **Geniş kapsamlı 3.8 Flash şeritleri 14 dk `--print-timeout`'ta boş düştü** (3 şeritten 2'si,
  kısmi çıktı da yazmadı). Araştırma şeridine "en fazla N sayfa aç, sonra yaz" sınırı konur.
- **Şerit durdururken `pkill -f '<model adı>'` kullanma:** aynı dizeyi içeren kendi arka plan
  kabuğunu da öldürür. Task ID ile durdur.

## Araştırma şeridinin kaynak disiplini (0022, 0026 — üç kez tekrarladı)

Ucuz katman bilmediğini "bilmiyorum" diye yazmaz, makul görünen bir şey uydurur. En kolay
uydurulan üç tür: **kişi adları** (sporcu, hoca, yetkili), **kaynak adresleri** ve **özellik
tablolarındaki hücreler**. Brief'e "kaynak koy" yazmak yetmedi; üç şeritte de kaynak sütunu
ana sayfa adresleriyle doldu.

- **Ana sayfa kaynak sayılmaz.** Brief şart koşar: olgunun geçtiği **belge sayfasının tam
  adresi** verilir (`docs.x.com/hooks#sessionstart`), `docs.x.com` değil. Adres yoksa hücreye
  "bilinmiyor" yazılır — tahmin yazılmaz.
- **Kişi adı isteyen brief her ad için doğrulama URL'i ister.** URL'siz ad rapora girmez.
  Gemini Flash Türkiye federasyonları için uydurma hoca adları üretti; bir kısmı hiç yoktu.
- **Ana döngü örneklem kontrolü yapar.** Rapordaki kararı taşıyan satırlardan ikisi kaynaktan
  elle doğrulanır. 14 araçlık uyumluluk tablosunda iki iddiadan biri yanlış çıktı: rapor
  "kısmi" dedi, belgede özelliğin tamamı vardı.
