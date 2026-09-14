#!/usr/bin/env bash
# Çalışma ofisi ve kurulum haritasının sağlık kontrolü.
#
# Symlink'ler, harici komutlar ve isteğe bağlı hafıza kancaları kontrol edilir.

set -euo pipefail

CONFIG_FILE="$HOME/.config/my-ai-system/sistem.json"
if [ -f "$CONFIG_FILE" ]; then
  if [ -z "${OFIS:-}" ]; then
    OFIS="$(python3 -c "import json; d=json.load(open('$CONFIG_FILE', encoding='utf-8')); print(d.get('ofis') or '')" 2>/dev/null || true)"
  fi
  if [ -z "${HAFIZA:-}" ]; then
    HAFIZA="$(python3 -c "import json; d=json.load(open('$CONFIG_FILE', encoding='utf-8')); print(d.get('hafiza') or '')" 2>/dev/null || true)"
  fi
fi
OFIS="${OFIS:-$HOME/ofis}"
HAFIZA="${HAFIZA:-}"
export OFIS
export HAFIZA
CLAUDE_DIR="$HOME/.claude"
AGENTS_DIR="$HOME/.agents"

kirik=0
saglam=0

kontrol() {
  local yol="$1"
  if [ -L "$yol" ]; then
    if [ -e "$yol" ]; then
      saglam=$((saglam + 1))
    else
      printf '  ✘ KIRIK  %-32s → %s\n' "$(basename "$yol")" "$(readlink "$yol")"
      kirik=$((kirik + 1))
    fi
  fi
}

echo "═══ SYMLINK KONTROLÜ ═══"
for d in "$OFIS" "$OFIS/araclar" "$OFIS/projeler" "$CLAUDE_DIR/skills" "$AGENTS_DIR/skills" "$CLAUDE_DIR/agents"; do
  if [ -d "$d" ]; then
    for yol in "$d"/*; do
      [ -e "$yol" ] || [ -L "$yol" ] && kontrol "$yol"
    done
  fi
done
echo "  sağlam: $saglam · kırık: $kirik"

echo
echo "═══ KOMUTLAR PATH'TE Mİ ═══"
for t in codeburn yt-dlp pdf2md skillui agy codex; do
  if command -v "$t" >/dev/null 2>&1; then
    printf '  ✔ %-10s %s\n' "$t" "$(command -v "$t")"
  else
    printf '  - %-10s (kurulu değil / opsiyonel)\n' "$t"
  fi
done

echo
echo "═══ YAPILANDIRMA DİZİNLERİ ═══"
for d in "$HOME/.config/codeburn" "$HOME/.config/last30days" "$HOME/.impeccable"; do
  ad="$(basename "$d")"
  if [ -d "$d" ]; then
    printf '  ✔ %-16s mevcut: %s\n' "$ad" "$d"
  fi
done

echo
echo "═══ HAFIZA SİSTEMİ VE KANCALAR ═══"
if [ -n "$HAFIZA" ] && [ -f "$HAFIZA/.claude/settings.json" ]; then
  python3 - <<PY
import json
import os
from pathlib import Path

p = Path(os.environ["HAFIZA"]) / ".claude/settings.json"
try:
    d = json.loads(p.read_text(encoding="utf-8"))
    hooks_dict = d.get("hooks", {})
    n = sum(len(t.get("hooks", [])) for l in hooks_dict.values() for t in l)
    print(f"  {n} kanca kayıtlı", "✔" if n >= 5 else "⚠")
    for olay, l in hooks_dict.items():
        for t in l:
            for h in t.get("hooks", []):
                cmd = h.get("command", "").split("/")[-1].rstrip('"')
                print(f"    {olay}: {cmd}")
except Exception as e:
    print(f"  Hata: {e}")
PY
else
  echo "  Hafıza sistemi (\$HAFIZA) tanımlı değil veya ayar dosyası yok; atlandı."
fi

echo
if [ "$kirik" -eq 0 ]; then
  echo "SONUÇ: Bütün sembolik bağlar sağlam."
else
  echo "SONUÇ: $kirik kırık bağlantı var, yukarıdaki listeyi inceleyin."
fi

exit 0
