# Política de Segurança e Privacidade

Este repositório reúne apenas documentação e links públicos para programas estudantis oficiais. Ainda assim, a segurança das URLs listadas e a proteção de dados pessoais de estudantes são prioridade.

## O que reportar em canal privado

Use o canal privado caso identifique qualquer um dos cenários abaixo:

1. **Links maliciosos, phishing ou domínios sequestrados:** quando um endereço oficial listado passar a redirecionar para golpes, páginas falsas de login ou malware.
2. **Abuso de redirecionamento ou links de afiliado ocultos:** inclusão disfarçada de links de rastreamento ou páginas intermediárias não oficiais.
3. **Exposição acidental de dados pessoais (LGPD):** se alguém publicar em issue, comentário ou pull request documentos com **CPF, RG, RA, número de matrícula, endereço, telefone ou declaração escolar não anonimizada**.
4. **Vulnerabilidade no script de validação ou workflows:** falhas em `scripts/validate.py` ou `.github/workflows/`.

## Como reportar

Não abra uma issue pública para casos envolvendo phishing ativo ou vazamento de dados pessoais.

Envie um relato privado diretamente pelo recurso oficial do repositório:

- [Abrir Security Advisory privado](https://github.com/tiagovilasboas/beneficios-estudantes-brasil/security/advisories/new)

Caso seja apenas um link expirado ou erro 404 sem risco de segurança, utilize o template normal de [Reportar mudança ou link quebrado](https://github.com/tiagovilasboas/beneficios-estudantes-brasil/issues/new?template=reportar-mudanca.yml).

## Boas práticas ao contribuir com evidências

Antes de anexar capturas de tela ou comprovantes em issues ou discussões para mostrar que um benefício funcionou no Brasil:

- Cubra ou remova **nome completo, CPF, RA, código de barras, QR Code do DNE e e-mail pessoal**.
- Informe apenas o nome da plataforma, o tipo de validação (ex.: `SheerID`, `UNiDAYS`, `.edu.br`) e a data do teste.
