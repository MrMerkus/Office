#!/usr/bin/env python3
"""codeburn'ün ürettiği bütün kullanım verisini markdown bir kayda çevirir.

Sayma işini codeburn yapar; bu betik kaydı tutar ve okunur hâle getirir.
İkinci bir sayaç kurulmamasının sebebi basit: iki sayaç bir gün çelişir ve hangisinin
doğru olduğu bilinemez.

Toplanan kaynaklar:
  sessions --format json   → oturum başına 16 alan (asıl tablo)
  models   --format json   → model başına token, maliyet, çağrı
  overview                 → faaliyet dağılımı, araç kullanımı, günlük ve proje toplamları
  plan                     → abonelik / fiyatlandırma görünümü

Oturumlar sessionId ile eşleşir: betik kaç kez çalışırsa çalışsın satır çoğalmaz,
devam eden bir oturumun satırı yerinde güncellenir.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path


def ayarlar() -> dict:
    """Sistem ayarlarını ~/.config/my-ai-system/sistem.json dosyasından okur."""
    varsayilan = {
        "sistem_adi": "My AI System",
        "asistan_adi": "Atlas",
        "dil": "Türkçe",
        "kok": str(Path.home() / "yapay-zeka-sistemim"),
        "hafiza": os.environ.get("HAFIZA"),
        "ofis": os.environ.get("OFIS") or str(Path.home() / "ofis"),
    }
    ayar_dosyasi = Path.home() / ".config" / "my-ai-system" / "sistem.json"
    if ayar_dosyasi.exists():
        try:
            with open(ayar_dosyasi, "r", encoding="utf-8") as f:
                veri = json.load(f)
                if isinstance(veri, dict):
                    varsayilan.update(veri)
        except Exception:
            pass
    if os.environ.get("OFIS"):
        varsayilan["ofis"] = os.environ["OFIS"]
    if os.environ.get("HAFIZA"):
        varsayilan["hafiza"] = os.environ["HAFIZA"]
    if not varsayilan.get("ofis"):
        varsayilan["ofis"] = str(Path.home() / "ofis")
    return varsayilan


OFIS = Path(ayarlar()["ofis"])
KAYIT = Path(os.environ.get("TOKEN_KAYIT") or (OFIS / "token-kullanimi.md"))
ZAMAN_ASIMI = 600


def codeburn_yolu() -> list[str]:
    """Kurulu codeburn'ü tercih eder; yoksa npx'e düşer."""
    for aday in (shutil.which("codeburn"),
                 str(Path.home() / ".local/npm/bin/codeburn"),
                 str(Path.home() / ".npm-global/bin/codeburn")):
        if aday and Path(aday).exists():
            return [aday]
    return ["npx", "--yes", "codeburn"]


ANSI = re.compile(r"\x1b\[[0-9;]*[a-zA-Z]")


def cb(*args: str) -> str:
    """codeburn'ü çalıştırır, npm gürültüsünü ve ANSI dizilerini ayıklar."""
    ortam = {**os.environ, "NO_COLOR": "1", "FORCE_COLOR": "0", "TERM": "dumb"}
    r = subprocess.run([*codeburn_yolu(), *args], env=ortam,
                       capture_output=True, text=True, timeout=ZAMAN_ASIMI)
    if r.returncode != 0:
        sys.exit(f"codeburn {' '.join(args)} çalışmadı:\n{r.stderr[-400:]}")
    temiz = ANSI.sub("", r.stdout)
    return "\n".join(s for s in temiz.splitlines() if not s.startswith("npm notice"))


def cb_json(*args: str):
    metin = cb(*args)
    bas = min((metin.index(c) for c in "[{" if c in metin), default=-1)
    if bas < 0:
        return []
    return json.loads(metin[bas:])


