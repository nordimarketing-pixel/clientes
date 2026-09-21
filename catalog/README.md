# Catálogo Dent Med — como adicionar fotos reais dos produtos

Esta sessão (ambiente web/cloud) não tem acesso à internet, então o catálogo
foi montado com ícones ilustrados no lugar de fotos. Para trocar os ícones
por fotos reais, rode isto numa sessão do Claude Code **com acesso à web**
(local/desktop, por exemplo) neste mesmo branch.

## Passo a passo

1. Pesquise e baixe uma foto para cada produto abaixo (fundo neutro/branco,
   de preferência foto de catálogo do fabricante ou de e-commerce).
2. Salve cada imagem em `catalog/assets/products/<slug>.jpg` (pode ser
   `.jpg`, `.png` ou `.webp`) usando exatamente o nome de arquivo (slug)
   indicado na lista abaixo — é assim que `build_catalog.py` encontra a foto
   certa para cada item.
3. Rode `python3 catalog/build_catalog.py` — ele regenera
   `catalog/catalogo_dentmed.html`, e imprime quantas fotos foram
   encontradas (`product photos found: X/Y`). Qualquer item sem foto
   correspondente continua usando o ícone de linha como fallback, então dá
   pra rodar incrementalmente.
4. Gere o PDF a partir do HTML (A4, com background):
   ```bash
   npm install -g playwright   # se ainda não tiver
   node catalog/render.js      # gera catalog/catalogo_dentmed.pdf
   ```
   Ou, se preferir, abra `catalogo_dentmed.html` num Chrome/Chromium e use
   "Imprimir > Salvar como PDF" com tamanho A4 e margens em 0.
5. Copie o PDF final para a raiz do repo (`catalogo_dentmed.pdf`) e faça
   commit + push no branch `claude/dentmed-a4-catalog-5fy0rc`.

## Lista de slugs por categoria (nome do arquivo esperado em `assets/products/`)

### 01 Luvas
- `luva-de-procedimento-em-latex-com-po.jpg` — Luva de Procedimento em Látex, com pó (Unigloves/Medix)
- `luva-de-procedimento-em-latex-sem-po-linha-conforto-premium.jpg` — Luva de Procedimento em Látex, sem pó
- `luva-de-procedimento-nitrilica-sem-po.jpg` — Luva de Procedimento Nitrílica, sem pó
- `luva-de-procedimento-em-vinil-sem-po.jpg` — Luva de Procedimento em Vinil, sem pó
- `luva-cirurgica-esteril-em-latex-par.jpg` — Luva Cirúrgica Estéril em Látex
- `luva-multiuso-em-latex-amarela.jpg` — Luva Multiuso em Látex, amarela

### 02 Máscaras, Toucas e Vestimentas Descartáveis
- `mascara-tripla-com-elastico.jpg`
- `touca-sanfonada-com-elastico.jpg`
- `prope-descartavel-com-elastico.jpg`
- `avental-descartavel-manga-longa-tnt.jpg`
- `babador-descartavel-odontologico.jpg`
- `oculos-de-protecao-uv.jpg`

### 03 Seringas e Agulhas
- `seringa-hipodermica-descartavel-sem-agulha.jpg`
- `seringa-para-insulina-com-agulha-acoplada.jpg`
- `agulha-gengival-descartavel.jpg`
- `agulha-hipodermica-descartavel-esteril.jpg`
- `seringa-de-carpule.jpg`
- `scalp-para-infusao-intravenosa.jpg`
- `cateter-intravenoso.jpg`

### 04 Algodão, Gaze e Papéis Descartáveis
- `algodao-hidrofilo.jpg`
- `compressa-de-gaze.jpg`
- `rolete-dental-de-algodao.jpg`
- `papel-grau-cirurgico-em-rolo.jpg`
- `papel-toalha-interfolha.jpg`
- `lencol-descartavel-tnt-papel.jpg`

### 05 Fios de Sutura
- `fio-de-sutura-categute.jpg`
- `fio-de-sutura-seda.jpg`
- `fio-de-sutura-nylon.jpg`

