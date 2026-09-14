# Çalışma Ofisi Kuralları

Bu dizin, projelerin geliştirildiği ana çalışma alanıdır. Karmaşayı önlemek ve araçlar arası uyumu korumak için aşağıdaki kurallar uygulanır.

## 1. Her Proje Kendi Klasöründe

- Ofis kökünde başıboş kod veya dosya tutulmaz.
- Her iş, `$OFIS/projeler/<slug>` veya `$OFIS/<slug>` altında kendi izole klasöründe ve kendi git deposunda yaşar.
- Klasör adı (slug) küçük harf, ASCII ve tire ile ayrılmış olmalıdır (`ornek-proje`).

## 2. AGENTS.md ve CLAUDE.md Eşleşmesi

- Her projenin kökünde bir `CLAUDE.md` bulunur.
- **`AGENTS.md` her zaman `CLAUDE.md` dosyasına bir sembolik bağdır (symlink).**
- Codex `AGENTS.md`, Claude Code ise `CLAUDE.md` okur. İki ayrı dosya tutulmaz; kural kayması dosya sistemi düzeyinde engellenir.

## 3. Yarım Kalan İşler ve Araştırmalar

- **`backlog.md`:** Yarım kalan işler buraya tek satır olarak kaydedilir: ne yarım kaldı, nerede kaldı, sıradaki adım ne. Biten maddeler silinmez, `backlog-log.md`'ye aktarılır.
- **`reports/`:** Alt ajanlara yaptırılan araştırma, tarama ve analiz çıktıları bu klasöre kaydedilir. Kod içine doğrudan girmeden önce insan veya ana döngü tarafından incelenir.

## 4. Hafıza Köprüsü (İsteğe Bağlı)

Eğer harici bir hafıza sistemi (`$HAFIZA`) kullanılıyorsa, projenin mimari kararları ve öğrenilen dersleri oradaki ikiz notta tutulur. Kod ofiste, akıl ve süreklilik hafıza sisteminde kalır.
