# Catálogo Dent Med — fotos dos produtos

67 dos 76 produtos já têm foto real (enviada pelo cliente, verificada uma a
uma contra o nome do produto). Os 9 que faltam continuam com o ícone
ilustrado como fallback automático.

## Faltam foto (9)

- `luva-de-procedimento-em-latex-sem-po-linha-conforto-premium.jpg`
- `luva-cirurgica-esteril-em-latex-par.jpg`
- `seringa-hipodermica-descartavel-sem-agulha.jpg`
- `seringa-de-carpule.jpg`
- `scalp-para-infusao-intravenosa.jpg`
- `lencol-descartavel-tnt-papel.jpg`
- `espelho-bucal-com-cabo.jpg`
- `moldeira-plastica-perfurada.jpg`
- `resina-acrilica-termopolimerizavel.jpg`

## Como adicionar uma foto

1. Salve a imagem em `catalog/assets/products/<slug>.jpg` (`.jpg`, `.png` ou
   `.webp` funcionam), usando exatamente um dos nomes de arquivo acima.
2. Rode `python3 catalog/build_catalog.py` — regenera
   `catalog/catalogo_dentmed.html` e imprime quantas fotos foram
   encontradas (`product photos found: X/Y`).
3. Gere o PDF:
   ```bash
   npm install -g playwright && npx playwright install chromium   # se ainda não tiver
   node catalog/render.js      # gera catalog/catalogo_dentmed.pdf
   ```
   (ou abra o HTML no Chrome e "Imprimir > Salvar como PDF", A4, margens 0)
4. Copie o PDF pra raiz do repo (`catalogo_dentmed.pdf`) e commit + push no
   branch `claude/dentmed-a4-catalog-5fy0rc`.

Para reimprimir esta lista com o status atual a qualquer momento:
```bash
cd catalog && python3 -c "
import build_catalog as bc
for s in bc.SECTIONS:
    for name, brand, var in s['items']:
        mark = ' [foto ok]' if bc.find_photo(name) else ' [FALTA]'
        print(bc.slugify(name) + '.jpg  <-  ' + name + mark)
"
```

## Notas de layout

- Fotos com fundo branco/neutro ficam melhores — o layout usa
  `object-fit: contain` dentro de um quadrado arredondado de 19mm (a foto
  inteira aparece, sem cortar, mas fica pequena se for muito alongada ou
  na diagonal).
- A logo e o ícone do dente extraídos do cartão de visita estão em
  `catalog/assets/logo/`.
- O catálogo tem 14 categorias (a seção de Instrumental foi dividida em
  duas páginas — "07 Exame/Cirurgia/Periodontia" e "08
  Restauração/Acabamento" — pra caber as fotos sem apertar).
- **Cuidado ao identificar fotos em lote:** ao processar várias imagens de
  uma vez, é fácil trocar a legenda/descrição de uma com a de outra
  (aconteceu aqui — 6 fotos ficaram temporariamente atribuídas ao produto
  errado antes da conferência final). Depois de mapear fotos, sempre
  reabra o arquivo final salvo em `assets/products/<slug>` e confirme que
  ele bate com o nome do produto antes de considerar concluído.