### 06 Dentística — Resinas, Adesivos e Cimentos
- `resina-composta-micro-hibrida.jpg`
- `resina-opallis-llis-vittra-aps.jpg` (buscar "resina FGM Opallis")
- `resina-filtek-z350-xt-z100.jpg` (buscar "resina 3M Filtek Z350 XT")
- `resina-composta-nanohibrida.jpg` (buscar "resina Ultradent nanohíbrida")
- `adesivo-fotopolimerizavel-universal-monocomponente.jpg`
- `cimento-de-zinco.jpg`
- `ionomero-de-vidro-restaurador-e-forramento.jpg`
- `cimento-resinoso-dual.jpg`

### 07 Instrumental Odontológico
- `espelho-bucal-com-cabo.jpg`
- `sonda-exploradora-e-periodontal-milimetrada.jpg`
- `pincas-clinica-anatomica-allis-kelly-mosquito.jpg`
- `cureta-periodontal-gracey-lucas-molt.jpg`
- `forceps-odontologico.jpg`
- `alavanca-e-elevador-apical.jpg`
- `espatulas-e-calcadores-para-resina-cimento.jpg`
- `tesoura-cirurgica.jpg`

### 08 Brocas e Pontas Diamantadas
- `ponta-diamantada-fg-linha-completa.jpg` (buscar "ponta diamantada FG Fava")
- `broca-carbide-ca-fg.jpg` (buscar "broca carbide Kerr odontológica")
- `broca-gates-glidden-largo.jpg`

### 09 Moldagem e Gesso
- `alginato.jpg` (buscar "alginato odontológico Maquira")
- `silicone-de-condensacao.jpg` (buscar "silicone de condensação Vigodent")
- `gesso-pedra.jpg`
- `moldeira-plastica-perfurada.jpg`

### 10 Endodontia e Clareamento
- `guta-percha-iso-calibrada.jpg`
- `lima-manual-k-file.jpg` (buscar "lima endodôntica K-File Kerr")
- `cimento-endodontico-selante-para-canal.jpg`
- `hipoclorito-de-sodio-2-5.jpg`
- `edta-trissodico-gel.jpg`
- `clareador-dental-de-consultorio-35.jpg` (buscar "Whiteness HP FGM clareador consultório")
- `clareador-dental-caseiro-10-a-22.jpg` (buscar "Whiteness Perfect FGM clareador caseiro")

### 11 Equipamentos de Diagnóstico
- `oximetro-de-dedo-de-alta-precisao.jpg` (buscar "oxímetro de dedo Dellamed")
- `termometro-clinico-digital-infravermelho.jpg`
- `monitor-de-pressao-arterial.jpg`
- `balanca-digital.jpg`
- `estetoscopio.jpg`
- `medidor-de-glicemia-tiras.jpg` (buscar "medidor de glicemia Accu-Chek")

### 12 Dentes Artificiais e Prótese
- `dente-artificial-popdent-anterior.jpg` (buscar "dente Popdent Vipi anterior")
- `dente-artificial-popdent-posterior.jpg` (buscar "dente Popdent Vipi posterior")
- `resina-acrilica-termopolimerizavel.jpg` (buscar "resina acrílica Vipi Cril")
- `resina-acrilica-autopolimerizavel.jpg`

### 13 Consultório — Descartáveis e Antissépticos
- `coletor-de-perfurocortantes.jpg` (buscar "coletor perfurocortante Descarbox")
- `sugador-cirurgico-descartavel.jpg`
- `kit-de-paramentacao-cirurgica-esteril.jpg`
- `gluconato-de-clorexidina-0-12.jpg` (buscar "clorexidina Perioplak")
- `alcool-70.jpg`
- `fluor-gel-enxaguante-bucal.jpg`

## Observações

- A lista de slugs também pode ser reimpressa a qualquer momento com:
  ```bash
  cd catalog && python3 -c "
  import build_catalog as bc
  for s in bc.SECTIONS:
      for name, brand, var in s['items']:
          print(bc.slugify(name) + '.jpg  <-  ' + name)
  "
  ```
- Fotos quadradas (proporção 1:1) ficam melhores — elas são recortadas em
  círculo (`object-fit: cover`) no layout atual.
- A logo e o ícone do dente já extraídos do cartão de visita estão em
  `catalog/assets/logo/`.
- Todo o texto/estrutura do catálogo (categorias, produtos, variações)
  vem do relatório de estoque `DENT_MED_ESTOQUE_1709_1.pdf` enviado pelo
  cliente — os 968 itens foram agrupados em 13 famílias de produto.
