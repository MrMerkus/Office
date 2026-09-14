# Ofis

Claude Code, Antigravity (`agy`) ve Codex için tasarlanmış Türkçe yapay zekâ çalışma ofisi şablonu. Her projeyi izole bir alt klasörde tutar, araçlar arası iş bölümü sağlar ve geliştirme sürecini yapılandırır.

## Kurulum

Claude Code'u boş bir klasörde aç ve şunu yapıştır:

```
https://github.com/MrMerkus/My-AI-System deposundaki KURULUM.md dosyasını oku ve beni kur. Sadece ofisi istiyorum.
```

Claude isimleri ve klasörleri tek tek sorar, özeti onaylatır, kurulumu `kur.sh` yapar. Elle kurmak
istersen depoyu indirip `bash kur.sh` çalıştır. Seçilen yollar `~/.config/my-ai-system/sistem.json`
dosyasında durur; skill'ler ve araçlar ofis ile hafıza klasörünü oradan okur.

## Araç uyumluluğu

Bugün **Claude Code**'da tam çalışır ve kurulum onunla test edildi. **Codex** ve **Antigravity**
için hafıza köprüleri var ama kısmi; **Gemini CLI** ve **Cursor** desteği planlandı. Ayrıntılı
tablo ve yol haritası: [ARAC-UYUMLULUK.md](https://github.com/MrMerkus/My-AI-System/blob/main/ARAC-UYUMLULUK.md)

## 3 Katmanlı Ajan Mimarisi

1. **Ana Döngü — Claude Code:** Mimari kararlar, şartname (spec) yazımı, kod birleştirme ve son sentez. En yüksek akıl ve yargı katmanı.
2. **Ucuz Alt Katman — Antigravity (`agy`):** Keşif, kod tabanı haritalama, hızlı tarama ve mekanik işler. Geniş bağlamı ucuza tüketir.
3. **İcra Katmanı — Codex (`codex exec`):** Şartnamesi hazırlanmış görevlerin icrası, refactor, paralel şeritler, test yazımı ve görsel üretimi.

## Klasör Düzeni

- `projeler/`: Her projenin kendi alt klasörü ve git deposu.
- `sablonlar/`: Yeni projeler için köprü şablonları (`CLAUDE.md`, `backlog.md`, `reports/`).
- `araclar/`: Bakım, geri yükleme, transkript düzeltme ve token izleme betikleri.
- `skills/`: Ofisin yerel becerileri.
- `skill-gozlemleri/`: Çalışırken fark edilen örüntülerin ve sürtünmelerin biriktiği defter.
- `upstream.tsv`: Dışarıdan çekilen üçüncü parti repoların sicil kaydı.

## Hızlı Kurulum

```bash
bash kur.sh
```

Türkçe tetikleyicileri etkinleştirmek için:

```bash
bash kur.sh --turkce
```

Kurulum betiği yerel becerileri `~/.claude/skills/` altına kopyalar, `upstream.tsv` içindeki depoları çeker ve gerekli sembolik bağları kurar.

## Yerel Beceriler

- `basla`: İş tanımına göre doğru çalışma kümesini belirler ve yönlendirir.
- `karar`: Seçenekler arasında kalındığında veya fikir test edilirken kullanılır.
- `kod`: Yazılım geliştirme, hata ayıklama ve sürüm adımlarını yönetir.
- `site`: Web sitesi, arayüz geliştirme ve yayın süreçlerini yürütür.
- `temizlik`: Kod tabanındaki fazlalıkları bulur ve sadeleştirir.
- `arastirma`: Doküman, web ve video kaynaklarından bilgi toplar.
- `fable-orchestration`: 3 katmanlı yığın için delege ve görev dağıtım politikası.
- `antigravity-fleet`: `agy` üzerinden keşif ve hafif mekanik işleri yürüten filo koşucusu.
- `codex-fleet`: `codex exec` ile şartnamesi yazılmış icra ve görsel üretimi.
- `gorsel-handoff`: ChatGPT web arayüzüyle yarı otomatik görsel üretim döngüsü.
- `yeni-proje`: Ofiste yeni proje klasörü, git deposu ve hafıza köprüsü kurar.
- `skill-gozlemcisi`: Tekrar eden örüntüleri ve sürtünme anlarını gözlem olarak kaydeder.

## Dış Kaynak Becerileri (Upstream)

- **agent-skills**: Addy Osmani — Apache-2.0 — https://github.com/addyosmani/agent-skills
- **last30days**: Mark Van Horn — MIT — https://github.com/mvanhorn/last30days-skill
- **council-of-high-intelligence**: 0xNyk — MIT — https://github.com/0xNyk/council-of-high-intelligence
- **ponytail**: Dietrich Gebert — MIT — https://github.com/DietrichGebert/ponytail
- **impeccable**: Paul Bakaus — MIT — https://github.com/pbakaus/impeccable
- **ui-ux-pro-max**: nextlevelbuilder — MIT — https://github.com/nextlevelbuilder/ui-ux-pro-max-skill
- **claude-video**: Brad Automates — MIT — https://github.com/bradautomates/claude-video

Bazı skill'ler Avenox (avenoxai) çalışmalarından uyarlanmıştır (MIT).
