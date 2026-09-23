#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gera o Catálogo Completo Dent Med (A4, PDF) a partir de completo_data.py.

Uso:
    python3 build_completo.py
    # -> catalogo_dentmed_completo.pdf (e os HTMLs intermediários em build/)

Imagem de cada seção: se existir assets/sections/<key>.(jpg|png|webp), ela é
usada; senão, a foto indicada em "img" (assets/products/); senão, o quadro
fica como espaço reservado ("Espaço para imagem").

Requer Node com o pacote "playwright" (Chromium) e o pacote Python "pypdf".
"""
import base64, html, json, os, re, subprocess, sys

import build_catalog as bc
from completo_data import SECTIONS, POPDENT, POPDENT_SHADES, POPDENT_IDS

BASE = bc.BASE
BUILD = os.path.join(BASE, "build")
SECTION_IMG_DIR = os.path.join(BASE, "assets", "sections")
OUT_PDF = os.path.join(BASE, "catalogo_dentmed_completo.pdf")

PLACEHOLDER_ICON = {
    "isolamento": "instruments", "orto": "denture", "radiologia": "vitals",
    "equipamentos": "vitals",
}

esc = html.escape


def data_uri(path):
    return f"data:image/{bc.mime_for(path)};base64," + base64.b64encode(open(path, "rb").read()).decode()


def section_image(sec):
    for ext in bc.PHOTO_EXTS:
        p = os.path.join(SECTION_IMG_DIR, sec["key"] + ext)
        if os.path.isfile(p):
            return p
    if sec.get("img"):
        p = os.path.join(bc.PRODUCTS_DIR, sec["img"])
        if os.path.isfile(p):
            return p
    return None


def families(sec):
    return [g for g in sec["items"] if isinstance(g, dict) or g == "POPDENT"]


def stock_lines(sec):
    n = 0
    for g in sec["items"]:
        if g == "POPDENT":
            n += len(POPDENT_IDS)
        elif isinstance(g, dict):
            n += len(g["ids"])
    return n


# ---------------------------------------------------------------------------
CSS = """
* { box-sizing: border-box; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
:root {
  --green: #5BAE7E; --green-dark: #3E8A61; --green-light: #E7F4EC; --green-line: #CFE7D8;
  --ink: #2C2C2C; --body: #55575A; --muted: #8B8B8B; --paper: #FFFFFF; --line: #E3E1DC;
}
html, body { margin: 0; padding: 0; background: var(--paper); }
body { font-family: 'Liberation Sans', 'DejaVu Sans', sans-serif; color: var(--body); font-size: 8.5pt; }

/* ---------- body pages ---------- */
.sec { margin: 0 0 5mm 0; }
.keep { break-inside: avoid; }
.sec-head {
  display: flex; gap: 6mm; align-items: stretch;
  background: var(--green-light); border-radius: 3.5mm; padding: 3mm; margin-bottom: 2.6mm;
}
.sec-img {
  width: 54mm; height: 34mm; flex-shrink: 0; border-radius: 2.5mm; background: #fff;
  display: flex; align-items: center; justify-content: center; overflow: hidden; padding: 2mm;
}
.sec-img img { max-width: 100%; max-height: 100%; object-fit: contain; }
.sec-img.ph { border: 1.4px dashed #9CCBB0; flex-direction: column; gap: 2mm; color: var(--green-dark); }
.sec-img.ph svg { width: 13mm; height: 13mm; opacity: .75; }
.sec-img.ph span { font-size: 7.5pt; letter-spacing: 1.2px; text-transform: uppercase; font-weight: 700; opacity: .8; }
.sec-text { display: flex; flex-direction: column; justify-content: center; padding-right: 2mm; }
.sec-eyebrow { font-size: 7.5pt; letter-spacing: 2px; font-weight: 700; color: var(--green-dark); margin-bottom: 1.5mm; }
.sec-text h1 { font-size: 18pt; line-height: 1.1; color: var(--ink); margin: 0 0 1.8mm 0; }
.sec-text p { font-size: 8.8pt; line-height: 1.4; margin: 0 0 1.8mm 0; }
.sec-meta { font-size: 7.5pt; color: var(--muted); letter-spacing: .3px; }
.sec-meta b { color: var(--green-dark); }

.sub {
  font-size: 9pt; font-weight: 700; color: var(--green-dark); text-transform: uppercase; letter-spacing: 1.4px;
  margin: 1.5mm 0 2mm 0; padding-bottom: 1mm; border-bottom: 1.5px solid var(--green-line);
}
.row { display: flex; gap: 2.6mm; margin-bottom: 2.6mm; }
.row > .card { flex: 1 1 0; min-width: 0; }
.row.one > .card.half { flex: 0 0 calc(50% - 1.3mm); }
.card {
  border: 1px solid var(--line); border-radius: 2.5mm; padding: 2.2mm 3mm 2.4mm 3mm; background: #fff;
  border-left: 2.2px solid var(--green);
}
.c-name { font-size: 9.4pt; font-weight: 700; color: var(--ink); line-height: 1.25; margin: 0 0 .9mm 0; }
.c-brand { font-size: 7pt; font-weight: 700; color: var(--green-dark); letter-spacing: .6px; text-transform: uppercase; margin: 0 0 .9mm 0; }
.c-pres { font-size: 7.8pt; color: var(--body); margin: 0 0 .6mm 0; }
.vars { margin-top: 1.3mm; display: flex; flex-direction: column; gap: 1mm; }
.var { display: flex; gap: 2mm; align-items: baseline; }
.var-l { font-size: 7pt; font-weight: 700; color: var(--muted); text-transform: uppercase; letter-spacing: .4px; flex: 0 0 21mm; line-height: 1.3; }
.wide .var-l { flex-basis: 18mm; }
.chips { display: flex; flex-wrap: wrap; gap: 1mm; }
.chip {
  font-size: 7.4pt; line-height: 1; color: var(--ink); background: var(--green-light);
  border: 1px solid var(--green-line); border-radius: 1.2mm; padding: .8mm 1.5mm; white-space: nowrap;
}

/* popdent matrix */
.pd-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 3mm 5mm; margin-top: 2mm; }
.pd h4 { font-size: 8pt; color: var(--ink); margin: 0 0 1mm 0; }
.pd h4 span { font-weight: 400; color: var(--muted); }
.pd table { width: 100%; border-collapse: collapse; font-size: 7.3pt; }
.pd th, .pd td { text-align: center; padding: .55mm 0; border-bottom: 1px solid #EFEDE8; }
.pd th { color: var(--muted); font-weight: 700; font-size: 6.8pt; }
.pd td.m { text-align: left; font-weight: 700; color: var(--ink); padding-left: 1mm; }
.pd .dot { display: inline-block; width: 2.2mm; height: 2.2mm; border-radius: 50%; background: var(--green); }
.pd-legend { font-size: 7pt; color: var(--muted); margin-top: 1.6mm; }

/* ---------- cover / back ---------- */
.page { width: 210mm; height: 297mm; position: relative; overflow: hidden; break-after: page; }
.page:last-child { break-after: auto; }
.cover, .back { background: linear-gradient(160deg, #7b7b7b 0%, #8b8b8b 55%, #6e6e6e 100%); color: #fff; }
.cover { display: flex; flex-direction: column; }
.cover-top { padding: 22mm 20mm 0 20mm; }
.cover-eyebrow { text-transform: uppercase; letter-spacing: 3px; font-size: 10pt; font-weight: 700; color: var(--green-light); margin-bottom: 6mm; }
.cover-logo { width: 120mm; }
.cover-title { font-size: 25pt; font-weight: 700; line-height: 1.25; margin: 9mm 20mm 3mm 20mm; }
.cover-sub { font-size: 11pt; color: #EFEFEF; margin: 0 20mm; max-width: 150mm; line-height: 1.5; }
.cover-index {
  margin: 9mm 20mm 0 20mm; background: rgba(255,255,255,.08);
  border: 1px solid rgba(255,255,255,.25); border-radius: 4mm; padding: 6mm 9mm;
}
.cover-index-title { font-size: 9pt; letter-spacing: 2px; text-transform: uppercase; color: var(--green-light); font-weight: 700; margin-bottom: 3mm; }
.cover-index ol { columns: 2; column-gap: 10mm; margin: 0; padding: 0; list-style: none; }
.cover-index li { font-size: 9.6pt; padding: 1.35mm 0; border-bottom: 1px solid rgba(255,255,255,.15); display: flex; gap: 2.5mm; break-inside: avoid; }
.cover-index li .n { color: var(--green-light); font-weight: 700; min-width: 5.5mm; }
.cover-index li .t { flex: 1; }
.cover-index li .p { color: var(--green-light); font-weight: 700; }
.cover-bottom {
  margin-top: auto; background: rgba(0,0,0,.18); padding: 6mm 20mm; font-size: 9.2pt;
  border-top: 1px solid rgba(255,255,255,.15); display: flex; flex-direction: column; gap: 1.3mm;
}
.cover-bottom b { color: var(--green-light); }
.back { display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; gap: 8mm; }
.back img { width: 30mm; }
.back h2 { font-size: 20pt; margin: 0; }
.back p { font-size: 11pt; color: #EFEFEF; margin: 0; max-width: 120mm; line-height: 1.5; }
.back .contact { margin-top: 6mm; font-size: 11pt; line-height: 1.6; }
.back .contact b { color: var(--green-light); }
"""


def chips(values):
    return "".join(f'<span class="chip">{esc(v)}</span>' for v in values.split("|"))


def card(g, cls=""):
    parts = [f'<div class="card {cls}">',
             f'<p class="c-name">{esc(g["n"])}</p>',
             f'<p class="c-brand">{esc(g["b"])}</p>']
    if g["p"]:
        parts.append(f'<p class="c-pres">{esc(g["p"])}</p>')
    if g["v"]:
        parts.append('<div class="vars">')
        for label, values in g["v"]:
            parts.append(f'<div class="var"><div class="var-l">{esc(label)}</div><div class="chips">{chips(values)}</div></div>')
        parts.append('</div>')
    parts.append('</div>')
    return "".join(parts)


def popdent_card():
    blocks = []
    for title, pack, molds in POPDENT:
        head = "".join(f"<th>{s}</th>" for s in POPDENT_SHADES)
        rows = []
        for mold in sorted(molds, key=lambda m: (not m[0].isdigit(), m)):
            have = set(molds[mold].split())
            cells = "".join(f'<td>{"<span class=dot></span>" if s in have else ""}</td>' for s in POPDENT_SHADES)
            rows.append(f'<tr><td class="m">{esc(mold)}</td>{cells}</tr>')
        blocks.append(f'<div class="pd"><h4>{esc(title)} <span>· {esc(pack)}</span></h4>'
                      f'<table><tr><th style="text-align:left;padding-left:1mm">Molde</th>{head}</tr>{"".join(rows)}</table></div>')
    return ('<div class="card wide">'
            '<p class="c-name">Dente Artificial Popdent</p>'
            '<p class="c-brand">Vipi · Dentbras</p>'
            '<p class="c-pres">Dentes de estoque em resina acrílica — moldes e cores disponíveis:</p>'
            f'<div class="pd-grid">{"".join(blocks)}</div>'
            '<p class="pd-legend">Cores (escala Popdent): 60 · 62 · 66 · 67 · 69 · BL2 (bleach). '
            '<span class="dot" style="display:inline-block;width:2mm;height:2mm;border-radius:50%;background:#5BAE7E;vertical-align:middle"></span> = disponível.</p>'
            '</div>')


def rows_for(items):
    """Pair cards two per row; wide cards and subtitles break the pairing.
    Returns a list of (html, is_sub) blocks."""
    out, pending = [], []

    def flush():
        if pending:
            cls = "row" if len(pending) == 2 else "row one"
            cards = "".join(card(g, "" if len(pending) == 2 else "half") for g in pending)
            out.append((f'<div class="{cls}">{cards}</div>', False))
            pending.clear()

    for g in items:
        if g == "POPDENT":
            flush()
            out.append((f'<div class="row">{popdent_card()}</div>', False))
        elif isinstance(g, tuple):
            flush()
            out.append((f'<div class="sub">{esc(g[1])}</div>', True))
        elif g["w"]:
            flush()
            out.append((f'<div class="row">{card(g, "wide")}</div>', False))
        else:
            pending.append(g)
            if len(pending) == 2:
                flush()
    flush()
    return out


def section_html(i, sec):
    img = section_image(sec)
    if img:
        box = f'<div class="sec-img"><img src="{data_uri(img)}"/></div>'
    else:
        ic = bc.icon(PLACEHOLDER_ICON.get(sec["key"], "instruments"), 13)
        box = f'<div class="sec-img ph">{ic}<span>Espaço para imagem</span></div>'
    fam = len(families(sec))
    head = (f'<div class="sec-head">{box}<div class="sec-text">'
            f'<div class="sec-eyebrow">SEÇÃO {i:02d}</div>'
            f'<h1>{esc(sec["title"])}</h1><p>{esc(sec["intro"])}</p>'
            f'<div class="sec-meta"><b>{fam}</b> {"família" if fam == 1 else "famílias"} de produtos · '
            f'<b>{stock_lines(sec)}</b> itens em estoque</div>'
            f'</div></div>')
    blocks = rows_for(sec["items"])
    # Keep the header together with the first row, and each subtitle with the row after it.
    out, k = [], 0
    first = [head]
    while k < len(blocks):
        first.append(blocks[k][0])
        k += 1
        if not blocks[k - 1][1]:
            break
    out.append(f'<div class="keep">{"".join(first)}</div>')
    while k < len(blocks):
        h, is_sub = blocks[k]
        if is_sub and k + 1 < len(blocks):
            out.append(f'<div class="keep">{h}{blocks[k + 1][0]}</div>')
            k += 2
        else:
            out.append(f'<div class="keep">{h}</div>')
            k += 1
    return f'<section class="sec">{"".join(out)}</section>'


def doc(body, margin="0", title="Dent Med — Catálogo Completo"):
    return (f'<!DOCTYPE html><html lang="pt-BR"><head><meta charset="utf-8"/><title>{title}</title>'
            f'<style>@page {{ size: A4; margin: {margin}; }}{CSS}</style></head><body>{body}</body></html>')


def cover_html(pages):
    total = sum(len(families(s)) for s in SECTIONS)
    idx = "".join(
        f'<li><span class="n">{i:02d}</span><span class="t">{esc(s["title"])}</span>'
        f'<span class="p">{pages.get(i, "")}</span></li>'
        for i, s in enumerate(SECTIONS, 1))
    return f"""
<div class="page cover">
  <div class="cover-top">
    <div class="cover-eyebrow">Catálogo Completo · Setembro 2026</div>
    <img class="cover-logo" src="data:image/png;base64,{bc.LOGO_FULL}"/>
  </div>
  <div class="cover-title">Produtos odontológicos<br/>e hospitalares</div>
  <div class="cover-sub">Todo o nosso estoque organizado por setor, com {total} famílias de produtos —
  itens iguais em cores, tamanhos e numerações diferentes aparecem juntos.</div>
  <div class="cover-index">
    <div class="cover-index-title">Setores · página</div>
    <ol>{idx}</ol>
  </div>
  <div class="cover-bottom">
    <div><b>Dent Med</b> — Produtos Odontológicos e Hospitalares</div>
    <div>Quadra 3 Conjunto A, Lote 41 - Loja 1, Planaltina/DF &nbsp;·&nbsp; Tel. (61) 3600-0140</div>
  </div>
</div>"""


def back_html():
    return f"""
<div class="page back">
  <img src="data:image/png;base64,{bc.TOOTH}"/>
  <h2>Vamos atender o seu consultório</h2>
  <p>Fale com a nossa equipe para orçamentos, condições especiais e disponibilidade atualizada do estoque.</p>
  <div class="contact"><b>(61) 3600-0140</b><br/>Quadra 3 Conjunto A, Lote 41 - Loja 1 — Planaltina/DF</div>
</div>"""


HEADER = f"""
<div style="width:100%;margin:0 16mm;padding:0 0 2.2mm 0;border-bottom:1.5px solid #5BAE7E;display:flex;
            justify-content:space-between;align-items:center;font-family:'Liberation Sans',sans-serif;
            -webkit-print-color-adjust:exact;">
  <div style="display:flex;align-items:center;gap:2mm;">
    <img src="data:image/png;base64,{bc.TOOTH}" style="height:6mm"/>
    <span style="font-family:'Liberation Serif',serif;font-size:10.5pt;letter-spacing:1px;color:#2C2C2C">DENT<b style="color:#3E8A61">·</b>MED</span>
  </div>
  <span style="font-size:7pt;letter-spacing:1.5px;text-transform:uppercase;color:#8B8B8B">Catálogo de Produtos</span>
</div>"""

FOOTER = """
<div style="width:100%;margin:0 16mm;padding-top:2mm;border-top:1px solid #E3E1DC;display:flex;
            justify-content:space-between;font-family:'Liberation Sans',sans-serif;font-size:7pt;color:#8B8B8B;">
  <span>Dent Med · Produtos Odontológicos e Hospitalares · (61) 3600-0140</span>
  <span style="font-weight:700;color:#3E8A61"><span class="pageNumber"></span></span>
</div>"""

RENDER_JS = r"""
const { chromium } = require('playwright');
const jobs = JSON.parse(process.argv[2]);
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  for (const j of jobs) {
    await page.goto('file://' + j.html, { waitUntil: 'load' });
    const opts = { path: j.pdf, format: 'A4', printBackground: true,
                   margin: { top: 0, bottom: 0, left: 0, right: 0 } };
    if (j.header) {
      Object.assign(opts, { displayHeaderFooter: true, headerTemplate: j.header, footerTemplate: j.footer,
                            margin: { top: '19mm', bottom: '15mm', left: '16mm', right: '16mm' } });
    }
    await page.pdf(opts);
  }
  await browser.close();
})();
"""


def render(jobs):
    js = os.path.join(BUILD, "render_jobs.js")
    open(js, "w").write(RENDER_JS)
    env = dict(os.environ)
    try:
        env["NODE_PATH"] = subprocess.check_output(["npm", "root", "-g"], text=True).strip()
    except Exception:
        pass
    subprocess.run(["node", js, json.dumps(jobs)], check=True, env=env)


def main():
    from pypdf import PdfReader, PdfWriter
    os.makedirs(BUILD, exist_ok=True)
    body = "".join(section_html(i, s) for i, s in enumerate(SECTIONS, 1))
    p_body = os.path.join(BUILD, "miolo.html")
    open(p_body, "w", encoding="utf-8").write(doc(body, margin="19mm 16mm 15mm 16mm"))
    render([dict(html=p_body, pdf=os.path.join(BUILD, "miolo.pdf"), header=HEADER, footer=FOOTER)])

    # Page of each section (footer numbering starts at 1 on the first inner page).
    pages = {}
    for pno, pg in enumerate(PdfReader(os.path.join(BUILD, "miolo.pdf")).pages, 1):
        for m in re.finditer(r"SEÇÃO(\d\d)", re.sub(r"\s+", "", pg.extract_text() or "")):
            pages.setdefault(int(m.group(1)), pno)
    missing = [i for i in range(1, len(SECTIONS) + 1) if i not in pages]
    if missing:
        sys.exit(f"could not locate sections {missing} in the rendered PDF")

    p_cover = os.path.join(BUILD, "capa.html")
    open(p_cover, "w", encoding="utf-8").write(doc(cover_html(pages) + back_html()))
    render([dict(html=p_cover, pdf=os.path.join(BUILD, "capa.pdf"))])

    cover = PdfReader(os.path.join(BUILD, "capa.pdf"))
    inner = PdfReader(os.path.join(BUILD, "miolo.pdf"))
    w = PdfWriter()
    w.add_page(cover.pages[0])
    for pg in inner.pages:
        w.add_page(pg)
    w.add_page(cover.pages[1])
    w.add_metadata({"/Title": "Dent Med — Catálogo Completo de Produtos"})
    with open(OUT_PDF, "wb") as f:
        w.write(f)
    fams = sum(len(families(s)) for s in SECTIONS)
    print(f"wrote {OUT_PDF}: {len(inner.pages) + 2} pages, {len(SECTIONS)} sections, {fams} families")
    print("section pages:", pages)


if __name__ == "__main__":
    main()
