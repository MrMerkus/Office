#!/usr/bin/env bash
# Dış bağımlılık depolarını (upstream) çeker veya günceller.
#
# upstream.tsv dosyasını okuyarak depoları ${OFIS}/.upstream/ altına klonlar
# ve ilgili becerileri ~/.claude/skills ile ~/.agents/skills dizinlerine bağlar.

set -euo pipefail

OFIS="${OFIS:-$HOME/ofis}"
UPSTREAM_TSV="${UPSTREAM_TSV:-$OFIS/upstream.tsv}"
HEDEF="${OFIS}/.upstream"
CLAUDE_SKILLS="$HOME/.claude/skills"
AGENTS_SKILLS="$HOME/.agents/skills"
CLAUDE_AGENTS="$HOME/.claude/agents"

mkdir -p "$HEDEF" "$CLAUDE_SKILLS" "$AGENTS_SKILLS" "$CLAUDE_AGENTS"

if [ ! -f "$UPSTREAM_TSV" ]; then
  echo "HATA: upstream.tsv bulunamadı: $UPSTREAM_TSV" >&2
  exit 1
fi

listele() {
  printf '%-30s %-12s %s\n' "DEPO" "LİSANS" "ADRES"
  printf '%.0s─' {1..80}; echo
  while IFS=$'\t' read -r ad url alt_yol lisans || [ -n "$ad" ]; do
    [[ "$ad" =~ ^#.*$ ]] && continue
    [ -z "$ad" ] && continue
    printf '%-30s %-12s %s\n' "$ad" "$lisans" "$url"
  done < "$UPSTREAM_TSV"
}

bagla() {
  local ad="$1" alt_yol="$2"
  local repo_yol="$HEDEF/$ad"

  if [ ! -d "$repo_yol" ]; then
    return 0
  fi

  # Becerileri bağla
  if [ "$alt_yol" = "." ]; then
    if [ -f "$repo_yol/SKILL.md" ]; then
      ln -sfn "$repo_yol" "$CLAUDE_SKILLS/$ad"
      ln -sfn "$repo_yol" "$AGENTS_SKILLS/$ad"
      echo "     ✔ skill bağlandı: $ad"
    fi
  elif [ -d "$repo_yol/$alt_yol" ]; then
    if [ -f "$repo_yol/$alt_yol/SKILL.md" ]; then
      local skill_ad
      skill_ad="$(basename "$alt_yol")"
      ln -sfn "$repo_yol/$alt_yol" "$CLAUDE_SKILLS/$skill_ad"
      ln -sfn "$repo_yol/$alt_yol" "$AGENTS_SKILLS/$skill_ad"
      echo "     ✔ skill bağlandı: $skill_ad"
    else
      for alt_skill in "$repo_yol/$alt_yol"/*; do
        if [ -d "$alt_skill" ] && [ -f "$alt_skill/SKILL.md" ]; then
          local skill_ad
          skill_ad="$(basename "$alt_skill")"
          ln -sfn "$alt_skill" "$CLAUDE_SKILLS/$skill_ad"
          ln -sfn "$alt_skill" "$AGENTS_SKILLS/$skill_ad"
          echo "     ✔ alt skill bağlandı: $skill_ad"
        fi
      done
    fi
  fi

  # Konsey veya diğer ajanları bağla
  if [ -d "$repo_yol/agents" ]; then
    for ajan in "$repo_yol/agents"/*.md; do
      if [ -f "$ajan" ]; then
        ln -sfn "$ajan" "$CLAUDE_AGENTS/$(basename "$ajan")"
      fi
    done
    echo "     ✔ ajanlar bağlandı (~/.claude/agents/)"
  fi
}

getir() {
  local hedef_ad="$1" zorla_guncel="${2:-}" bulundu=0

  while IFS=$'\t' read -r ad url alt_yol lisans || [ -n "$ad" ]; do
    [[ "$ad" =~ ^#.*$ ]] && continue
    [ -z "$ad" ] && continue
    [ "$ad" != "$hedef_ad" ] && continue

    bulundu=1
    local repo_dir="$HEDEF/$ad"

    if [ -d "$repo_dir/.git" ]; then
      echo "  ↻ $ad güncelleniyor ($url)..."
      git -C "$repo_dir" pull --quiet || true
    else
      echo "  ↓ $ad klonlanıyor ($url)..."
      git clone --depth 1 --quiet "$url" "$repo_dir"
    fi

    bagla "$ad" "$alt_yol"
    return 0
  done < "$UPSTREAM_TSV"

  if [ "$bulundu" -eq 0 ]; then
    echo "  ✘ '$hedef_ad' kayıtlarda yok. Liste için: --liste" >&2
    return 1
  fi
}

case "${1:---liste}" in
  --liste|-l)
    listele
    ;;
  --hepsi)
    echo "Tüm upstream depoları çekiliyor..."
    while IFS=$'\t' read -r ad url alt_yol lisans || [ -n "$ad" ]; do
      [[ "$ad" =~ ^#.*$ ]] && continue
      [ -z "$ad" ] && continue
      getir "$ad"
    done < "$UPSTREAM_TSV"
    ;;
  --guncel)
    if [ -z "${2:-}" ]; then
      echo "Kullanım: --guncel <depo-adı>" >&2
      exit 1
    fi
    getir "$2" "guncel"
    ;;
  *)
    getir "$1"
    ;;
esac
