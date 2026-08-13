---
name: abnt-formatter
description: >
  Formata documentos acadêmicos e técnicos conforme as normas ABNT brasileiras (NBR 14724,
  NBR 6023, NBR 10520, NBR 6024, NBR 6027, NBR 6028). Gera arquivos .docx prontos para
  entrega com margens, fontes, espaçamentos, citações, referências bibliográficas e estrutura
  de capas corretas. Use esta skill sempre que o usuário mencionar: TCC, monografia,
  dissertação, tese, artigo ABNT, relatório técnico, trabalho acadêmico, formatação ABNT,
  normas ABNT, NBR, referências ABNT, citações ABNT, capa ABNT, sumário ABNT — mesmo que
  não peça explicitamente um arquivo .docx. Se o usuário tiver um documento em texto e quiser
  formatá-lo nas normas, ou quiser criar um documento do zero com conteúdo acadêmico, use
  esta skill.
---

# Skill: Formatador ABNT

Esta skill gera documentos acadêmicos e técnicos com formatação rigorosamente conforme as
normas ABNT. O resultado principal é sempre um arquivo `.docx` pronto para impressão e entrega.

## Como usar esta skill

1. **Entender o que o usuário precisa** — tipo de documento, conteúdo disponível, seções necessárias
2. **Coletar o conteúdo** — peça ou use o texto já fornecido pelo usuário
3. **Executar o script de geração** usando `scripts/gerar_abnt.py`
4. **Entregar o `.docx` gerado** e explicar as escolhas de formatação

## Tipos de documentos suportados

- **TCC / Monografia** — capa, folha de rosto, resumo, abstract, sumário, introdução, desenvolvimento, conclusão, referências, apêndices/anexos
- **Artigo científico** — título, autores, resumo, abstract, seções, referências
- **Relatório técnico** — capa, sumário, introdução, corpo, conclusão, referências

## Regras de formatação ABNT (NBR 14724)

Consulte `references/nbr14724-formatacao.md` para regras detalhadas.

| Elemento | Especificação |
|---|---|
| Papel | A4 (21 × 29,7 cm), branco |
| Margem superior | 3 cm |
| Margem inferior | 2 cm |
| Margem esquerda | 3 cm |
| Margem direita | 2 cm |
| Fonte texto | Times New Roman ou Arial |
| Tamanho fonte texto | 12 pt |
| Tamanho fonte citação longa | 10 pt (ou 11 pt) |
| Tamanho fonte notas de rodapé | 10 pt |
| Espaçamento texto | 1,5 entre linhas |
| Espaçamento citação longa | Simples (1,0) |
| Recuo parágrafo | 1,25 cm (primeira linha) |
| Recuo citação longa | 4 cm da margem esquerda (recomendado) |
| Numeração de páginas | Superior direito, arábicos, a 2 cm da margem superior |
| Alinhamento texto | Justificado |
| Alinhamento referências | À esquerda |

## Estrutura de um TCC

```
PRÉ-TEXTUAIS:
  Capa (obrigatória)
  Folha de rosto (obrigatória)
  Folha de aprovação (obrigatória)
  Resumo em português (obrigatório)
  Resumo em língua estrangeira — abstract (obrigatório)
  Sumário (obrigatório)
  [Listas de ilustrações, tabelas, abreviações — opcionais]

TEXTUAIS:
  Introdução
  Desenvolvimento (capítulos temáticos)
  Conclusão

PÓS-TEXTUAIS:
  Referências (obrigatório)
  Apêndice(s) (opcional — elaborado pelo autor)
  Anexo(s) (opcional — elaborado por terceiros)
```

## Capa (NBR 14724)

Ordem obrigatória, tudo centralizado:

1. Nome da Instituição (maiúsculo)
2. Curso
3. Autor (maiúsculo)
4. **Título** (maiúsculo, negrito)
5. Subtítulo (se houver)
6. Local e Ano

## Folha de rosto

Contém os dados da capa + "Natureza do trabalho" recuado **7,5 cm** da margem esquerda,
fonte 10, espaço simples.

## Resumo e abstract

- Título "RESUMO" / "ABSTRACT": maiúsculo, negrito, centralizado, fonte 12
- Texto: fonte 12, espaçamento **simples**, **sem recuo** na primeira linha, parágrafo único
- Escrito na **3ª pessoa do singular**, voz ativa
- Sem citações bibliográficas e sem abreviações
- Extensão: 100–500 palavras (100 para artigos; 150 para TCC)
- Palavras-chave: separadas por **ponto e vírgula** (ex.: `Educação; ABNT; TCC`)

