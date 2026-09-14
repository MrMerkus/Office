---
name: antigravity-fleet
description: "Antigravity CLI (`agy`) runner and fleet orchestrator — the cheap tier of the user's stack. Hands recon, codebase mapping, research sweeps, reviews and mechanical edits to Claude Opus 4.6 or Gemini via `agy -p` (default model order is documented inside), one lane or several in parallel, always EXECUTING rather than describing. Paid separately (Gemini Pro subscription through December), so it does NOT consume the Claude or Codex budget. Triggers on: 'agy', 'antigravity', 'gemini'ye ver', 'geminiye sor', 'ucuz katmana ver', 'alt ajana tara', 'keşif yap', 'şu klasörde ne var', 'bunu tarasın', 'ucuza yaptır', any recon/mapping/summarize task big enough to be worth offloading."
---

# Antigravity Fleet — ucuz katman koşucusu

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

## Varsayılan model sırası

kullanıcı 2026-09-12'de bu sırayı kendi eliyle koydu. **Şerit açarken listenin başından
başlanır, başarısız olan veya kotası dolan modelde bir alt sıraya inilir.**

| Sıra | Model kimliği | Ne için |
|---|---|---|
| 1 | `claude-opus-4-6-thinking` | Varsayılan. Yargı ve hassasiyet isteyen her şerit. |
| 2 | `gemini-3.8-flash-high` | Opus düştüğünde ve toplu, mekanik, hızlı taramalarda. |
| 3 | `gemini-3.7-flash-high` | Üstteki ikisi düştüğünde. |
| 4 | `claude-sonnet-4-6` | Dördüncü sıra; Opus'a en yakın yedek. |
| 5+ | Gerisi serbest | `gemini-3.1-pro-*`, `gemini-3.6-flash-*`, `gpt-oss-120b-medium` — duruma göre seçilir. |

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
**Claude Code kotasının dışında kalmaktır.** Opus 4.6 orada en kaliteli icra seçeneği
olduğu için birinci sıradadır.

## Kilitli varsayılanlar

| Ayar | Değer | Ne zaman değiştir |
|---|---|---|
| Model | `claude-opus-4-6-thinking` | Yukarıdaki varsayılan model sırasına bak. Toplu, mekanik, ucuz tarama → `gemini-3.8-flash-high`. Model düşerse sırada bir alta in. |
| Çıktı | `--output-format text` | Çıktıyı script'le işleyeceksen `json`. |
| Kapsam | `-C` yerine `cd <dir>` + `--add-dir <dir>` | Şerit birden fazla klasör görecekse `--add-dir` tekrarlanır. |
| Zaman aşımı | `timeout 240` sar | Ağır tarama → 600. `--print-timeout` varsayılanı 5 dk. |
| Arka plan | >10 sn ise `run_in_background: true` | Kısa doğrulama sorusu ön planda kalabilir. |

## Tek şerit — temel komut

```bash
cd <ÇALIŞMA_DİZİNİ> && timeout 240 agy \
  --model claude-opus-4-6-thinking \
  --add-dir <ÇALIŞMA_DİZİNİ> \
  --output-format text \
  -p='<KENDİ KENDİNE YETEN BRIEF>' 2>&1 | tail -40
```

`-p='...'` bitişik. Prompt tek tırnak içinde; içinde tek tırnak varsa `-p="..."` kullan.

## Salt-okuma şeridi (keşif — varsayılan kullanım)

Print modunun freni olmadığı için, **yazmasını istemediğin her şeritte briefe açıkça yaz.**
Bu bir öneri değil, tek koruma katmanı:

```bash
cd ~/ofis/<proje> && timeout 300 agy --model claude-opus-4-6-thinking \
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

## Ne buraya gitmez

- Mimari kararı, spec yazımı, sözleşmeye duyarlı tasarım → ana döngü.
- Spec'i yazılmış hassas icra, doğruluk kritik refactor → `codex-fleet`.
- Kullanıcının hassas dosyaları (şifreler, özel notlar, kişisel günlükler) **hiçbir şeride
  verilmez** — ne `--add-dir` ile, ne brief içinde.
