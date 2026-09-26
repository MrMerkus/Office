---
name: sablon-yayini
description: Kişisel bir çalışma düzenini (vault, ofis, skill paketi) başkalarının kurabileceği public bir şablon deposu olarak yayınlar; kişisel iz, commit geçmişi, dal ve temiz kurulum kontrollerini sırayla yapar. "şablon yayınla", "bunu public yap", "şablon deposu", "başkaları da kursun", "dağıtım sürümü çıkar" dendiğinde kullan.
---

# Şablon yayını

Kaynak: 2026-09-14'te üç depo (vault, ofis, skill paketi) aynı zincirle elle yayınlandı.
Yakalanan hataların **hiçbiri içerik taramasında görünmedi**: kasa klasörü `.gitignore`'da
değildi, klonlanan kopya şablon deposunu `origin` tutuyordu, yerel kopya eski `master`
dalındaydı, eski dalın geçmişinde gerçek ad ve gmail duruyordu. Yani dosyalara bakmak yetmez;
**geçmişe, dala, uzağa ve kuruluma** bakılır.

## Değişmez kurallar

- Public depoya yalnızca yayınlanan ürün girer. `CLAUDE.md`/`AGENTS.md` iç kuralları,
  `backlog.md`, `reports/`, `spec/`, `.state/`, günlük ve hafıza içerikleri girmez.
- Kimlik: **<GITHUB KULLANICI>** + `<GITHUB NOREPLY>`. `<KİŞİSEL E-POSTA>`
  hiçbir dosyada ve **hiçbir commit'te** geçmez. Gerçek ad sorun değildir.
- Kaynaktan **kopyalanır**, kaynak depo yayınlanmaz. Yayın her zaman taze bir klasörde
  (`~/ofis/<slug>-dagitim/`) ve **tek commit'lik yeni geçmişle** başlar.
- Metin genelleştirme (kişisel ifade → yer tutucu) mümkünse **script'le** yapılır; model
  yaparsa içeriği kırpar (bkz. `fable-orchestration`, "Brief'teki genel kural"). Kabul
  kontrolünde kaynakla kelime sayısı karşılaştırılır.

## Zincir

Her adımın kontrolü geçmeden sonrakine geçilmez. kullanıcıya planı göster, onay al, sonra başla.

1. **Kopyala.** `rsync -a --exclude-from=<hariç-listesi> <kaynak>/ <dagitim>/` — hariç listesi:
   `.git`, `🔐 kasa/`, `.state/`, `daily/`, `knowledge/`, günlük/defter, `node_modules`, `.env*`,
   iç çalışma dosyaları. Liste dağıtım klasöründe `dagit-haric.txt` olarak saklanır.
2. **Genelleştir.** Kişisel ifadeler (kullanıcı, Deha/Bilinmez hitapları, yerel yollar
   `$HOME`, proje adları) bir `sed` tablosuyla yer tutucuya çevrilir. Tablo
   `dagit-degistir.tsv` olarak saklanır ki bir sonraki sürümde tekrar kullanılsın.
3. **İçerik iz taraması.** Sıfır sonuç beklenir:
   `grep -rIn -iE "<E-POSTA ADI>|gmail|$HOME|kullanıcı|sk-[A-Za-z0-9]{20}|ghp_|AIza" <dagitim>`
   Sonuç varsa 2. adıma dön; elle istisna yazılacaksa gerekçesi `dagit-degistir.tsv`'ye not düşülür.
4. **`.gitignore` kontrolü.** Hassas klasörler (`kasa`, `.state`, `.env`) listede mi? Boş bir
   test dosyası oluşturup `git check-ignore -v` ile doğrula.
5. **Yeni geçmiş.** `git init -b main`, kimlik yerel olarak <GITHUB KULLANICI>+noreply ayarlanır, tek commit.
   Sonra **geçmiş taraması**: `git log --all --format='%an %ae %cn %ce' | sort -u` yalnızca
   <GITHUB KULLANICI>+noreply göstermeli. `git branch -a` yalnızca `main`.
6. **Uzak kontrolü.** `git remote -v` — `origin` yayın deposu olmalı; kaynak veya eski şablon
   deposu görünüyorsa sil.
7. **Temiz kurulum denemesi.** Yalıtılmış HOME'da uçtan uca: `HOME=$(mktemp -d) bash -c
   'git clone <dagitim> x && cd x && <kurulum komutu>'`. README'deki adımlar birebir izlenir;
   kırılan her adım README'ye veya kuruluma düzeltme olarak döner.
8. **Push ve görünürlük.** `gh repo create <GITHUB KULLANICI>/<ad> --public --source . --push` (ilk kez)
   ya da `git push`. Sonra `gh repo view --json visibility,defaultBranchRef` ile public ve
   varsayılan dalın `main` olduğu doğrulanır.
9. **Kayıt.** Proje notuna (`🏰 İş/<slug>/`) sürüm, tarih, depo adresi ve bu turda yakalanan
   hatalar tek satırlarla yazılır.

## Sonraki sürümler

Aynı zincir; 1-2. adımlar saklanan `dagit-haric.txt` ve `dagit-degistir.tsv` ile tekrar edilir.
Yayın deposu yeni geçmişle ezilmez: dağıtım klasöründe normal commit atılır, ama her commit'ten
önce 3, 5 ve 7. adımlar yeniden çalıştırılır.
