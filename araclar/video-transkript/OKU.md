# Video Transkript Düzeltme

Türkçe otomatik altyazı teknik terimleri **tutarlı biçimde** bozabiliyor ("Claude" yerine "cloud", "Anthropic" yerine "Antropik", "LLM" yerine "Elelem", "commit" yerine "komit", "vibe coding" yerine "vip coding").

Hata rastgele değil sistematik olduğu için sözlükle düzeltilebilmektedir.

## Kullanım

```bash
python3 duzelt.py <transkript.txt>          # yalnızca rapor, dosyaya dokunmaz
python3 duzelt.py <transkript.txt> --yaz    # uygular ve günlüğe işler
```

## İki Kategori

- **`kesin`**: Bağlamdan bağımsız güvenli değişimler, otomatik uygulanır ("cloud code" → "Claude Code", "elelem" → "LLM").
- **`supheli`**: Masum bir anlamı da olabilecek kelimeler. **Değiştirilmez, yalnızca raporlanır.** Tek başına "cloud" gerçekten "bulut" olabilir; "model" çoğu zaman doğrudur.

Bu ayrım, doğru bir kelimeyi sessizce bozma riskini önlemek içindir.

## Periyodik Denetim

Sözlüğün sağlığı için belirli aralıklarla şu adımlar izlenir:

1. **`duzeltme-gunlugu.md` okunur:** Hangi kural kaç kez çalışmış, beklenmedik bir değişim var mı?
2. **Yanlış düzeltme kontrolü:** Özellikle yeni eklenen bağlam kalıpları kontrol edilir.
3. **Yeni bozulmaların tespiti:** Şüpheli listesindeki örneklere bakılarak yeni kalıplar sözlüğe eklenir.

Denetim tarihi `sozluk.json` içindeki `_son_denetim` alanına yazılır.
