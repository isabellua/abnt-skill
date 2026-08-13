#!/usr/bin/env python3
"""Gerador de documentos ABNT (.docx) — TCC, artigo, relatório
Normas: NBR 14724 (2011 + atualizações 2023), NBR 10520, NBR 6023, NBR 6024"""
import argparse, json, sys
from pathlib import Path

try:
    from docx import Document
    from docx.shared import Cm, Pt, RGBColor
    from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
    from docx.oxml.ns import qn
    from docx.oxml import OxmlElement
except ImportError:
    print("ERRO: python-docx não instalado. Execute: pip install python-docx")
    sys.exit(1)

FONTE = "Times New Roman"


# ── Configuração global ───────────────────────────────────────────────────────

def cfg_pagina(doc):
    s = doc.sections[0]
    s.top_margin = Cm(3)
    s.bottom_margin = Cm(2)
    s.left_margin = Cm(3)
    s.right_margin = Cm(2)
    s.page_height = Cm(29.7)
    s.page_width = Cm(21)


PRETO = RGBColor(0, 0, 0)


def cfg_normal(doc):
    e = doc.styles["Normal"]
    e.font.name = FONTE
    e.font.size = Pt(12)
    e.font.color.rgb = PRETO
    e.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    e.paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
    e.paragraph_format.first_line_indent = Cm(1.25)
    e.paragraph_format.space_before = Pt(0)
    e.paragraph_format.space_after = Pt(0)


def adicionar_numeracao_paginas(doc):
    """Adiciona numeração de página no canto superior direito, a 2 cm da margem."""
    section = doc.sections[0]
    header = section.header
    header.is_linked_to_previous = False

    # Limpa conteúdo atual do cabeçalho
    for p in header.paragraphs:
        for r in p.runs:
            r.text = ""

    if not header.paragraphs:
        header.add_paragraph()

    p = header.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)

    run = p.add_run()
    run.font.name = FONTE
    run.font.size = Pt(10)

    # Insere campo PAGE do Word (número de página automático)
    fldChar1 = OxmlElement("w:fldChar")
    fldChar1.set(qn("w:fldCharType"), "begin")
    instrText = OxmlElement("w:instrText")
    instrText.text = "PAGE"
    fldChar2 = OxmlElement("w:fldChar")
    fldChar2.set(qn("w:fldCharType"), "end")
    run._r.append(fldChar1)
    run._r.append(instrText)
    run._r.append(fldChar2)


# ── Helpers de parágrafo ──────────────────────────────────────────────────────

def para(doc, txt, bold=False, center=False, size=None, li=None,
         single=False, no_first=False, caps=False, left=False):
    pg = doc.add_paragraph()
    if center:
        pg.alignment = WD_ALIGN_PARAGRAPH.CENTER
    elif left:
        pg.alignment = WD_ALIGN_PARAGRAPH.LEFT
    else:
        pg.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    pf = pg.paragraph_format
    pf.line_spacing_rule = WD_LINE_SPACING.SINGLE if single else WD_LINE_SPACING.ONE_POINT_FIVE
    pf.space_before = pf.space_after = Pt(0)

    if li is not None:
        pf.left_indent = li
        pf.first_line_indent = Cm(0)
    elif no_first:
        pf.first_line_indent = Cm(0)
    else:
        pf.first_line_indent = Cm(1.25)

    r = pg.add_run(txt.upper() if caps else txt)
    r.font.name = FONTE
    r.font.size = size or Pt(12)
    r.font.bold = bold
    r.font.color.rgb = PRETO
    return pg


def titulo_secao(doc, num, t, nivel):
    """Formata títulos de seção conforme NBR 6024."""
    txt = f"{num} {t}".strip() if num else t
    pg = doc.add_paragraph()
    pg.alignment = WD_ALIGN_PARAGRAPH.LEFT
    pf = pg.paragraph_format
    pf.first_line_indent = Cm(0)
    pf.space_before = Pt(12)
    pf.space_after = Pt(6)
    pf.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE

    texto_formatado = txt.upper() if nivel <= 2 else txt
    r = pg.add_run(texto_formatado)
    r.font.name = FONTE
    r.font.size = Pt(12)
    r.font.bold = nivel in (1, 3)
    r.font.italic = nivel == 4
    r.font.color.rgb = PRETO