## Sumário

- Título "SUMÁRIO" centralizado, maiúsculo
- Lista apenas elementos textuais e pós-textuais (não lista pré-textuais como resumo, abstract etc.)
- Numeração e títulos refletem exatamente os do texto

## Numeração de páginas

- A contagem começa na **folha de rosto** (número 1), mas o número não aparece nas pré-textuais
- O número aparece a partir da **introdução**, no **canto superior direito**, a **2 cm da margem superior**
- Algarismos arábicos

## Citações (NBR 10520) — resumo

Consulte `references/nbr10520-citacoes.md` para todos os casos.

- **Direta curta** (até 3 linhas): entre aspas duplas no texto — "texto" (AUTOR, ano, p. X)
- **Direta longa** (mais de 3 linhas): recuo 4 cm, fonte 10, espaço simples, sem aspas (recuo recomendado, não obrigatório desde ABNT 2023)
- **Indireta/paráfrase**: sem aspas, sem recuo — (AUTOR, ano) ou Autor (ano)
- **Dois autores**: (SILVA; SOUZA, 2020) — ponto e vírgula entre parênteses
- **Quatro ou mais**: (SILVA *et al.*, 2020)

### Expressões latinas (ABNT 2023)

Devem ser escritas em **itálico**: *apud*, *ibidem*, *et al.*, *op. cit.*, *loc. cit.*

- Correta: (Adorno; Horkheimer, 1947 *apud* Mazzetti, 2008, p. 259)
- Correta: (Araújo *et al.*, 2021)

### Fontes sem paginação

Para e-books e fontes sem número de página, indicar a localização:

- (Cavalcanti, 2018, local 27)
- (Cavalcanti, 2018, cap. 3, seção 2)

### Destaque em citações

Ao destacar trecho com negrito, itálico ou sublinhado, acrescentar ao final:

- `(AUTOR, ano, p. X, grifo nosso)` — quando o destaque é seu
- `(AUTOR, ano, p. X, grifo do autor)` — quando o destaque já estava no original
- Tradução: acrescentar `tradução nossa` ou `tradução própria`

## Referências (NBR 6023) — formatos essenciais

Consulte `references/nbr6023-referencias.md` para todos os formatos.

- Livro: `SOBRENOME, Nome. **Título**. ed. Local: Editora, ano.`
- Artigo: `SOBRENOME, Nome. Título. **Revista**, v. X, n. Y, p. X-Y, mês ano.`
- Site: `AUTOR. **Título**. Disponível em: URL. Acesso em: dia mês. ano.`
- Anais: `AUTOR. Título. In: NOME DO EVENTO, n., ano, Local. **Anais** [...]. Local: Ed., ano. p. X-Y.`

## Numeração de seções (NBR 6024)

| Nível | Formato |
|---|---|
| Seção primária | MAIÚSCULO, negrito — **1 INTRODUÇÃO** |
| Seção secundária | MAIÚSCULO, sem negrito — 1.1 CONTEXTO |
| Seção terciária | Minúsculo, negrito — 1.1.1 Objetivo geral |
| Seção quaternária | Minúsculo, itálico |

## Como executar o script

```bash
pip install python-docx
python3 scripts/gerar_abnt.py --tipo tcc --config config.json --saida documento.docx
```

Veja o formato do `config.json` em `references/config-schema.md`.

## Fluxo recomendado

1. Usuário tem texto pronto → montar config.json e gerar .docx
2. Usuário quer criar do zero → perguntar dados e gerar com placeholders [PREENCHER]
3. Usuário quer corrigir referências → aplicar NBR 6023 diretamente no chat
4. Usuário pede template → gerar .docx com estrutura completa e placeholders

## Perguntas para TCC completo

- Nome completo do autor
- Título e subtítulo do trabalho
- Instituição / Universidade / Curso
- Nome do orientador e título (Prof. Dr., Prof. Me. etc.)
- Grau almejado (Bacharel, Licenciado, Tecnólogo, Especialista)
- Cidade e ano de entrega
- Palavras-chave (3 a 6)
- Conteúdo das seções ou usar placeholders?
