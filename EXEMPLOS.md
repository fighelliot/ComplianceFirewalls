# Exemplos de Uso dos Scripts - ComplianceFirewalls

Este documento traz exemplos práticos de execução dos scripts do repositório, com explicações sobre parâmetros e saída esperada.

---

## 1. Validador Avançado de Configuração FortiSwitch/FortiWiFi

**Arquivo:** `advanced_fortinet_switch_wifi_checker.py`

### Uso básico:

```sh
python advanced_fortinet_switch_wifi_checker.py
```

O script irá solicitar:

- `Informe o tipo (switch/wifi):` → Digite `switch` ou `wifi` conforme o tipo do equipamento.
- `Informe o caminho do arquivo de configuração:` → Informe o caminho do arquivo texto exportado do equipamento.

### Exemplo Switch:

```sh
python advanced_fortinet_switch_wifi_checker.py
```
```
Informe o tipo (switch/wifi): switch
Informe o caminho do arquivo de configuração: configs/switch01.conf
```

### Exemplo WiFi:

```sh
python advanced_fortinet_switch_wifi_checker.py
```
```
Informe o tipo (switch/wifi): wifi
Informe o caminho do arquivo de configuração: configs/wifi01.conf
```

### Saídas geradas:

- `relatorio_fortinet_switch.html` / `relatorio_fortinet_wifi.html` (relatório visual)
- `relatorio_fortinet_switch.pdf` / `relatorio_fortinet_wifi.pdf` (relatório PDF)
- `relatorio_fortinet_switch.xlsx` / `relatorio_fortinet_wifi.xlsx` (relatório Excel)

> **Dica:** Para visualizar o relatório, abra o arquivo HTML no navegador.

---

## 2. Validador de Configuração de Firewalls Fortinet

**Arquivo:** `fortinet_firewall_checker.py`

### Uso básico:

```sh
python fortinet_firewall_checker.py
```

O script irá solicitar:

- Caminho do arquivo de configuração do firewall.

### Exemplo:

```sh
python fortinet_firewall_checker.py
```
```
Informe o caminho do arquivo de configuração do firewall: configs/firewall01.conf
```

### Saídas geradas:

- `relatorio_fortinet_firewall.html` (relatório visual)
- `relatorio_fortinet_firewall.pdf` (relatório PDF)
- `relatorio_fortinet_firewall.xlsx` (relatório Excel)

---

## 3. Validador de Configuração Palo Alto

**Arquivo:** `paloalto_firewall_checker.py`

### Uso básico:

```sh
python paloalto_firewall_checker.py
```

O script irá solicitar:

- Caminho do arquivo de configuração XML exportado do firewall Palo Alto.

### Exemplo:

```sh
python paloalto_firewall_checker.py
```
```
Informe o caminho do arquivo de configuração (XML): configs/paloalto01.xml
```

### Saídas geradas:

- `relatorio_paloalto_firewall.html` (relatório visual)
- `relatorio_paloalto_firewall.pdf` (relatório PDF)
- `relatorio_paloalto_firewall.xlsx` (relatório Excel)

---

## 4. Dependências do Projeto

**Arquivo:** `requirements.txt`

Instale as dependências com:

```sh
pip install -r requirements.txt
```

Para exportar PDF, é necessário instalar o **wkhtmltopdf** no sistema operacional.  
Exemplo para Ubuntu:

```sh
sudo apt-get install wkhtmltopdf
```

---

## 5. Observações Importantes

- Recomenda-se executar os scripts em ambiente Python 3.8+.
- Os arquivos de configuração devem ser exportados em formato texto (para switches/wifi) ou XML (para Palo Alto).
- Os relatórios gerados trazem um resumo visual do compliance e detalhes dos blocos problemáticos.

---

## Referências nos Scripts

Todos os scripts possuem comentários no início e ao longo do código explicando:
- Quais funções fazem parsing dos arquivos
- Quais funções realizam checagens de compliance
- Como os relatórios são gerados (HTML/PDF/Excel)
- Pontos de entrada (função `main()`)

Exemplo de apontamento no código:

```python
# Definição da função principal
def main():
    # Solicita tipo de equipamento e caminho do arquivo
    ...
    # Executa parsing e validações conforme tipo selecionado
    ...
    # Gera relatórios em HTML, PDF e Excel
    ...
```

---

## Dúvidas?

Consulte o README ou abra uma Issue no repositório!