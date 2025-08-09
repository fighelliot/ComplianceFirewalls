# ComplianceFirewalls

Ferramenta de Compliance e Validação para configurações de firewall Fortigate e Palo Alto.  
Gera relatórios em HTML (com gráficos), PDF e Excel a partir de arquivos de configuração.

## Funcionalidades
- Validação avançada de regras e boas práticas
- Relatório HTML detalhado com gráficos de compliance (Chart.js)
- Exportação automática para PDF (`pdfkit` e `wkhtmltopdf`)
- Exportação para Excel (`pandas` e `openpyxl`)
- Suporte a Fortigate (plain text) e Palo Alto (XML)

## Requisitos

```bash
pip install -r requirements.txt
```
Além disso, instale o [wkhtmltopdf](https://wkhtmltopdf.org/downloads.html) no seu sistema para exportação PDF.

## Uso

```bash
python advanced_firewall_checker.py
```

Siga as instruções no terminal para informar o fabricante e o arquivo de configuração.

## Arquivos gerados
- **relatorio_firewall.html** — Relatório detalhado com gráficos
- **relatorio_firewall.pdf** — Relatório em PDF
- **relatorio_firewall.xlsx** — Resumo, detalhes e blocos de configuração em Excel

## Exemplo de configuração suportada

- Fortigate: arquivo plain-text (exportado do firewall)
- Palo Alto: arquivo XML de configuração

## Licença

MIT