def citacao_longa(doc, txt, autor=""):
    """Formata citação direta longa: recuo 4 cm, fonte 10, espaço simples, sem aspas."""
    pg = doc.add_paragraph()
    pg.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    pf = pg.paragraph_format
    pf.left_indent = Cm(4)
    pf.first_line_indent = Cm(0)
    pf.line_spacing_rule = WD_LINE_SPACING.SINGLE
    pf.space_before = Pt(6)
    pf.space_after = Pt(6)
    conteudo = f"{txt} ({autor})" if autor else txt
    r = pg.add_run(conteudo)
    r.font.name = FONTE
    r.font.size = Pt(10)
    r.font.color.rgb = PRETO


def br(doc):
    pg = doc.add_paragraph()
    pg.paragraph_format.space_before = Pt(0)
    pg.paragraph_format.space_after = Pt(0)
    pg.paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE


def pb(doc):
    doc.add_page_break()


# ── Elementos pré-textuais ────────────────────────────────────────────────────

def gerar_capa(doc, c):
    """
    Capa NBR 14724: Instituição → Curso → Autor → Título → Subtítulo → Local/Ano.
    Todos centralizados, sem número de página visível.
    """
    para(doc, c.get("instituicao", "[INSTITUIÇÃO]"), center=True, caps=True, no_first=True)
    if c.get("curso"):
        para(doc, c["curso"], center=True, caps=True, no_first=True)
    br(doc)
    para(doc, c.get("autor", "[AUTOR]"), center=True, caps=True, no_first=True)
    for _ in range(6):
        br(doc)
    para(doc, c.get("titulo", "[TÍTULO]"), bold=True, center=True, caps=True, no_first=True)
    if c.get("subtitulo"):
        para(doc, c["subtitulo"], center=True, no_first=True)
    for _ in range(8):
        br(doc)
    para(doc, c.get("cidade", "[CIDADE]"), center=True, no_first=True)
    para(doc, str(c.get("ano", "[ANO]")), center=True, no_first=True)
    pb(doc)


def gerar_folha_rosto(doc, c):
    """
    Folha de rosto: dados da capa + natureza do trabalho recuada 7,5 cm,
    fonte 10, espaço simples (NBR 14724).
    """
    para(doc, c.get("autor", "[AUTOR]"), center=True, caps=True, no_first=True)
    for _ in range(4):
        br(doc)
    para(doc, c.get("titulo", "[TÍTULO]"), bold=True, center=True, caps=True, no_first=True)
    if c.get("subtitulo"):
        para(doc, c["subtitulo"], center=True, no_first=True)
    for _ in range(4):
        br(doc)

    grau = c.get("grau", "Bacharel")
    nota = (
        f"Trabalho de Conclusão de Curso apresentado ao Curso de {c.get('curso', '[CURSO]')},"
        f" da {c.get('instituicao', '[INSTITUIÇÃO]')},"
        f" como requisito parcial para obtenção do título de {grau}.\n"
        f"Orientador: {c.get('orientador', '[ORIENTADOR]')}"
    )
    # Recuo de 7,5 cm conforme NBR 14724
    pg = doc.add_paragraph()
    pg.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    pf = pg.paragraph_format
    pf.left_indent = Cm(7.5)
    pf.first_line_indent = Cm(0)
    pf.line_spacing_rule = WD_LINE_SPACING.SINGLE
    r = pg.add_run(nota)
    r.font.name = FONTE
    r.font.size = Pt(10)
    r.font.color.rgb = PRETO

    for _ in range(6):
        br(doc)
    para(doc, c.get("cidade", "[CIDADE]"), center=True, no_first=True)
    para(doc, str(c.get("ano", "[ANO]")), center=True, no_first=True)
    pb(doc)


