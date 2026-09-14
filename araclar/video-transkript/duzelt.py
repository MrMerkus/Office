#!/usr/bin/env python3
"""Video transkriptlerindeki ASR hatalarını düzeltir ve ne yaptığını raporlar.

Türkçe otomatik altyazı teknik terimleri tutarlı biçimde bozabiliyor: "Claude"
"cloud" olabiliyor, "Anthropic" "Antropik" olabiliyor, "LLM" "Elelem" olabiliyor.
Hata rastgele değil sistematik olduğu için sözlükle düzeltilebiliyor.

İki kategori var:
  kesin    — bağlamdan bağımsız güvenli değişimler, otomatik uygulanır
  supheli  — masum bir anlamı da olabilecek kelimeler, yalnızca RAPOR EDİLİR

Kullanım:
    python3 duzelt.py <transkript.txt> [--yaz]

--yaz verilmezse dosyaya dokunulmaz, yalnızca rapor basılır.
"""

from __future__ import annotations

import json
import re
import sys
from datetime import date
from pathlib import Path

KOK = Path(__file__).parent
SOZLUK = KOK / "sozluk.json"
GUNLUK = KOK / "duzeltme-gunlugu.md"


def yukle() -> dict:
    return json.loads(SOZLUK.read_text(encoding="utf-8"))


def uygula(metin: str, kesin: dict[str, str]) -> tuple[str, list[tuple[str, str, int]]]:
    """Kesin kuralları uygular. Uzun kalıplar önce denenir."""
    kayit = []
    for yanlis in sorted(kesin, key=len, reverse=True):
        dogru = kesin[yanlis]
        desen = re.compile(rf"\b{re.escape(yanlis)}\b", re.IGNORECASE)
        n = len(desen.findall(metin))
        if n:
            metin = desen.sub(dogru, metin)
            kayit.append((yanlis, dogru, n))
    return metin, kayit


def tara(metin: str, supheli: dict[str, str]) -> list[tuple[str, int, str]]:
    """Şüphelileri yalnızca sayar ve örnek gösterir; hiçbirini değiştirmez."""
    bulunan = []
    for kelime, not_ in supheli.items():
        desen = re.compile(rf"\b{re.escape(kelime)}\w*", re.IGNORECASE)
        eslesme = desen.findall(metin)
        if eslesme:
            ilk = re.search(rf".{{0,45}}\b{re.escape(kelime)}\w*.{{0,45}}", metin, re.IGNORECASE)
            bulunan.append((kelime, len(eslesme), (ilk.group(0).strip() if ilk else "")))
    return bulunan


def main() -> None:
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    yol = Path(sys.argv[1])
    yaz = "--yaz" in sys.argv
    metin = yol.read_text(encoding="utf-8")

    s = yukle()
    yeni, kayit = uygula(metin, s["kesin"])
    supheliler = tara(yeni, s["supheli"])

    print(f"=== {yol.name} ===")
    print(f"kelime: {len(metin.split())}")
    print()
    if kayit:
        print("DÜZELTİLDİ:")
        for yanlis, dogru, n in kayit:
            print(f"  {yanlis!r} → {dogru!r}  ×{n}")
    else:
        print("DÜZELTİLDİ: (kesin kural eşleşmedi)")
    print()
    if supheliler:
        print("ŞÜPHELİ (değiştirilmedi, gözle bak):")
        for kelime, n, ornek in supheliler:
            print(f"  {kelime!r} ×{n} — {s['supheli'][kelime]}")
            if ornek:
                print(f"      … {ornek}")
    else:
        print("ŞÜPHELİ: yok")

    if yaz:
        yol.write_text(yeni, encoding="utf-8")
        satir = f"- {date.today()} · `{yol.name}` · " + (
            ", ".join(f"{y}→{d} ×{n}" for y, d, n in kayit) if kayit else "değişiklik yok")
        if not GUNLUK.exists():
            GUNLUK.write_text("# Düzeltme Günlüğü\n\nHer uygulanan düzeltme buraya düşer.\n", encoding="utf-8")
        with GUNLUK.open("a", encoding="utf-8") as f:
            f.write(satir + "\n")
        print(f"\n✔ dosya güncellendi, günlüğe işlendi: {GUNLUK.name}")
    else:
        print("\n(dosyaya dokunulmadı — uygulamak için --yaz ekle)")


if __name__ == "__main__":
    main()
