# <Proje Adı>

Bu proje çalışma ofisinde geliştirilmektedir.

**Bu klasör:** kaynak kod ve çalışan iş. Kararlar, açık sorular ve öğrenilenler proje notlarına yazılır.
<!-- Eğer bir hafıza sistemi ($HAFIZA) kullanılıyorsa, projenin düşünsel merkezi oradaki ikiz notudur ($HAFIZA/projeler/<slug>.md). -->

## Çalışma protokolü

- **`AGENTS.md` bu dosyaya symlink'tir.** Codex ve Claude aynı kuralları okur; birini değiştirmek ikisini birden değiştirir. Symlink'i kopyaya çevirme.
- **Yarım kalan iş `backlog.md`'ye düşer.** Oturum işi bitiremeden kapanıyorsa nerede kaldığı ve sıradaki adım oraya tek satır yazılır. Biten satır silinmez, `backlog-log.md`'ye taşınır.
- **Arka plan araştırmaları `reports/` altına yazılır.** Alt ajanlara yaptırılan keşif ve doküman taraması oraya düşer, doğrudan koda girmez: önce okunur, sonra karar olur.
- **Gizlilik:** Hassas ortam değişkenleri (.env) ve kişisel veriler depoya eklenmez.
