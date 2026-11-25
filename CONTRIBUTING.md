# Como contribuir

Este repositório mantém uma lista curada e verificada de benefícios reais para estudantes no Brasil. Prefira qualidade e evidência a volume.

## Critérios de aceitação

Toda entrada no [README.md](README.md) precisa atender aos três pontos abaixo:

1. **Exige vínculo estudantil ou elegibilidade acadêmica:** planos que já são gratuitos para qualquer pessoa ficam fora das tabelas principais (podem ser citados em [docs/criterios-e-fora-da-lista.md](docs/criterios-e-fora-da-lista.md) apenas como referência).
2. **Funciona no Brasil:** validável com `.edu.br`, e-mail institucional de faculdade brasileira, declaração de matrícula, DNE/CIE, SheerID, UNiDAYS Brasil, Goodstack ou CadÚnico.
3. **Link oficial e público:** página direta do programa educacional em `https://`, sem paywall, sem link de afiliado e sem código de indicação.

## O que não enviar

- Links com parâmetros de afiliado, referral ou encurtadores (`bit.ly`, `utm_*` promocional).
- Ofertas exclusivas de `.edu` dos EUA, Canadá ou Europa.
- Programas encerrados ou testes gratuitos padrão abertos ao público geral.
- Benefícios sem explicação clara de como validar no Brasil.

## Padrão de formatação

- Idioma: `pt-BR`.
- Não use travessão longo (`—`) nem emojis decorativos.
- Mantenha arquivos Markdown abaixo de 300 linhas.
- Ao atualizar preços ou regras, inclua a data ou observação objetiva na coluna correspondente.

## Validação local antes do PR

Instale os hooks do repositório e rode a checagem estrutural:

```bash
make hooks
make check
```

Para testar também a disponibilidade HTTP dos links externos:

```bash
make check-urls
```
