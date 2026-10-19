# SEI Pro Lab para Firefox

    python3 build.py sei-pro-3.8.zip sei-pro-3.8-firefox.xpi

Troca no `manifest.json`: `service_worker` por `background.scripts`, `side_panel`/`sidePanel` por
`sidebar_action`, remove `options_page`, adiciona `browser_specific_settings.gecko` (id, Firefox >= 128) e
`host_permissions` (união dos `matches` dos content scripts). Em `background.js`, `sidebarAction.open()` ganha
fallback que abre `painel.html` em aba.

## Instalar

- Temporário (some ao fechar o Firefox): `about:debugging#/runtime/this-firefox` > Carregar extensão temporária > escolher o `.xpi`.
- Permanente: Firefox comum só aceita extensão assinada. Opções: assinar como "não listada" em
  addons.mozilla.org, ou usar Developer Edition/Nightly/ESR com `xpinstall.signatures.required = false`.

## Não testado

Validado só com `web-ext lint` (0 erros). Nunca rodou contra uma instância real do SEI no Firefox.
Pontos de risco: abrir o painel lateral a partir do botão na barra do SEI (exige gesto do usuário),
rotinas agendadas do Agente (event page do Firefox descarrega), e backup em arquivo
(`showSaveFilePicker` não existe no Firefox; o código detecta e deve desativar).
