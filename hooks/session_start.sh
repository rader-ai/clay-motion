#!/usr/bin/env bash
# SessionStart: find the pinned Blender env and record its path for bin/studio (ENGINEERING.md section 3).
# Fast check only (import + version); the full smoke test is `studio smoke`.
set -uo pipefail
PIN="5.2.2"
CANDIDATES=("${CLAUDE_PLUGIN_DATA:-/nonexistent}/bpy-$PIN" "$HOME/.local/share/clay-studio/bpy-$PIN")
for d in "${CANDIDATES[@]}"; do
  py="$d/bin/python"
  if [[ -x "$py" ]] && v="$("$py" -c 'import bpy; print(bpy.app.version_string)' 2>/dev/null)"; then
    mkdir -p "$HOME/.config/clay-studio"
    printf 'BPY_PYTHON=%s\nBPY_VERSION=%s\n' "$py" "$v" > "$HOME/.config/clay-studio/env"
    echo "clay-studio: Blender $v ready ($py)"
    exit 0
  fi
done
echo "clay-studio: pinned bpy $PIN not found. Install: python3.13 -m venv ~/.local/share/clay-studio/bpy-$PIN && ~/.local/share/clay-studio/bpy-$PIN/bin/pip install bpy==$PIN"
exit 0