# codeburn çıktısı İngilizce; kullanıcı için tablo başlıkları Türkçeye çevrilir.
SOZLUK = {
    "Provider": "Sağlayıcı", "Top Task": "Ağırlıklı iş", "Cache Write": "Cache yaz",
    "Cache Read": "Cache oku", "Input": "Girdi", "Output": "Çıktı", "Total": "Toplam",
    "Cost": "Maliyet", "Saved": "Tasarruf", "Activity": "Faaliyet", "Turns": "Tur",
    "Tool": "Araç", "Calls": "Çağrı", "Date": "Tarih", "Tokens": "Token",
    "Providers": "Sağlayıcılar", "Project": "Proje", "Sessions": "Oturum",
    "Type": "Tür", "Share": "Pay", "Model": "Model", "Communities": "Topluluk",
    "**Total**": "**Toplam**", "**Cost**": "**Maliyet**",
    "Coding": "Kodlama", "Conversation": "Konuşma", "Debugging": "Hata ayıklama",
    "Exploration": "Keşif", "Feature Dev": "Özellik geliştirme", "Research": "Araştırma",
    "Writing": "Yazma", "Refactoring": "Yeniden düzenleme", "Testing": "Test",
    "Cache in": "Cache giriş", "Cache out": "Cache çıkış",
}


def turkcelestir(metin: str) -> str:
    """Tablo başlıklarını ve bilinen etiketleri Türkçeye çevirir."""
    satirlar = []
    for s in metin.splitlines():
        ayrac = "│" if "│" in s else ("|" if "|" in s else None)
        if ayrac:
            parcalar = s.split(ayrac)
            parcalar = [
                p.replace(p.strip(), SOZLUK[p.strip()]) if p.strip() in SOZLUK else p
                for p in parcalar
            ]
            s = ayrac.join(str(x) for x in parcalar)
        satirlar.append(s)
    metin = "\n".join(satirlar)
    metin = re.sub(r"\$(\d+)\.(\d),(\d+)", lambda m: f"${m.group(1)}.{m.group(2)}{m.group(3)}", metin)
    return metin


def sayi(n) -> str:
    try:
        return f"{int(n):,}".replace(",", ".")
    except (TypeError, ValueError):
        return str(n)


def sure(ms) -> str:
    try:
        dk = int(ms) // 60000
    except (TypeError, ValueError):
        return "?"
    return f"{dk // 60}s {dk % 60}dk" if dk >= 60 else f"{dk}dk"


def bolum_ayikla(overview: str, baslik: str) -> list[str]:
    """overview çıktısındaki bir başlığın altındaki kutu satırlarını döndürür."""
    satirlar = overview.splitlines()
    try:
        i = next(n for n, s in enumerate(satirlar) if s.strip() == baslik)
    except StopIteration:
        return []
    out = []
    for s in satirlar[i + 1:]:
        if s.strip() and not s.startswith(("│", "┌", "├", "└", "┬", "┼", "┴")):
            break
        if s.startswith("│"):
            out.append(s)
    return out


def kutu_to_tablo(satirlar: list[str]) -> str:
    """Kutu çizgili codeburn tablosunu markdown tabloya çevirir."""
    hucreler = [[h.strip() for h in s.strip("│").split("│")] for s in satirlar]
    hucreler = [h for h in hucreler if any(h)]
    if not hucreler:
        return ""
    bas, *govde = hucreler
    md = "| " + " | ".join(bas) + " |\n|" + "|".join("---" for _ in bas) + "|\n"
    md += "\n".join("| " + " | ".join(r) + " |" for r in govde)
    return md + "\n"


def satir_uret(o: dict) -> str:
    bas = datetime.fromisoformat(o["startedAt"].replace("Z", "+00:00")).astimezone()
    baslik = (o.get("title") or "(başlıksız)").replace("|", "·")[:40]
    proje = (o.get("project") or "").split("-")[-1][:16]
    return (
        f"| {bas:%Y-%m-%d} | {bas:%H:%M} | {baslik} | {proje} | {o.get('provider','?')} | "
        f"{', '.join(o.get('models') or ['?'])[:20]} | {o.get('turns',0)} | {o.get('calls',0)} | "
        f"{sayi(o.get('inputTokens',0))} | {sayi(o.get('outputTokens',0))} | "
        f"{sayi(o.get('cacheReadTokens',0))} | {sayi(o.get('cacheWriteTokens',0))} | "
        f"{sure(o.get('durationMs'))} | ${o.get('cost',0):.2f} |"
        f" <!-- sid:{o['sessionId']} -->"
    )


