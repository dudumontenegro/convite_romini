# Convite Digital — Inauguração do Showroom Romini

Convite interativo feito a partir do `CONVITE DIGITAL 3.pdf`. O PDF é uma única página
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

## Antes de publicar: confira os três links

No topo do `<script>` em `index.html`:

```js
const CONFIG = {
  whatsapp:  "https://wa.me/5583993398397?text=...",  // botão "confirmar presença"
  mapa:      "https://...",                           // botão do pin
  instagram: "https://..."                            // botão do Instagram
};
```

O botão de confirmar presença abre o WhatsApp do número **83 99339-8397** já com a
mensagem "Oi! Estou confirmando a minha presença para o Showroom" escrita.

Depois rode `python3 build-artifact.py` para regerar o arquivo único.

## Como funciona a abertura

Não há corte nem troca de imagem: a **mesma** foto do envelope é recortada por
`clip-path` na linha exata do V (medida do PDF: as bordas encontram as laterais em
37,19% e 38,85%, e o bico fica em 53,33% / 58,33%). A parte de cima vira a aba, a de
baixo vira o corpo. A sequência, no GSAP:

1. o lacre afunda e uma onda fina se abre a partir dele
2. a aba se ergue e se dissolve; a aresta da boca do envelope acende
3. **movimento contrário** — o convite sobe enquanto o envelope desce, que é como
   se tira um cartão de dentro de um envelope de verdade
4. uma sombra fixa na boca do envelope deixa tudo abaixo dela no escuro, então o
   convite sai da sombra para a luz conforme sobe
5. o envelope some e o convite assume a tela, com um brilho passando uma vez

Camadas, de trás para frente: forro → convite → corpo do envelope → sombra da boca → aba.

**Estado final:** quando a animação termina, todas as camadas do envelope recebem
`display: none`. Isso não é só limpeza — é o que impede o bug de composição do Safari
no iOS, em que o forro preto do envelope reaparecia por cima do convite. A animação
também é 100% 2D (sem `preserve-3d`), justamente a causa daquele bug.

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
