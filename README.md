# nf_bot_zap

Bot de WhatsApp (Evolution API) para leitura e validação de notas fiscais eletrônicas (NF-e / NFC-e / entre outros modelos), focado em automatizar conferência fiscal e organização de dados.

## Visão geral

O objetivo do projeto é permitir que o usuário envie uma nota fiscal em PDF pelo WhatsApp e o bot:

- Extraia os dados relevantes da nota com o uso de IA (emitente, destinatário, produtos, tributos, totais).
- Normalize informações fiscais (CNPJ, NCM, CFOP, alíquotas) para facilitar relatórios e análises.
- Armazena esses dados em um banco de dados estruturado.
- É possível visualizar e exportar o relatório das notas recebidas através do painel administrativo.

Com isso, o nf_bot_zap ajuda empresas a:

- Reduzir trabalho manual na conferência de documentos fiscais.
- Diminuir erros de digitação e inconsistências de cadastro.
- Ter uma base de dados de notas mais limpa e padronizada.

## Funcionalidades (planejadas / em desenvolvimento)

- Integração com WhatsApp via API.
- Recebimento de arquivos de nota fiscal.
- Extração automática de dados da NF (IA/OCR ou parsers específicos).
- Normalização de CNPJ, NCM, CFOP e alíquotas em banco de dados.

## Tecnologias

- Python
- FastAPI
- Integração com API de WhatsApp (Evolution API)
- Banco de dados relacional para armazenar notas e cadastros fiscais

## Objetivo do projeto

Entregar uma ferramenta prática para automatizar o fluxo de recebimento e validação de notas fiscais pelo WhatsApp, tornando mais simples para times fiscais, contábeis e de backoffice conferirem documentos, manterem cadastros organizados e gerarem relatórios confiáveis.