def gerar_resumo(doc, c, idioma="pt"):
    """
    Resumo NBR 6028:
    - Título centralizado, maiúsculo, negrito, fonte 12
    - Texto em parágrafo único, espaço simples, sem recuo, 3ª pessoa singular
    - Palavras-chave separadas por ponto e vírgula
    """
    tit = "RESUMO" if idioma == "pt" else "ABSTRACT"
    campo_txt = "resumo" if idioma == "pt" else "abstract"
    campo_kw = "palavras_chave" if idioma == "pt" else "keywords"
    label = "Palavras-chave" if idioma == "pt" else "Keywords"

    para(doc, tit, bold=True, center=True, no_first=True, single=True)
    br(doc)
    # Texto sem recuo, espaço simples
    pg = doc.add_paragraph()
    pg.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    pf = pg.paragraph_format
    pf.first_line_indent = Cm(0)
    pf.line_spacing_rule = WD_LINE_SPACING.SINGLE
    pf.space_before = pf.space_after = Pt(0)
    r = pg.add_run(c.get(campo_txt, f"[{tit}]"))
    r.font.name = FONTE
    r.font.size = Pt(12)
    r.font.color.rgb = PRETO

    # Linha em branco com espaçamento 1,5 antes das palavras-chave
    br(doc)

    kws = c.get(campo_kw, [])
    if isinstance(kws, list):
        # Palavras-chave separadas por ponto e vírgula (NBR 6028)
        kws_str = "; ".join(kws)
    else:
        kws_str = kws

    pg = doc.add_paragraph()
    pg.alignment = WD_ALIGN_PARAGRAPH.LEFT
    pf = pg.paragraph_format
    pf.first_line_indent = Cm(0)
    pf.line_spacing_rule = WD_LINE_SPACING.SINGLE
    pf.space_before = pf.space_after = Pt(0)
    rl = pg.add_run(f"{label}: ")
    rl.bold = True
    rl.font.name = FONTE
    rl.font.size = Pt(12)
    rl.font.color.rgb = PRETO
    rt = pg.add_run(kws_str)
    rt.font.name = FONTE
    rt.font.size = Pt(12)
    rt.font.color.rgb = PRETO

    pb(doc)


def gerar_sumario(doc, secs):
    """
    Sumário NBR 6027: não lista pré-textuais (resumo, abstract etc.).
    Reflete exatamente os títulos e numeração do texto.
    """
    para(doc, "SUMÁRIO", bold=True, center=True, no_first=True)
    br(doc)
    for s in secs:
        num = s.get("numero", "")
        tit = s.get("titulo", "")
        pag = s.get("pagina", "X")
        nivel = s.get("nivel", 1)

        if nivel <= 2:
            texto = f"{num} {tit.upper()}".strip() if num else tit.upper()
        else:
            texto = f"{num} {tit}".strip() if num else tit

        pg = doc.add_paragraph()
        pg.alignment = WD_ALIGN_PARAGRAPH.LEFT
        pf = pg.paragraph_format
        pf.first_line_indent = Cm(0)
        pf.left_indent = Cm((nivel - 1) * 0.5)
        pf.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
        pf.space_before = pf.space_after = Pt(0)
        r = pg.add_run(f"{texto}\t{pag}")
        r.font.name = FONTE
        r.font.size = Pt(12)
        r.font.bold = nivel in (1, 3)
        r.font.color.rgb = PRETO
        pf.tab_stops.add_tab_stop(Cm(15.5))

    pb(doc)


# ── Elementos textuais ────────────────────────────────────────────────────────

def _renderizar_secao(doc, s):
    """Renderiza o conteúdo de uma seção (título + parágrafos + citações longas)."""
    nivel = s.get("nivel", 1)
    num = s.get("numero", "")
    tit = s.get("titulo", "")
    cont = s.get("conteudo", "")
    citacoes = s.get("citacoes_longas", [])

    titulo_secao(doc, num, tit, nivel)

    if isinstance(cont, list):
        for txt in cont:
            if txt.strip():
                para(doc, txt)
    elif cont:
        para(doc, cont)

    for cit in citacoes:
        citacao_longa(doc, cit.get("texto", ""), cit.get("autor", ""))

    br(doc)


