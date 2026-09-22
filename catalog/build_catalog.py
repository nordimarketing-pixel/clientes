#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Builds the Dent Med A4 product catalog (HTML -> print to PDF).

Usage:
    python3 build_catalog.py
    # then render catalogo_dentmed.html -> PDF, see render.js / README.md

Adding real product photos:
    Drop an image into assets/products/<slug>.jpg (or .png/.webp), where
    <slug> is the product name run through slugify() below (lowercase,
    accents stripped, spaces/punctuation -> "-"). If a matching file exists,
    it is embedded instead of the line-icon. See README.md for the full
    list of slugs and suggested search terms per category.
"""
import base64, html, os, re, unicodedata

BASE = os.path.dirname(os.path.abspath(__file__))
PRODUCTS_DIR = os.path.join(BASE, "assets", "products")
PHOTO_EXTS = [".jpg", ".jpeg", ".png", ".webp"]

def b64(path):
    return base64.b64encode(open(os.path.join(BASE, path), 'rb').read()).decode()

def mime_for(path):
    ext = os.path.splitext(path)[1].lower()
    return {"jpg": "jpeg", "jpeg": "jpeg", "png": "png", "webp": "webp"}.get(ext.lstrip("."), "jpeg")

LOGO_FULL = b64('assets/logo/logo_full.png')
TOOTH = b64('assets/logo/tooth_icon.png')

def slugify(name):
    name = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore').decode('ascii')
    name = name.lower()
    name = re.sub(r'[^a-z0-9]+', '-', name).strip('-')
    return name

def find_photo(name):
    slug = slugify(name)
    for ext in PHOTO_EXTS:
        p = os.path.join(PRODUCTS_DIR, slug + ext)
        if os.path.isfile(p):
            return p
    return None

# ---------------------------------------------------------------------------
# Icon library (simple line-art SVGs, 0 0 64 64 viewBox, stroke-based)
# Used as a fallback whenever no photo is found for a product.
# ---------------------------------------------------------------------------
ICONS = {
"gloves": """
<path d="M18 30 V14 a4 4 0 0 1 8 0 V26" />
<path d="M26 26 V11 a4 4 0 0 1 8 0 V26" />
<path d="M34 26 V13 a4 4 0 0 1 8 0 V28" />
<path d="M42 28 V19 a3.5 3.5 0 0 1 7 0 V34" />
<path d="M14 34 C14 27 18 24 22 24 C24 24 25 25.5 25.5 27" />
<path d="M14 34 V44 a10 10 0 0 0 10 10 H39 a10 10 0 0 0 10 -10 V34" />
<path d="M22 46 V34 M30 46 V34 M38 46 V34" stroke-width="2" />
""",
"syringe": """
<path d="M14 44 L24 34" />
<rect x="22" y="16" width="12" height="24" rx="2" transform="rotate(45 28 28)"/>
<path d="M33 15 L40 8" />
<path d="M37 19 L44 12" />
<path d="M12 46 L18 52" stroke-width="2"/>
<path d="M9 43 L15 49" stroke-width="2"/>
<line x1="36" y1="6" x2="40" y2="10" stroke-width="2"/>
<circle cx="46" cy="46" r="1.6" fill="var(--green)" stroke="none"/>
<circle cx="50" cy="41" r="1.2" fill="var(--green)" stroke="none"/>
""",
"gauze": """
<rect x="12" y="12" width="40" height="40" rx="3"/>
<path d="M12 22 H52 M12 32 H52 M12 42 H52" stroke-width="1.6" opacity="0.8"/>
<path d="M22 12 V52 M32 12 V52 M42 12 V52" stroke-width="1.6" opacity="0.8"/>
<path d="M40 40 L52 52 L40 52 Z" fill="var(--green-light)" stroke-width="1.6"/>
""",
"suture": """
<path d="M40 12 A12 12 0 1 1 27 22" />
<path d="M25 24 L14 35" stroke-width="2"/>
<path d="M16 33 C22 37 20 43 26 45 C32 47 30 53 36 54" stroke-width="2" fill="none"/>
<circle cx="40.5" cy="11.5" r="1.8" fill="var(--green)" stroke="none"/>
""",
"resin": """
<path d="M32 10 C22 10 20 18 20 24 C20 26 21 27 22 28.5 C24 31 26 30 27 27 C27.5 25.5 28.5 24.5 29 26 C30 30 25 38 22 46 C20 51 24 55 28 52 C30.5 50 31 47 32 44 C33 47 33.5 50 36 52 C40 55 44 51 42 46 C39 38 34 30 35 26 C35.5 24.5 36.5 25.5 37 27 C38 30 40 31 42 28.5 C43 27 44 26 44 24 C44 18 42 10 32 10 Z" />
<path d="M32 14 C34 20 36 27 36 27" stroke-width="2" opacity="0"/>
<circle cx="45" cy="14" r="4.5" fill="var(--green-light)"/>
<path d="M45 10.5 C43 12.5 43 15.5 45 17.5 C47 15.5 47 12.5 45 10.5 Z" fill="var(--green)" stroke="none"/>
""",
"instruments": """
<circle cx="20" cy="17" r="6.5"/>
<circle cx="20" cy="17" r="2.4" fill="var(--green)" stroke="none"/>
<path d="M24.6 21.6 L46 43" stroke-width="3.4"/>
<path d="M43 40 L50 47 M46 37 L53 44" stroke-width="3"/>
<path d="M44 12 C38 12 34 16 34 21 C34 25 37 27 39 29" stroke-width="3"/>
<path d="M39 29 L18 50" stroke-width="3.4"/>
<path d="M15 53 L20 48" stroke-width="3"/>
""",
"bur": """
<rect x="29" y="10" width="6" height="22" rx="2"/>
<path d="M22 32 L32 50 L42 32 Z" />
<circle cx="32" cy="37" r="1.3" fill="var(--green)" stroke="none"/>
<circle cx="27" cy="36" r="1.1" fill="var(--green)" stroke="none"/>
<circle cx="37" cy="36" r="1.1" fill="var(--green)" stroke="none"/>
<circle cx="29" cy="42" r="1.1" fill="var(--green)" stroke="none"/>
<circle cx="35" cy="42" r="1.1" fill="var(--green)" stroke="none"/>
<circle cx="32" cy="46" r="1" fill="var(--green)" stroke="none"/>
""",
"mold": """
<path d="M12 24 C12 42 20 52 32 52 C44 52 52 42 52 24" />
<path d="M17 24 C17 38 23 46 32 46 C41 46 47 38 47 24" stroke-width="2"/>
<path d="M17 24 C17 19 20 15 24 14 M47 24 C47 19 44 15 40 14" stroke-width="2"/>
<path d="M22 16 C22 13 24 11 27 11 M42 16 C42 13 40 11 37 11" stroke-width="2"/>
""",
"whitening": """
<path d="M32 12 C24 12 22 19 22 24 C22 26.5 23.5 28 25 29.5 C27 31.5 28 30 28.5 27.5 C29 25 30 25 30.5 27.5 C31 31 27 39 24.5 45 C23 49 26.5 52.5 30 49.5 C31.5 48 32 45.5 32 43 C32 45.5 32.5 48 34 49.5 C37.5 52.5 41 49 39.5 45 C37 39 33 31 33.5 27.5 C34 25 35 25 35.5 27.5 C36 30 37 31.5 39 29.5 C40.5 28 42 26.5 42 24 C42 19 40 12 32 12 Z" />
<path d="M46 12 L48 16 L52 17 L48 18 L46 22 L44 18 L40 17 L44 16 Z" fill="var(--green)" stroke="none"/>
<path d="M14 22 L15.3 24.6 L18 25.4 L15.3 26.2 L14 28.8 L12.7 26.2 L10 25.4 L12.7 24.6 Z" fill="var(--green)" stroke="none"/>
""",
"vitals": """
<rect x="10" y="18" width="44" height="28" rx="4"/>
<path d="M15 32 H22 L26 24 L31 40 L35 30 L38 32 H49" stroke-width="2.6"/>
<circle cx="45" cy="40" r="1.6" fill="var(--green)" stroke="none"/>
""",
"denture": """
<path d="M8 30 C8 20 14 14 32 14 C50 14 56 20 56 30" stroke-width="2.4"/>
<path d="M14 24 C14 30 16 40 19 46 C20 48 23 48 23.5 45 C24 42 25 42 25.5 45 C26 48 29 48 29.5 45" stroke-width="2"/>
<path d="M29.5 45 C30 42 31 42 31.5 45 C32 48 35 48 35.5 45 C36 42 37 42 37.5 45 C38 48 41 48 41.5 45 C42.2 40 44 30 44 24" stroke-width="2"/>
""",
"antiseptic": """
<path d="M27 10 H37 V16 L40 20 V50 a3 3 0 0 1 -3 3 H27 a3 3 0 0 1 -3 -3 V20 L27 16 Z" />
<rect x="26" y="8" width="12" height="4" rx="1" fill="var(--green)" stroke="none"/>
<path d="M24 34 H40" stroke-width="1.6" opacity="0.6"/>
<path d="M45 30 C45 27 47 26 47 26 C47 26 49 27 49 30 C49 32 47.5 33 47 33 C46.5 33 45 32 45 30 Z" fill="var(--green)" stroke="none"/>
""",
"mask": """
<path d="M10 26 C10 22 14 19 20 19 H44 C50 19 54 22 54 26 V34 C54 42 44 47 32 47 C20 47 10 42 10 34 Z" />
<path d="M10 28 C18 31 26 32 32 32 C38 32 46 31 54 28" stroke-width="2"/>
<path d="M10 34 C18 37 26 38 32 38 C38 38 46 37 54 34" stroke-width="2"/>
<path d="M10 27 C5 25 3 30 6 34 C8 36.5 10 35 10 33" stroke-width="2"/>
<path d="M54 27 C59 25 61 30 58 34 C56 36.5 54 35 54 33" stroke-width="2"/>
""",
}

def icon(key, size=30):
    body = ICONS[key]
    return f'<svg viewBox="0 0 64 64" width="{size}" height="{size}" fill="none" stroke="var(--ink)" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round">{body}</svg>'

# ---------------------------------------------------------------------------
# Catalog content — grouped/consolidated product families from stock report
# ---------------------------------------------------------------------------
SECTIONS = [
{
"icon": "gloves", "num": "01",
"title": "Luvas",
"intro": "Linha completa de luvas de procedimento e cirúrgicas, com opções de tamanho, cor e composição para cada perfil de uso.",
"items": [
    ("Luva de Procedimento em Látex, com pó", "Unigloves · Medix", "Tam. PP, P, M, G, EP  ·  Cores: natural, roxa, rosa, vermelha, preta  ·  Caixa c/ 100 un"),
    ("Luva de Procedimento em Látex, sem pó (linha Conforto/Premium)", "Unigloves · Medix", "Tam. P, M, G  ·  Caixa c/ 100 un"),
    ("Luva de Procedimento Nitrílica, sem pó", "Medix · Unigloves", "Tam. PP, P, M, G  ·  Cores: azul, preta, rosa  ·  Caixa c/ 100 un"),
    ("Luva de Procedimento em Vinil, sem pó", "Medix", "Tam. P, M, G  ·  Caixa c/ 100 un"),
    ("Luva Cirúrgica Estéril em Látex (par)", "Medix", "Numeração 6.0 a 8.5  ·  Com pó"),
    ("Luva Multiuso em Látex, amarela", "Medix", "Tam. P (6), M (7), G (8)"),
]},
{
"icon": "mask", "num": "02",
"title": "Máscaras, Toucas e Vestimentas Descartáveis",
"intro": "Itens de barreira para paramentação da equipe, com variação de cor e gramatura conforme o item.",
"items": [
    ("Máscara Tripla com Elástico", "Medix", "Cores: branca, azul, rosa, preta  ·  Caixa c/ 50 un"),
    ("Touca Sanfonada com Elástico", "Medix", "Cores: branca, preta, rosa  ·  Pacote c/ 100 un"),
    ("Propé Descartável com Elástico", "Medix", "Tamanho único, branco  ·  Pacote c/ 100 un"),
    ("Avental Descartável Manga Longa / TNT", "Medix · Império Descartáveis", "Gramaturas 16g / 30g / 40g  ·  Cores: branco, rosa, azul  ·  Pacote c/ 10 un"),
    ("Babador Descartável / Odontológico", "Biodinâmica · Medix · Maxclean", "Cores: branco, azul, rosa, verde, misto  ·  Pacote c/ 100 un"),
    ("Óculos de Proteção UV", "Medix", "Uso individual — proteção contra fotopolimerizador"),
]},
{
"icon": "syringe", "num": "03",
"title": "Seringas e Agulhas",
"intro": "Seringas descartáveis, agulhas gengivais e hipodérmicas nas principais graduações usadas na rotina clínica.",
"items": [
    ("Seringa Hipodérmica Descartável, sem agulha", "Medix · Procare · Rymco", "Volumes: 3ml, 5ml, 10ml, 20ml"),
    ("Seringa para Insulina, com agulha acoplada", "Medix · Descarpack · Uniqmed · SR Saldanha", "Volumes: 0,3ml / 0,5ml / 1,0ml"),
    ("Agulha Gengival Descartável", "Medix · Procare · DFL", "Curta, extra curta e longa  ·  Calibres 27G / 30G  ·  Caixa c/ 100 un"),
    ("Agulha Hipodérmica Descartável Estéril", "Medix · Solidor", "Calibres 18G a 30G, diversos comprimentos  ·  Caixa c/ 100 un"),
    ("Seringa de Carpule", "Golgran", "Com e sem refluxo"),
    ("Scalp para Infusão Intravenosa", "Medix · Solidor", "Calibres 19G, 21G, 27G  ·  Caixa c/ 100 un"),
    ("Cateter Intravenoso", "Solidor / Biomed", "Calibre 18G  ·  Caixa c/ 50 un"),
]},
{
"icon": "gauze", "num": "04",
"title": "Algodão, Gaze e Papéis Descartáveis",
"intro": "Itens de consumo diário para assepsia, secagem e proteção da cadeira odontológica.",
"items": [
    ("Algodão Hidrófilo", "Melhormed", "Rolo 500g não estéril  ·  Bolas 50g"),
    ("Compressa de Gaze", "Ultracotton · Melhormed · Bio Textil", "7,5x7,5cm  ·  9, 11 ou 13 fios  ·  Estéril e não estéril"),
    ("Rolete Dental de Algodão", "SS Plus · Cremer", "Pacote/caixa c/ 100 un"),
    ("Papel Grau Cirúrgico em Rolo", "Medix · Pack CG", "Larguras de 5cm a 350mm  ·  Rolo 100m"),
    ("Papel Toalha Interfolha", "Alve Flor · CA Clean", "20x20cm"),
    ("Lençol Descartável TNT / Papel", "Medix · Descarbox", "Com elástico  ·  Rolo ou pacote c/ 10 un"),
]},
{
"icon": "suture", "num": "05",
"title": "Fios de Sutura",
"intro": "Fios estéreis agulhados nas espessuras e materiais mais usados em cirurgias orais.",
"items": [
    ("Fio de Sutura Categute", "Technofio", "Espessuras 0, 2-0, 3-0  ·  Estéril, caixa c/ 24 un"),
    ("Fio de Sutura Seda", "Technofio", "Espessuras 3-0, 4-0  ·  Caixa c/ 24 un"),
    ("Fio de Sutura Nylon", "Technofio · Procare · Shalon", "Espessuras 2-0 a 6-0  ·  Agulhados, caixa c/ 24 un"),
]},
{
"icon": "resin", "num": "06",
"title": "Dentística — Resinas, Adesivos e Cimentos",
"intro": "Linha de restauradores estéticos e cimentação, cobrindo toda a escala de cores VITA usada nos consultórios.",
"items": [
    ("Resina Composta Micro-híbrida", "Dentsply · Kulzer · 3M · Vigodent", "Escala completa de cores A1 a C2  ·  Seringa 4g"),
    ("Resina Opallis / LLIS / Vittra APS", "FGM", "Linhas Esmalte (EA) e Dentina (DA)  ·  Seringa 4g"),
    ("Resina Filtek Z350 XT / Z100", "3M", "Diversas cores e opacidades  ·  Seringa 4g"),
    ("Resina Composta Nanohíbrida", "Ultradent", "Cores A1E, A2E, A3E, A3B, WXE  ·  Seringa 4g"),
    ("Adesivo Fotopolimerizável Universal / Monocomponente", "Maquira · 3M · FGM · Ivoclar · Iodontosul", "Frascos de 4 a 6ml"),
    ("Cimento de Zinco", "SS White · Vigodent", "Pó e líquido"),
    ("Ionômero de Vidro — restaurador e forramento", "SS White · SDI · Maquira · FGM", "Kits pó + líquido, várias cores"),
    ("Cimento Resinoso Dual", "FGM · 3M · Biodinâmica", "Base + catalisador, várias cores"),
]},
{
"icon": "instruments", "num": "07",
"title": "Instrumental — Exame, Cirurgia e Periodontia",
"intro": "Instrumentais em aço inox das linhas Golgran e Millennium para exame, cirurgia e periodontia.",
"items": [
    ("Espelho Bucal com Cabo", "Golgran", "Nº 3, 4 e 5  ·  Cabos coloridos disponíveis"),
    ("Sonda Exploradora e Periodontal Milimetrada", "Golgran", "Modelos OMS, North Carolina, Nabers"),
    ("Pinças (Clínica, Anatômica, Allis, Kelly, Mosquito)", "Golgran", "Diversos comprimentos, retas e curvas"),
    ("Cureta Periodontal Gracey / Lucas / Molt", "Golgran", "Kit completo 3-4 a 13-14  ·  Cabo padrão ou silicone colorido"),
    ("Fórceps Odontológico", "Golgran", "Adulto e infantil, diversas numerações"),
    ("Alavanca e Elevador Apical", "Golgran", "Reto, esquerdo e direito, adulto"),
]},
{
"icon": "instruments", "num": "08",
"title": "Instrumental — Restauração e Acabamento",
"intro": "Espátulas, calcadores e itens de acabamento para o dia a dia da dentística.",
"items": [
    ("Espátulas e Calcadores para Resina/Cimento", "Golgran · Millennium", "Linha completa de formatos"),
    ("Tesoura Cirúrgica", "Golgran", "Reta e curva, 11,5 a 17cm"),
    ("Cabo para Bisturi", "Golgran", "Nº 3, 4 e 5  ·  Aço inoxidável autoclavável"),
    ("Tira de Lixa de Aço para Acabamento Interproximal", "American Burrs · Biodinâmica · Prevem", "150mm, serrilhada, centro neutro  ·  Pacote c/ 5 a 12 un"),
]},
{
"icon": "bur", "num": "09",
"title": "Brocas e Pontas Diamantadas",
"intro": "Pontas diamantadas FG e brocas carbide para alta e baixa rotação, com mais de 60 códigos em estoque.",
"items": [
    ("Ponta Diamantada FG — linha completa", "FAVA · Microdont", "Mais de 60 códigos: esféricas, troncocônicas, cilíndricas"),
    ("Broca Carbide CA / FG", "Kerr · Microdont", "Diversos formatos e numerações"),
    ("Broca Gates Glidden / Largo", "Microdont", "Numerações 2 a 5, 28mm"),
]},
{
"icon": "mold", "num": "10",
"title": "Moldagem e Gesso",
"intro": "Materiais de moldagem elástica e gessos odontológicos tipo II, III e IV.",
"items": [
    ("Alginato", "Maquira · Kulzer · Vigodent · Zhermack", "Tipo I e II, embalagens de 410 a 454g"),
    ("Silicone de Condensação", "Vigodent", "Putty, Light Body e Catalisador"),
    ("Gesso Pedra", "Yamay · Asfer · Vigodent", "Tipo II, III (branco/amarelo) e IV (rosa)  ·  Pacote 1kg"),
    ("Moldeira Plástica Perfurada", "Maquira · Bioart · Tecnodent", "Totais N1 a N5, superior/inferior"),
]},
{
"icon": "whitening", "num": "11",
"title": "Endodontia e Clareamento",
"intro": "Insumos para tratamento de canal e protocolos de clareamento dental de consultório e caseiro.",
"items": [
    ("Guta-percha ISO Calibrada", "Dentsply", "Nº 15-40 e 45-80, coloridas"),
    ("Lima Manual K-File", "Kerr", "25mm, kit c/ 6 peças"),
    ("Cimento Endodôntico / Selante para Canal", "Dentsply · Vigodent", "Diversas apresentações"),
    ("Hipoclorito de Sódio 2,5%", "Rioquímica", "Frasco 1000ml"),
    ("EDTA Trissódico / Gel", "Biodinâmica", "20ml e gel 3g"),
    ("Clareador Dental de Consultório 35%", "Whiteness · FGM", "Kit com ponteiras"),
    ("Clareador Dental Caseiro 10% a 22%", "Whiteness · FGM", "Seringa 3g"),
]},
{
"icon": "vitals", "num": "12",
"title": "Equipamentos de Diagnóstico",
"intro": "Instrumentos de aferição para triagem clínica na recepção e consultório.",
"items": [
    ("Oxímetro de Dedo de Alta Precisão", "Dellamed", "Display digital"),
    ("Termômetro Clínico Digital / Infravermelho", "Dellamed", "Medição em até 1 segundo"),
    ("Monitor de Pressão Arterial", "Dellamed · Accumed · Premium", "Automático de pulso/braço"),
    ("Balança Digital", "Dellamed", "Até 150kg"),
    ("Estetoscópio", "Honsun · Premium", "Adulto, série inox"),
    ("Medidor de Glicemia + Tiras", "Accu-Chek · On Call Plus · Bioland", "Kit completo com lancetas"),
]},
{
"icon": "denture", "num": "13",
"title": "Dentes Artificiais e Prótese",
"intro": "Dentes de estoque Popdent (Vipi) e resinas acrílicas para bases de prótese.",
"items": [
    ("Dente Artificial Popdent — Anterior", "Vipi", "Superior e inferior, mais de 40 cores/formas, caixa c/ 6 un"),
    ("Dente Artificial Popdent — Posterior", "Vipi", "Superior e inferior, diversas cores, caixa c/ 8 un"),
    ("Resina Acrílica Termopolimerizável", "Vipi", "Incolor e rosa, kg"),
    ("Resina Acrílica Autopolimerizável", "Vipi · TDV", "Cores rosa e vermelha, para reparos e escultura"),
]},
{
"icon": "antiseptic", "num": "14",
"title": "Consultório — Descartáveis e Antissépticos",
"intro": "Itens de biossegurança, sucção e soluções de higiene bucal para completar a rotina do consultório.",
"items": [
    ("Coletor de Perfurocortantes", "Descarbox · Flexpell", "Capacidades 7L, 13L e 20L, com suporte"),
    ("Sugador Cirúrgico / Descartável", "SS Plus · Maxclean · Allprime", "Pacote c/ 40 un"),
    ("Kit de Paramentação Cirúrgica Estéril", "SPK Institucional", "Pequenas cirurgias e implante"),
    ("Gluconato de Clorexidina 0,12%", "Perioplak · Reymer", "Frasco 250ml, 500ml e 1,1L"),
    ("Álcool 70%", "Barbarex", "Frasco 1 litro"),
    ("Flúor Gel / Enxaguante Bucal", "Reymer", "Sabor menta, com e sem álcool"),
]},
]

# ---------------------------------------------------------------------------
# HTML assembly
# ---------------------------------------------------------------------------
CSS = """
@page { size: A4; margin: 0; }
* { box-sizing: border-box; }
:root {
  --green: #5BAE7E;
  --green-dark: #3E8A61;
  --green-light: #E7F4EC;
  --ink: #2C2C2C;
  --body: #55575A;
  --plate: #8B8B8B;
  --plate-dark: #6f6f6f;
  --paper: #FDFDFC;
  --line: #E3E1DC;
}
html, body { margin:0; padding:0; background:#fff; }
body { font-family: 'Liberation Sans','DejaVu Sans',sans-serif; color: var(--body); }
.page {
  width: 210mm; height: 297mm;
  position: relative;
  overflow: hidden;
  page-break-after: always;
  background: var(--paper);
}
.page:last-child { page-break-after: auto; }

/* ---------- COVER ---------- */
.cover {
  background: linear-gradient(160deg, #7b7b7b 0%, #8b8b8b 55%, #6e6e6e 100%);
  color: #fff;
  display: flex; flex-direction: column; justify-content: space-between;
}
.cover-top { padding: 26mm 20mm 0 20mm; }
.cover-eyebrow {
  text-transform: uppercase; letter-spacing: 3px; font-size: 10.5pt; font-weight: 700;
  color: var(--green-light); opacity: .95; margin-bottom: 6mm;
}
.cover-logo { width: 130mm; max-width: 90%; }
.cover-mid { padding: 0 20mm; }
.cover-title { font-size: 27pt; font-weight: 700; color: #fff; line-height: 1.25; margin: 8mm 0 4mm 0; }
.cover-sub { font-size: 12.5pt; color: #EFEFEF; max-width: 130mm; line-height: 1.5; }
.cover-index {
  margin: 10mm 20mm 0 20mm; background: rgba(255,255,255,.08);
  border: 1px solid rgba(255,255,255,.25); border-radius: 4mm; padding: 8mm 10mm;
}
.cover-index-title { font-size: 9.5pt; letter-spacing: 2px; text-transform: uppercase; color: var(--green-light); font-weight:700; margin-bottom: 4mm; }
.cover-index ol { columns: 2; column-gap: 12mm; margin: 0; padding: 0; list-style: none; }
.cover-index li { font-size: 10.5pt; color: #fff; padding: 1.6mm 0; border-bottom: 1px solid rgba(255,255,255,.15); display:flex; gap:3mm; }
.cover-index li span.n { color: var(--green-light); font-weight: 700; min-width: 6mm; }
.cover-bottom {
  background: rgba(0,0,0,.18); padding: 7mm 20mm; display:flex; flex-direction:column; gap: 1.5mm;
  font-size: 9.5pt; border-top: 1px solid rgba(255,255,255,.15); white-space: nowrap;
}
.cover-bottom b { color: var(--green-light); }

/* ---------- CATEGORY PAGE ---------- */
.head {
  display:flex; align-items:center; justify-content:space-between;
  padding: 14mm 16mm 6mm 16mm; border-bottom: 2px solid var(--green);
}
.head-brand { display:flex; align-items:center; gap:3mm; }
.head-brand img { height: 8mm; }
.head-brand .wordmark { font-family:'Liberation Serif',serif; font-size: 12pt; letter-spacing:1px; color: var(--ink); }
.head-brand .wordmark b { color: var(--green-dark); }
.head-tag { font-size: 8pt; letter-spacing: 1.5px; text-transform: uppercase; color: var(--plate); }

.section-title-row { display:flex; align-items:center; gap:6mm; padding: 8mm 16mm 4mm 16mm; }
.section-num {
  width: 16mm; height:16mm; border-radius: 3mm; background: var(--green-light);
  display:flex; align-items:center; justify-content:center; flex-shrink:0;
}
.section-num svg { width: 9mm; height:9mm; }
.section-title h1 { font-size: 17pt; margin:0 0 1.5mm 0; color: var(--ink); font-weight:700; }
.section-title p { font-size: 9.3pt; margin:0; color: var(--body); max-width: 155mm; line-height:1.45; }

.items { padding: 2mm 16mm 0 16mm; }
.item {
  display:flex; gap:5mm; align-items:center;
  padding: 3.6mm 0; border-bottom: 1px solid var(--line);
}
.item:last-child { border-bottom: none; }
.item-ic {
  width: 19mm; height:19mm; border-radius: 3mm; background: var(--green-light);
  display:flex; align-items:center; justify-content:center; flex-shrink:0;
  overflow: hidden; padding: 1.3mm; border: 1px solid #DCEEE2;
}
.item-ic svg { width: 9mm; height:9mm; }
.item-ic img { max-width: 100%; max-height: 100%; width: auto; height: auto; object-fit: contain; }
.item-name { font-size: 11pt; font-weight:700; color: var(--ink); margin: 0 0 1mm 0; }
.item-brand { font-size: 8.6pt; color: var(--green-dark); font-weight:700; margin: 0 0 1.2mm 0; letter-spacing:.2px;}
.item-var { font-size: 9.3pt; color: var(--body); line-height:1.4; margin:0; }

.foot {
  position:absolute; bottom:0; left:0; right:0;
  display:flex; justify-content:space-between; align-items:center;
  padding: 4mm 16mm; border-top: 1px solid var(--line);
  font-size: 8pt; color: var(--plate);
}
.foot .pg { font-weight:700; color: var(--green-dark); }

/* ---------- BACK COVER ---------- */
.back {
  background: linear-gradient(160deg, #7b7b7b 0%, #8b8b8b 55%, #6e6e6e 100%);
  color:#fff; display:flex; flex-direction:column; align-items:center; justify-content:center; text-align:center;
  gap: 8mm;
}
.back img.tooth { width: 30mm; }
.back h2 { font-size: 20pt; margin:0; }
.back p { font-size: 11pt; color:#EFEFEF; margin:0; max-width:120mm; line-height:1.5; }
.back .contact { margin-top: 6mm; font-size: 11pt; }
.back .contact b { color: var(--green-light); }
"""

def item_visual(name, icon_key):
    """Photo if assets/products/<slug>.(jpg|png|webp) exists, else the line-icon."""
    photo = find_photo(name)
    if photo:
        data = base64.b64encode(open(photo, 'rb').read()).decode()
        return f'<img src="data:image/{mime_for(photo)};base64,{data}" alt=""/>'
    return icon(icon_key, 8)

def render_items_with_icon(items, icon_key):
    out = []
    for name, brand, var in items:
        out.append(f"""
        <div class="item">
          <div class="item-ic">{item_visual(name, icon_key)}</div>
          <div>
            <p class="item-name">{html.escape(name)}</p>
            <p class="item-brand">{html.escape(brand)}</p>
            <p class="item-var">{html.escape(var)}</p>
          </div>
        </div>""")
    return "".join(out)

def cover_page():
    idx_items = "".join(
        f'<li><span class="n">{s["num"]}</span>{html.escape(s["title"])}</li>' for s in SECTIONS
    )
    return f"""
<div class="page cover">
  <div class="cover-top">
    <div class="cover-eyebrow">Catálogo de Produtos · Edição 2026</div>
    <img class="cover-logo" src="data:image/png;base64,{LOGO_FULL}"/>
  </div>
  <div class="cover-mid">
    <div class="cover-title">Produtos odontológicos<br/>e hospitalares, organizados<br/>por categoria.</div>
    <div class="cover-sub">Seleção consolidada do nosso estoque — famílias de produtos agrupadas por tipo, com as variações de tamanho, cor e apresentação disponíveis em cada uma.</div>
  </div>
  <div class="cover-index">
    <div class="cover-index-title">Neste catálogo</div>
    <ol>{idx_items}</ol>
  </div>
  <div class="cover-bottom">
    <div><b>Dent Med</b> — Produtos Odontológicos e Hospitalares</div>
    <div>Quadra 3 Conjunto A, Lote 41 - Loja 1, Planaltina/DF &nbsp;·&nbsp; Tel. (61) 3600-0140</div>
  </div>
</div>
"""

def category_page(section, page_no, total_pages):
    return f"""
<div class="page">
  <div class="head">
    <div class="head-brand">
      <img src="data:image/png;base64,{TOOTH}"/>
      <div class="wordmark">DENT<b>·</b>MED</div>
    </div>
    <div class="head-tag">Catálogo de Produtos</div>
  </div>
  <div class="section-title-row">
    <div class="section-num">{icon(section['icon'], 9)}</div>
    <div class="section-title">
      <h1>{html.escape(section['num'])} &nbsp;{html.escape(section['title'])}</h1>
      <p>{html.escape(section['intro'])}</p>
    </div>
  </div>
  <div class="items">
    {render_items_with_icon(section['items'], section['icon'])}
  </div>
  <div class="foot">
    <div>Dent Med · Produtos Odontológicos e Hospitalares</div>
    <div class="pg">{page_no:02d} / {total_pages:02d}</div>
  </div>
</div>
"""

def back_page():
    return f"""
<div class="page back">
  <img class="tooth" src="data:image/png;base64,{TOOTH}"/>
  <h2>Vamos atender o seu consultório</h2>
  <p>Fale com a nossa equipe para orçamentos, condições especiais e disponibilidade completa do estoque.</p>
  <div class="contact">
    <b>(61) 3600-0140</b><br/>
    Quadra 3 Conjunto A, Lote 41 - Loja 1 — Planaltina/DF
  </div>
</div>
"""

def build():
    total_pages = len(SECTIONS) + 2
    pages = [cover_page()]
    for i, s in enumerate(SECTIONS, start=2):
        pages.append(category_page(s, i, total_pages))
    pages.append(back_page())
    html_doc = f"""<!DOCTYPE html>
<html lang="pt-BR"><head><meta charset="utf-8"/>
<title>Dent Med — Catálogo de Produtos</title>
<style>{CSS}</style>
</head><body>
{''.join(pages)}
</body></html>"""
    out_path = os.path.join(BASE, "catalogo_dentmed.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html_doc)
    print("wrote", out_path, len(html_doc), "bytes")
    used = sum(1 for s in SECTIONS for (n, b, v) in s["items"] if find_photo(n))
    total = sum(len(s["items"]) for s in SECTIONS)
    print(f"product photos found: {used}/{total} (rest fall back to line-icons)")

if __name__ == "__main__":
    build()
