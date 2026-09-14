#!/usr/bin/env bash
# Ofis Şablonu Kurulum Betiği
#
# Çalışma ofisi dizin yapısını hazırlar, yerel becerileri kurar ve
# upstream.tsv içindeki dış bağımlılıkları bağlar.

set -euo pipefail

ZORLA=0
TURKCE=0

for arg in "$@"; do
  case "$arg" in
    --zorla)
      ZORLA=1
      ;;
    --turkce)
      TURKCE=1
      ;;
    -h|--help)
      echo "Kullanım: bash kur.sh [--zorla] [--turkce]"
      echo "  --zorla   Mevcut yerel becerilerin üzerine yazar"
      echo "  --turkce  Kurulum sonrası Türkçe tetikleyicileri uygular"
      exit 0
      ;;
    *)
      echo "Bilinmeyen parametre: $arg" >&2
      echo "Kullanım: bash kur.sh [--zorla] [--turkce]" >&2
      exit 1
      ;;
  esac
done

if ! command -v git >/dev/null 2>&1; then
  echo "HATA: git kurulu değil. Lütfen önce git paketini yükleyin." >&2
  exit 1
fi

KOK="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OFIS="${OFIS:-$HOME/ofis}"
CLAUDE_SKILLS="$HOME/.claude/skills"
AGENTS_SKILLS="$HOME/.agents/skills"
CLAUDE_AGENTS="$HOME/.claude/agents"
UPSTREAM_DIR="${OFIS}/.upstream"
UPSTREAM_TSV="${KOK}/upstream.tsv"

echo "==> 1. Çalışma ofisi dizinleri hazırlanıyor..."
mkdir -p "$OFIS/projeler" "$CLAUDE_SKILLS" "$AGENTS_SKILLS" "$CLAUDE_AGENTS" "$UPSTREAM_DIR"

for d in araclar sablonlar skill-gozlemleri; do
  if [ -d "$KOK/$d" ]; then
    mkdir -p "$OFIS/$d"
    cp -rn "$KOK/$d"/* "$OFIS/$d/" 2>/dev/null || true
  fi
done

if [ -f "$KOK/projeler/.gitkeep" ] && [ ! -f "$OFIS/projeler/.gitkeep" ]; then
  cp "$KOK/projeler/.gitkeep" "$OFIS/projeler/.gitkeep"
fi

echo "==> 2. Yerel beceriler kuruluyor..."
for s in "$KOK/skills"/*; do
  if [ -d "$s" ]; then
    ad="$(basename "$s")"
    hedef="$CLAUDE_SKILLS/$ad"
    if [ -e "$hedef" ] && [ "$ZORLA" -eq 0 ]; then
      echo "  - $ad zaten mevcut (atlandı, güncellemek için --zorla kullanın)"
    else
      rm -rf "$hedef"
      cp -r "$s" "$hedef"
      echo "  ✔ $ad kuruldu → $hedef"
    fi
  fi
done

echo "==> 3. Dış bağımlılıklar (upstream) çekiliyor ve bağlanıyor..."
if [ -f "$UPSTREAM_TSV" ]; then
  while IFS=$'\t' read -r ad url alt_yol lisans || [ -n "$ad" ]; do
    [[ "$ad" =~ ^#.*$ ]] && continue
    [ -z "$ad" ] && continue

    repo_dir="$UPSTREAM_DIR/$ad"
    if [ -d "$repo_dir/.git" ]; then
      echo "  ↻ Güncelleniyor: $ad..."
      git -C "$repo_dir" pull --quiet || true
    else
      echo "  ↓ Klonlanıyor: $ad ($url)..."
      git clone --depth 1 --quiet "$url" "$repo_dir"
    fi

    # Symlink becerileri
    if [ "$alt_yol" = "." ]; then
      if [ -f "$repo_dir/SKILL.md" ]; then
        ln -sfn "$repo_dir" "$CLAUDE_SKILLS/$ad"
        ln -sfn "$repo_dir" "$AGENTS_SKILLS/$ad"
        echo "    ✔ $ad bağlandı"
      fi
    elif [ -d "$repo_dir/$alt_yol" ]; then
      if [ -f "$repo_dir/$alt_yol/SKILL.md" ]; then
        skill_ad="$(basename "$alt_yol")"
        ln -sfn "$repo_dir/$alt_yol" "$CLAUDE_SKILLS/$skill_ad"
        ln -sfn "$repo_dir/$alt_yol" "$AGENTS_SKILLS/$skill_ad"
        echo "    ✔ $skill_ad bağlandı"
      else
        for alt_skill in "$repo_dir/$alt_yol"/*; do
          if [ -d "$alt_skill" ] && [ -f "$alt_skill/SKILL.md" ]; then
            skill_ad="$(basename "$alt_skill")"
            ln -sfn "$alt_skill" "$CLAUDE_SKILLS/$skill_ad"
            ln -sfn "$alt_skill" "$AGENTS_SKILLS/$skill_ad"
            echo "    ✔ $skill_ad bağlandı"
          fi
        done
      fi
    fi

    # Council veya diğer ajanları bağla
    if [ -d "$repo_dir/agents" ]; then
      for ajan in "$repo_dir/agents"/*.md; do
        if [ -f "$ajan" ]; then
          ln -sfn "$ajan" "$CLAUDE_AGENTS/$(basename "$ajan")"
        fi
      done
      echo "    ✔ ajanlar bağlandı (~/.claude/agents/)"
    fi
  done < "$UPSTREAM_TSV"
else
  echo "  ⚠ upstream.tsv bulunamadı, dış bağımlılıklar atlandı."
fi

if [ "$TURKCE" -eq 1 ]; then
  echo "==> 4. Türkçe tetikleyiciler uygulanıyor..."
  if [ -f "$OFIS/araclar/turkce-tetikleyiciler.py" ]; then
    python3 "$OFIS/araclar/turkce-tetikleyiciler.py" --skills "$CLAUDE_SKILLS"
  elif [ -f "$KOK/araclar/turkce-tetikleyiciler.py" ]; then
    python3 "$KOK/araclar/turkce-tetikleyiciler.py" --skills "$CLAUDE_SKILLS"
  else
    echo "  ⚠ turkce-tetikleyiciler.py bulunamadı."
  fi
fi

echo
echo "════════════════════════════════════════════════════════"
echo "  Kurulum başarıyla tamamlandı!"
echo "════════════════════════════════════════════════════════"
echo
echo "Çalışma Ofisi: $OFIS"
echo "Claude Becerileri: $CLAUDE_SKILLS"
echo
echo "Sıradaki adımlar:"
echo "1. Yeni proje başlatmak için Claude Code içinde '/yeni-proje' becerisini kullanabilirsiniz."
echo "2. Kurulum sağlığını denetlemek için: bash $OFIS/araclar/bakim.sh"
echo "3. İsteğe bağlı CLI araçları:"
echo "   - Antigravity CLI (agy): Google Antigravity dokümantasyonuna bakınız."
echo "   - Codex CLI (codex): OpenAI Codex dokümantasyonuna bakınız."
echo
