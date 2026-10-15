# Painel ENADE — Faculdade Três de Maio (SETREM)

Painel para os coordenadores com prazos, conteúdo das provas (portarias na íntegra),
editais e responsabilidades do ENADE/PND. Cursos avaliados em **2026**: Pedagogia
(licenciatura) e Engenharia de Computação (bacharelado); em **2027** (preparação):
Agronomia e Enfermagem.

O site publicado é o **`index.html`** (GitHub Pages). O calendário e os prazos se
atualizam sozinhos pela data real; a legislação é conferida semanalmente contra as
páginas oficiais do INEP.

## Como o painel é gerado

```
cd src
python parse2.py   # extrai o conteúdo VERBATIM das portarias (pdfs/*.pdf) -> port.json
python gen.py      # template.html + port.json + editais -> ../index.html
```

- `src/template.html` — layout e lógica do painel (placeholders `/*__PORT__*/` e `/*__EDITAIS__*/`).
- `src/parse2.py` — extrai perfil, competências/habilidades e objetos das portarias (pdftotext).
- `src/port.json` — conteúdo verbatim das portarias (gerado; versionado).
- `src/pdfs/` — PDFs oficiais das portarias de matriz.
- `index.html` — painel publicado (gerado).

## Fontes oficiais

- Legislação ENADE: https://www.gov.br/inep/pt-br/centrais-de-conteudo/legislacao/enade
- Legislação PND: https://www.gov.br/inep/pt-br/centrais-de-conteudo/legislacao/prova-nacional-docente

Mantido pela Procuradoria Institucional da SETREM.
