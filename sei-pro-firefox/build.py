#!/usr/bin/env python3
"""Converte o zip do SEI Pro Lab (Chrome, MV3) em um pacote para Firefox (MV3).

Uso: python3 build.py <sei-pro-X.Y.zip> [saida.xpi]

Nao altera o codigo da extensao alem de dois pontos, ambos verificados por assert:
  manifest.json  -> chaves exclusivas do Chrome trocadas pelos equivalentes do Firefox
  background.js  -> sidebarAction.open() ganha fallback (abre painel.html em aba)
"""
import json
import sys
import zipfile
from pathlib import Path

GECKO_ID = "sei-pro-lab@local"
MIN_FIREFOX = "128.0"  # sidebarAction.open, optional_host_permissions


def patch_manifest(raw: bytes) -> bytes:
    m = json.loads(raw)
    assert m["manifest_version"] == 3, "esperado manifest v3"

    # Chrome-only
    panel = m.pop("side_panel")["default_path"]
    m.pop("options_page", None)  # Firefox usa options_ui (ja presente)
    m["permissions"] = [p for p in m.get("permissions", []) if p != "sidePanel"]

    # Firefox MV3 nao tem service worker: usa event page.
    assert "service_worker" in m["background"]
    m["background"] = {"scripts": [m["background"]["service_worker"]]}

    # Painel lateral: equivalente Firefox do sidePanel.
    icons = m.get("icons", {})
    m["sidebar_action"] = {
        "default_title": "SEI Pro",
        "default_panel": panel,
        "default_icon": {k: v for k, v in icons.items() if k in ("16", "32")},
        "open_at_install": False,
    }

    # Firefox MV3 so injeta content scripts onde ha permissao de host.
    hosts = []
    for cs in m["content_scripts"]:
        for pat in cs.get("matches", []):
            if pat not in hosts:
                hosts.append(pat)
    m["host_permissions"] = hosts

    m["browser_specific_settings"] = {
        "gecko": {"id": GECKO_ID, "strict_min_version": MIN_FIREFOX}
    }
    return (json.dumps(m, indent=2, ensure_ascii=False) + "\n").encode()


def patch_background(raw: bytes) -> bytes:
    s = raw.decode()
    old = "browser.sidebarAction.open();"
    assert s.count(old) == 2, "background.js mudou: revisar patch"
    new = (
        'browser.sidebarAction.open().catch(function () { '
        'browser.tabs.create({ url: browser.runtime.getURL("html/painel.html") }); });'
    )
    return s.replace(old, new).encode()


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    src = Path(sys.argv[1])
    out = Path(sys.argv[2]) if len(sys.argv) > 2 else src.with_name(src.stem + "-firefox.xpi")
    with zipfile.ZipFile(src) as zin, zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zout:
        for info in zin.infolist():
            if info.is_dir():
                continue
            data = zin.read(info.filename)
            if info.filename == "manifest.json":
                data = patch_manifest(data)
            elif info.filename == "background.js":
                data = patch_background(data)
            elif info.filename == "jsconfig.json":
                continue
            zout.writestr(info.filename, data)
    print(out)


if __name__ == "__main__":
    main()
