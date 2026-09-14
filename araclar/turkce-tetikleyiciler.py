#!/usr/bin/env python3
"""Türkçe tetikleyicileri skill açıklamalarına ekler.

Kaynak: turkce-tetikleyiciler.md
Skill'ler güncellendikten sonra bu betiği tekrar çalıştır — kayıp olmaz.
Güvenli: zaten eklenmişse dokunmaz, tekrar tekrar çalıştırılabilir.
"""
import argparse
import os
import pathlib
import re
import sys

IMZA = "Türkçe tetikleyiciler:"


def varsayilan_yollar():
    kok = pathlib.Path(__file__).resolve().parent
    kural = os.environ.get("TURKCE_TETIKLEYICILER_MD")
    kural_yol = pathlib.Path(kural) if kural else (kok / "turkce-tetikleyiciler.md")

    skills = os.environ.get("CLAUDE_SKILLS_DIR")
    skills_yol = pathlib.Path(skills) if skills else (pathlib.Path.home() / ".claude/skills")

    return kural_yol, skills_yol


def yamayi_oku(yol: pathlib.Path) -> dict[str, list[str]]:
    """Kural dosyasındaki ```yama bloğunu okur."""
    metin = yol.read_text(encoding="utf-8")
    blok = re.search(r"```yama\n(.*?)```", metin, re.S)
    if not blok:
        sys.exit(f"HATA: {yol} içinde ```yama bloğu bulunamadı.")
    tablo = {}
    for satir in blok.group(1).splitlines():
        satir = satir.strip()
        if not satir or "::" not in satir:
            continue
        ad, ifadeler = satir.split("::", 1)
        liste = [x.strip() for x in ifadeler.split("|") if x.strip()]
        if liste:
            tablo[ad.strip()] = liste
    return tablo


def cumle_kur(ifadeler: list[str]) -> str:
    tirnakli = ", ".join(f'"{x}"' for x in ifadeler)
    return f"{IMZA} {tirnakli}."


def frontmatter_bul(metin: str):
    """--- ... --- arasındaki frontmatter'ı döndürür: (bas, son, govde)"""
    m = re.match(r"^---\n(.*?)\n---", metin, re.S)
    if not m:
        return None
    return m.start(1), m.end(1), m.group(1)


def description_sonu(fm: str):
    """Frontmatter içinde description alanının bittiği konumu bulur."""
    m = re.search(r"^description:[ \t]*(.*)$", fm, re.M)
    if not m:
        return None
    ilk = m.group(1).strip()
    if ilk in (">", ">-", "|", "|-", ""):
        son = m.end()
        for satir in fm[m.end():].splitlines(keepends=True):
            if satir.strip() == "" or satir[:1] in (" ", "\t"):
                son += len(satir)
            else:
                break
        return son
    return m.end()


def uygula(kural_yol: pathlib.Path, skills_yol: pathlib.Path, kuru: bool = False):
    if not kural_yol.exists():
        sys.exit(f"HATA: kural dosyası yok: {kural_yol}")
    if not skills_yol.exists():
        sys.exit(f"HATA: skill klasörü yok: {skills_yol}")

    tablo = yamayi_oku(kural_yol)
    eklendi, atlandi, bulunamadi = [], [], []

    for ad, ifadeler in sorted(tablo.items()):
        sm = skills_yol / ad / "SKILL.md"
        if not sm.exists():
            bulunamadi.append(ad)
            continue

        metin = sm.read_text(encoding="utf-8")
        if IMZA in metin:
            atlandi.append(ad)
            continue

        fm = frontmatter_bul(metin)
        if not fm:
            bulunamadi.append(f"{ad} (frontmatter yok)")
            continue
        fm_bas, fm_son, fm_govde = fm

        yer = description_sonu(fm_govde)
        if yer is None:
            bulunamadi.append(f"{ad} (description yok)")
            continue

        cumle = cumle_kur(ifadeler)
        onceki = fm_govde[:yer].rstrip()
        ayrac = " " if onceki.endswith((".", "!", "?", '"')) else ". "
        kalan = fm_govde[yer:]
        if kalan and not kalan.startswith("\n"):
            kalan = "\n" + kalan
        yeni_fm = onceki + ayrac + cumle + kalan
        yeni_metin = metin[:fm_bas] + yeni_fm + metin[fm_son:]

        if not kuru:
            sm.write_text(yeni_metin, encoding="utf-8")
        eklendi.append(ad)

    print(f"{'[KURU ÇALIŞMA] ' if kuru else ''}Türkçe tetikleyici yaması")
    print(f"  eklendi     : {len(eklendi)}")
    print(f"  zaten vardı : {len(atlandi)}")
    if bulunamadi:
        print(f"  BULUNAMADI  : {len(bulunamadi)}")
        for b in bulunamadi:
            print(f"     - {b}")
    if eklendi:
        print("\n  eklenenler:")
        for e in eklendi:
            print(f"     ✓ {e}")


def main():
    varsayilan_kural, varsayilan_skills = varsayilan_yollar()
    parser = argparse.ArgumentParser(description="Skill dosyalarına Türkçe tetikleyiciler ekler.")
    parser.add_argument("--kural", type=pathlib.Path, default=varsayilan_kural,
                        help="Tetikleyici kural markdown dosyası")
    parser.add_argument("--skills", type=pathlib.Path, default=varsayilan_skills,
                        help="Skill dizini")
    parser.add_argument("--kuru", "--dry-run", action="store_true",
                        help="Dosyaları değiştirmeden simüle et")
    args = parser.parse_args()

    uygula(kural_yol=args.kural, skills_yol=args.skills, kuru=args.kuru)


if __name__ == "__main__":
    main()