TABLO_BAS = (
    "| Tarih | Saat | Oturum | Proje | Sağlayıcı | Model | Tur | Çağrı | "
    "Girdi | Çıktı | Cache oku | Cache yaz | Süre | Maliyet |\n"
    "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|\n"
)


def main() -> None:
    period = sys.argv[1] if len(sys.argv) > 1 else "30days"
    oturumlar = cb_json("sessions", "--period", period, "--format", "json")
    modeller = turkcelestir(cb("models", "--period", period, "--format", "markdown"))
    overview = turkcelestir(cb("overview"))
    plan = cb("plan")

    eski = KAYIT.read_text(encoding="utf-8") if KAYIT.exists() else ""
    satirlar = {m.group(1): s for s in eski.splitlines()
                if (m := re.search(r"<!-- sid:([0-9a-f-]+) -->", s))}
    yeni = sum(1 for o in oturumlar if o["sessionId"] not in satirlar)
    for o in oturumlar:
        satirlar[o["sessionId"]] = satir_uret(o)
    sirali = sorted(satirlar.values(), key=lambda s: s.split("|")[1:3])

    plan_satiri = next((s.strip() for s in plan.splitlines() if s.strip().startswith("Plan:")), "Plan: bilinmiyor")
    if plan_satiri.strip() in ("Plan: none", "Plan: None"):
        plan_satiri = "Abonelik planı tanımlı değil — API fiyatlandırmasına göre hesaplanıyor"
    bugun = datetime.now().strftime("%Y-%m-%d")

    p = [f"""---
title: Token Kullanımı
created: 2026-09-06
modified: {bugun}
type: note
status: active
tags: [token, maliyet, olcum, araclar]
---

# Token Kullanımı

Bütün AI araçlarının tüketim kaydı. Sayan codeburn, yazan token kaydetme betiği.
Bu dosya elle düzenlenmez: betik her çalıştığında eksik oturumları ekler, devam edenleri
yerinde günceller.

**Abonelik durumu:** {plan_satiri}

**Cache okumasına dikkat:** Toplam token sayısının büyük kısmı `Cache oku` sütunudur:
konuşma uzadıkça her turda bütün bağlam yeniden okunur. Bu okuma önbellekten geldiği için
ucuzdur ancak ham token rakamını şişirir. Maliyeti anlamak için `Çıktı` ve `Maliyet`
sütunlarına bakılır.

## Oturumlar

"""]
    p.append(TABLO_BAS + "\n".join(sirali) + "\n")

    p.append("\n## Model başına\n\n" + (modeller.strip() or "_veri yok_") + "\n")

    for baslik, ad in [("Totals", "Genel toplamlar"), ("Tokens", "Token dağılımı"),
                       ("By tool", "Araç başına maliyet"), ("Top models", "En çok kullanılan modeller"),
                       ("Top projects", "Projeler"), ("Daily", "Günlük toplamlar"),
                       ("By activity", "Faaliyet dağılımı"), ("Tools", "Araç çağrı sayıları")]:
        t = kutu_to_tablo(bolum_ayikla(overview, baslik))
        if t:
            p.append(f"\n## {ad}\n\n{t}")

    alt = next((s.strip() for s in overview.splitlines() if s.strip().startswith("Bottom line")), "")
    if alt:
        alt = (alt.replace("Bottom line:", "Sonuç:").replace(" totals ", " toplamı: ")
                  .replace(" across ", " · ").replace(" tokens", " token")
                  .replace(", mostly ", " · ağırlıklı olarak "))
        p.append(f"\n## Özet\n\n{alt}\n")

    tc = sum(o.get("outputTokens", 0) for o in oturumlar)
    tm = sum(o.get("cost", 0) for o in oturumlar)
    p.append(f"\n---\n\n**Kayıtlı oturum:** {len(satirlar)} · **son {period} çıktı tokeni:** "
             f"{sayi(tc)} · **son {period} maliyet:** ${tm:.2f} · **güncelleme:** {bugun}\n")

    KAYIT.parent.mkdir(parents=True, exist_ok=True)
    KAYIT.write_text("".join(p), encoding="utf-8")
    print(f"{KAYIT.name}: {len(satirlar)} oturum ({yeni} yeni) · model, faaliyet, araç, günlük, proje tabloları yazıldı")


if __name__ == "__main__":
    main()
