# Convite Digital — Inauguração do Showroom Romini

Convite interativo feito a partir do `CONVITE DIGITAL.pdf`. O PDF é uma única página
de 540×1920 pt — na verdade **duas telas 9:16 empilhadas**: o envelope lacrado em cima
e o convite embaixo. O site reproduz o layout original pixel a pixel e liga as duas
telas com a animação de abertura do envelope.

## Arquivos

| Arquivo | Para quê |
|---|---|
| `index.html` | Versão de desenvolvimento (usa `assets/`) |
| `assets/envelope.jpg` | Tela 1 do PDF — envelope com o lacre |
| `assets/convite.jpg` | Tela 2 do PDF — o convite |
| `convite-completo.html` | **Arquivo único**, imagens embutidas — é só enviar/hospedar |
| `build-artifact.py` | Regera o `convite-completo.html` a partir do `index.html` |

## Antes de publicar: troque os dois links

No topo do `<script>` em `index.html`:

```js
const CONFIG = {
  mapa:      "https://...",   // botão do pin
  instagram: "https://..."    // botão do Instagram
};
```

Depois rode `python3 build-artifact.py` para regerar o arquivo único.

## Como funciona a abertura

Não há corte nem troca de imagem: a **mesma** foto do envelope é recortada por
`clip-path` na linha exata do V (medida do PDF: as bordas encontram as laterais em
37,19% e 38,85%, e o bico fica em 53,33% / 58,33%). A parte de cima vira a aba, a de
baixo vira o corpo. Como o lacre de cera está bem em cima do bico, ele se parte
sozinho na linha do recorte quando a aba sobe — a metade de cima vai junto com a aba,
a de baixo fica no corpo. A sequência, no GSAP:

1. o lacre afunda e uma onda sai dele
2. rachadura de luz no bico + 12 lascas de cera + estalo sintetizado (Web Audio)
3. a aba gira em `rotateX(-172°)` em 3D e troca de face aos 90°
4. o convite sobe **de dentro** do envelope (atrás do corpo, na frente do forro)
5. o corpo desce e some; o convite ocupa a tela com um brilho passando

Camadas, de trás para frente: forro → convite → corpo do envelope → aba → rachadura.

## Detalhes

- **GSAP 3.12.5** via CDN — única dependência.
- **URL**: abrir o convite grava `#convite`, então o botão "voltar" do navegador
  fecha o envelope de novo. Compartilhar o link com `#convite` já abre no convite.
- **Acessibilidade**: `prefers-reduced-motion` pula a animação e vai direto ao
  convite; o lacre é um `<button>` de verdade, com foco visível e `aria-label`.
- **Som**: gerado no navegador (sem arquivos), com botão de mudo.
- O botão ↺ no canto fecha o convite e volta ao envelope.

## Rodando local

```sh
python3 -m http.server 8777
# http://localhost:8777
```

`convite-completo.html` também abre com dois cliques, direto do Finder.
# convite_romini