def gerar_secoes(doc, secs):
    """
    Gera seções textuais com formatação NBR 6024.
    Cada seção primária (nível 1) inicia em nova página — a quebra é inserida
    ao final da seção anterior, não no início da próxima, para evitar páginas
    em branco entre o sumário e a primeira seção.
    """
    # Agrupa seções em blocos encabeçados por uma seção primária
    grupos = []
    grupo_atual = []
    for s in secs:
        if s.get("nivel", 1) == 1 and grupo_atual:
            grupos.append(grupo_atual)
            grupo_atual = []
        grupo_atual.append(s)
    if grupo_atual:
        grupos.append(grupo_atual)

    for i, grupo in enumerate(grupos):
        # A quebra de página vai no FINAL de cada grupo primário, exceto o último
        # (o último é separado das referências pelo pb() dentro de gerar_referencias)
        for s in grupo:
            _renderizar_secao(doc, s)
        if i < len(grupos) - 1:
            pb(doc)


# ── Elementos pós-textuais ────────────────────────────────────────────────────

def gerar_referencias(doc, refs):
    """
    Referências NBR 6023: alinhamento esquerdo, espaço simples,
    linha em branco entre entradas, ordem alfabética.
    """
    pb(doc)
    para(doc, "REFERÊNCIAS", bold=True, left=True, no_first=True)
    br(doc)
    for ref in refs:
        pg = doc.add_paragraph()
        pg.alignment = WD_ALIGN_PARAGRAPH.LEFT
        pf = pg.paragraph_format
        pf.first_line_indent = Cm(0)
        pf.line_spacing_rule = WD_LINE_SPACING.SINGLE
        pf.space_before = Pt(0)
        pf.space_after = Pt(6)
        r = pg.add_run(ref)
        r.font.name = FONTE
        r.font.size = Pt(12)
        r.font.color.rgb = PRETO


def gerar_apendice_anexo(doc, itens, tipo="APÊNDICE"):
    """Apêndices/Anexos: paginação contínua, numerados com algarismos arábicos."""
    for i, item in enumerate(itens, 1):
        pb(doc)
        rotulo = f"{tipo} {i} — {item.get('titulo', '')}"
        para(doc, rotulo, bold=True, center=True, caps=True, no_first=True)
        br(doc)
        cont = item.get("conteudo", "")
        if cont:
            para(doc, cont)


# ── Gerador principal ─────────────────────────────────────────────────────────

def gerar(tipo, c, saida):
    doc = Document()
    cfg_pagina(doc)
    cfg_normal(doc)
    adicionar_numeracao_paginas(doc)

    # Remove parágrafo em branco inicial gerado pelo python-docx
    for pg in doc.paragraphs:
        pg._element.getparent().remove(pg._element)

    # Pré-textuais
    if tipo in ("tcc", "relatorio"):
        gerar_capa(doc, c)
    if tipo == "tcc":
        gerar_folha_rosto(doc, c)
        gerar_resumo(doc, c, "pt")
        if c.get("abstract") or c.get("keywords"):
            gerar_resumo(doc, c, "en")
    if c.get("sumario"):
        gerar_sumario(doc, c["sumario"])

    # Textuais
    if c.get("secoes"):
        gerar_secoes(doc, c["secoes"])

    # Pós-textuais
    if c.get("referencias"):
        gerar_referencias(doc, c["referencias"])
    if c.get("apendices"):
        gerar_apendice_anexo(doc, c["apendices"], "APÊNDICE")
    if c.get("anexos"):
        gerar_apendice_anexo(doc, c["anexos"], "ANEXO")

    doc.save(saida)
    print(f"Documento gerado: {saida}")


def main():
    ap = argparse.ArgumentParser(description="Gerador de documentos ABNT (.docx)")
    ap.add_argument("--tipo", choices=["tcc", "artigo", "relatorio"], default="tcc",
                    help="Tipo de documento")
    ap.add_argument("--config", required=True, help="Caminho para o arquivo config.json")
    ap.add_argument("--saida", default="documento_abnt.docx", help="Nome do arquivo de saída")
    args = ap.parse_args()

    with open(args.config, encoding="utf-8") as f:
        c = json.load(f)
    gerar(args.tipo, c, args.saida)


if __name__ == "__main__":
    main()
