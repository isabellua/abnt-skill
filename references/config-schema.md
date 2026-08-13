# Schema do config.json

O arquivo `config.json` alimenta o script `gerar_abnt.py`. Todos os campos são opcionais;
campos ausentes são substituídos por `[PREENCHER]` no documento.

## Campos gerais (TCC e relatório)

```json
{
  "instituicao":  "Universidade Federal do Paraná",
  "curso":        "Engenharia de Software",
  "autor":        "João da Silva Santos",
  "titulo":       "Inteligência Artificial na Educação Básica",
  "subtitulo":    "Uma revisão sistemática da literatura",
  "orientador":   "Prof. Dr. Maria Oliveira",
  "grau":         "Bacharel",
  "cidade":       "Curitiba",
  "ano":          2025
}
```

## Resumo e abstract

```json
{
  "resumo": "Parágrafo único em 3ª pessoa do singular, sem citações e sem abreviações. Mínimo 150 palavras para TCC.",
  "palavras_chave": ["Inteligência artificial", "Educação básica", "Revisão sistemática"],

  "abstract": "Same content translated to English, third person singular.",
  "keywords": ["Artificial intelligence", "Basic education", "Systematic review"]
}
```

> **Separação de palavras-chave:** ponto e vírgula — o script gera `Inteligência artificial; Educação básica; Revisão sistemática`.

## Sumário

```json
{
  "sumario": [
    {"numero": "1",     "titulo": "Introdução",          "pagina": "13", "nivel": 1},
    {"numero": "1.1",   "titulo": "Contextualização",    "pagina": "14", "nivel": 2},
    {"numero": "1.1.1", "titulo": "Objetivo geral",      "pagina": "15", "nivel": 3},
    {"numero": "2",     "titulo": "Revisão de literatura","pagina": "16", "nivel": 1},
    {"numero": "3",     "titulo": "Metodologia",         "pagina": "20", "nivel": 1},
    {"numero": "4",     "titulo": "Resultados",          "pagina": "24", "nivel": 1},
    {"numero": "5",     "titulo": "Conclusão",           "pagina": "30", "nivel": 1}
  ]
}
```

> Não inclua no sumário os pré-textuais (resumo, abstract, dedicatória etc.).

## Seções textuais

```json
{
  "secoes": [
    {
      "nivel": 1,
      "numero": "1",
      "titulo": "Introdução",
      "conteudo": "Texto da introdução em parágrafo único ou lista de strings."
    },
    {
      "nivel": 2,
      "numero": "1.1",
      "titulo": "Contextualização do Problema",
      "conteudo": [
        "Primeiro parágrafo do desenvolvimento.",
        "Segundo parágrafo com mais detalhes."
      ],
      "citacoes_longas": [
        {
          "texto": "Trecho com mais de três linhas que será recuado automaticamente em 4 cm e formatado com fonte 10 e espaço simples.",
          "autor": "SILVA, 2020, p. 45"
        }
      ]
    }
  ]
}
```

## Referências

```json
{
  "referencias": [
    "FREIRE, Paulo. Pedagogia do oprimido. 17. ed. Rio de Janeiro: Paz e Terra, 1987.",
    "LIMA, Manolita C. Monografia: a engenharia da produção acadêmica. 2. ed. São Paulo: Saraiva, 2008.",
    "SILVA, João; SOUZA, Maria. Metodologia de pesquisa. São Paulo: Atlas, 2020."
  ]
}
```

> As referências são inseridas como texto puro (já formatadas pelo usuário). Veja formatos em `nbr6023-referencias.md`.

## Apêndices e Anexos

```json
{
  "apendices": [
    {
      "titulo": "Questionário aplicado",
      "conteudo": "Texto ou descrição do apêndice."
    }
  ],
  "anexos": [
    {
      "titulo": "Parecer do Comitê de Ética",
      "conteudo": "Texto do documento de terceiros."
    }
  ]
}
```

## Exemplo mínimo (TCC com placeholders)

```json
{
  "instituicao": "Universidade Federal do Paraná",
  "curso": "Engenharia de Software",
  "autor": "João da Silva Santos",
  "titulo": "Meu Trabalho de Conclusão de Curso",
  "orientador": "Prof. Dr. Maria Oliveira",
  "grau": "Bacharel",
  "cidade": "Curitiba",
  "ano": 2025,
  "resumo": "[Insira aqui o resumo em parágrafo único, 3ª pessoa singular.]",
  "palavras_chave": ["Palavra-chave 1", "Palavra-chave 2", "Palavra-chave 3"],
  "abstract": "[Insert abstract here in a single paragraph, third person singular.]",
  "keywords": ["Keyword 1", "Keyword 2", "Keyword 3"],
  "secoes": [
    {"nivel": 1, "numero": "1", "titulo": "Introdução", "conteudo": "[Texto da introdução]"},
    {"nivel": 1, "numero": "2", "titulo": "Desenvolvimento", "conteudo": "[Texto do desenvolvimento]"},
    {"nivel": 1, "numero": "3", "titulo": "Conclusão", "conteudo": "[Texto da conclusão]"}
  ],
  "referencias": [
    "AUTOR, Sobrenome. Título da obra. Cidade: Editora, Ano."
  ]
}
```
