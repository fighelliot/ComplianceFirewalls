import os
import re
import pdfkit
import pandas as pd
from xml.etree import ElementTree as ET
from datetime import datetime

def parse_switch(config_lines):
    data = {
        "vlans": [],
        "ports": [],
        "auth": [],
        "snmp": [],
        "syslog": [],
        "mac_security": [],
        "bpdu_guard": [],
    }
    section = None
    buffer = []
    for line in config_lines:
        l = line.strip()
        if l.startswith("config vlan"):
            section = "vlans"; buffer = []
        elif l.startswith("config port"):
            section = "ports"; buffer = []
        elif l.startswith("config authentication"):
            section = "auth"; buffer = []
        elif l.startswith("config system snmp"):
            section = "snmp"; buffer = []
        elif l.startswith("config log syslogd"):
            section = "syslog"; buffer = []
        elif l.startswith("config mac-security"):
            section = "mac_security"; buffer = []
        elif l.startswith("config bpdu-guard"):
            section = "bpdu_guard"; buffer = []
        elif l == "end":
            if section and buffer:
                data[section].append('\n'.join(buffer))
            section = None; buffer = []
        elif section:
            buffer.append(l)
    return data

def parse_wifi(config_lines):
    data = {
        "ssids": [],
        "security": [],
        "radios": [],
        "vlan": [],
        "guest": [],
        "snmp": [],
        "syslog": [],
    }
    section = None
    buffer = []
    for line in config_lines:
        l = line.strip()
        if l.startswith("config wireless-controller vap"):
            section = "ssids"; buffer = []
        elif l.startswith("config wireless-controller security"):
            section = "security"; buffer = []
        elif l.startswith("config wireless-controller radio"):
            section = "radios"; buffer = []
        elif l.startswith("config wireless-controller vlan"):
            section = "vlan"; buffer = []
        elif l.startswith("config guest"):
            section = "guest"; buffer = []
        elif l.startswith("config system snmp"):
            section = "snmp"; buffer = []
        elif l.startswith("config log syslogd"):
            section = "syslog"; buffer = []
        elif l == "end":
            if section and buffer:
                data[section].append('\n'.join(buffer))
            section = None; buffer = []
        elif section:
            buffer.append(l)
    return data

def compliance_check(results):
    return "OK" if not results else "FALHOU"

# --- SWITCH CHECKS ---
def check_vlan_config(vlans):
    findings = []
    if not vlans:
        findings.append("Nenhuma VLAN configurada.")
    for idx, vlan in enumerate(vlans):
        if "default" in vlan.lower():
            findings.append(f"VLAN default em uso (Bloco #{idx+1})")
    return findings

def check_port_security(ports):
    findings = []
    for idx, port in enumerate(ports):
        if "trunk" not in port.lower() and "tagged" not in port.lower():
            findings.append(f"Porta sem trunk/tag (Bloco #{idx+1})")
    return findings

def check_mac_security(mac_security):
    findings = []
    if not mac_security:
        findings.append("MAC security não configurado.")
    return findings

def check_bpdu_guard(bpdu_guard):
    findings = []
    if not bpdu_guard:
        findings.append("BPDU Guard não configurado.")
    return findings

def check_auth(auth):
    findings = []
    if not auth:
        findings.append("Autenticação 802.1X/RADIUS não configurada.")
    return findings

def check_snmp(snmp):
    return [] if snmp else ["SNMP NÃO configurado!"]

def check_syslog(syslog):
    return [] if syslog else ["Syslog NÃO configurado!"]

# --- WIFI CHECKS ---
def check_ssids(ssids):
    findings = []
    if not ssids:
        findings.append("Nenhum SSID configurado.")
    for idx, ssid in enumerate(ssids):
        if "open" in ssid.lower():
            findings.append(f"SSID aberto detectado (Bloco #{idx+1})")
    return findings

def check_wifi_security(security):
    findings = []
    for idx, sec in enumerate(security):
        if "wpa2" not in sec.lower() and "wpa3" not in sec.lower():
            findings.append(f"Rede sem WPA2/WPA3 (Bloco #{idx+1})")
    return findings

def check_radios(radios):
    findings = []
    if not radios:
        findings.append("Nenhum radio configurado.")
    return findings

def check_guest(guest):
    findings = []
    if not guest:
        findings.append("Rede guest não configurada.")
    return findings

def check_wifi_vlan(vlan):
    findings = []
    if not vlan:
        findings.append("VLAN Wi-Fi não configurada.")
    return findings

# --- RELATÓRIOS (igual ao do firewall, adaptado) ---
def generate_html_report(tipo, sections, results_summary, results_details):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    total_checks = len(results_summary)
    passed = sum(1 for v in results_summary.values() if v == "OK")
    failed = total_checks - passed
    check_names = list(results_summary.keys())
    check_results = [1 if v == "OK" else 0 for v in results_summary.values()]

    html_content = f"""<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>Relatório Fortinet {tipo.capitalize()}</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
    body {{ font-family: Arial, sans-serif; background: #f8f8f8; }}
    h2 {{ color: #2d4a73; }}
    table {{ border-collapse: collapse; width: 100%; background: #fff; margin-bottom: 2em; }}
    th, td {{ border: 1px solid #ccc; padding: 8px; }}
    th {{ background: #eaeaea; }}
    .ok {{ color: green; font-weight: bold; }}
    .fail {{ color: red; font-weight: bold; }}
    pre {{ background: #f0f0f0; padding: 10px; border-radius: 5px; }}
    </style>
</head>
<body>
    <h1>Relatório de Compliance Fortinet {tipo.capitalize()}</h1>
    <p>Data de análise: {now}</p>
    <h2>Resumo das Validações</h2>
    <table>
        <tr>
            <th>Validação</th>
            <th>Status</th>
        </tr>
"""
    for check, status in results_summary.items():
        color = "ok" if status == "OK" else "fail"
        html_content += f"<tr><td>{check}</td><td class='{color}'>{status}</td></tr>\n"
    html_content += "</table>\n"

    html_content += f"""
    <h2>Gráfico de Compliance</h2>
    <canvas id="complianceChart" width="800" height="350"></canvas>
    <script>
    const ctx = document.getElementById('complianceChart').getContext('2d');
    new Chart(ctx, {{
        type: 'bar',
        data: {{
            labels: {check_names},
            datasets: [{
                label: 'Compliance',
                data: {check_results},
                backgroundColor: {['"green"' if v == 1 else '"red"' for v in check_results]},
            }}]
        }},
        options: {{
            scales: {{
                y: {{
                    beginAtZero: true,
                    max: 1,
                    ticks: {{
                        callback: function(value) {{
                            return value === 1 ? 'OK' : 'FALHOU';
                        }}
                    }}
                }}
            }},
            plugins: {{
                legend: {{display: false}}
            }}
        }}
    }});
    </script>
    <h3>Percentual de Compliance: <span style="color:{{'green' if failed==0 else 'orange'}}">{round(passed/total_checks*100,1)}%</span></h3>
    """

    html_content += "<h2>Detalhes das Validações</h2>\n"
    for check, details in results_details.items():
        html_content += f"<h3>{check}</h3>\n"
        if details:
            html_content += "<ul>\n"
            for item in details:
                html_content += f"<li>{item}</li>\n"
            html_content += "</ul>\n"
        else:
            html_content += "<p class='ok'>Nenhum problema encontrado.</p>\n"

    html_content += "<h2>Blocos Principais de Configuração</h2>\n"
    for section, blocks in sections.items():
        html_content += f"<h3>{section.capitalize()}</h3>\n"
        for idx, block in enumerate(blocks):
            html_content += f"<pre>Bloco #{idx+1}\n{block}</pre>\n"
    html_content += "</body></html>"
    with open(f"relatorio_fortinet_{tipo}.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Relatório HTML gerado: relatorio_fortinet_{tipo}.html")
    try:
        pdfkit.from_file(f"relatorio_fortinet_{tipo}.html", f"relatorio_fortinet_{tipo}.pdf")
        print(f"Relatório PDF gerado: relatorio_fortinet_{tipo}.pdf")
    except Exception as e:
        print(f"Falha na exportação para PDF: {e}\nVerifique se o wkhtmltopdf está instalado no sistema.")

def export_to_excel(results_summary, results_details, sections, tipo):
    df_summary = pd.DataFrame(list(results_summary.items()), columns=["Validação", "Status"])
    details_list = []
    for check, details in results_details.items():
        if details:
            for item in details:
                details_list.append({"Validação": check, "Detalhe": item})
        else:
            details_list.append({"Validação": check, "Detalhe": "Nenhum problema encontrado."})
    df_details = pd.DataFrame(details_list)
    blocks_list = []
    for section, blocks in sections.items():
        for idx, block in enumerate(blocks):
            blocks_list.append({"Bloco": section, "ID": idx+1, "Conteúdo": block})
    df_blocks = pd.DataFrame(blocks_list)
    with pd.ExcelWriter(f"relatorio_fortinet_{tipo}.xlsx", engine="openpyxl") as writer:
        df_summary.to_excel(writer, sheet_name="Resumo", index=False)
        df_details.to_excel(writer, sheet_name="Detalhes", index=False)
        df_blocks.to_excel(writer, sheet_name="Configuração", index=False)
    print(f"Relatório Excel gerado: relatorio_fortinet_{tipo}.xlsx")

def main():
    print("==== Validador Avançado de Configuração Switch/WiFi Fortinet ====")
    tipo = input("Informe o tipo (switch/wifi): ").strip().lower()
    config_file = input("Informe o caminho do arquivo de configuração: ").strip()

    if not os.path.isfile(config_file):
        print("Arquivo não encontrado. Verifique o caminho e tente novamente.")
        return

    with open(config_file, encoding='utf-8', errors='ignore') as f:
        config_lines = f.readlines()

    print(f"\n--- Iniciando parsing para {tipo} ---")
    if tipo == "switch":
        sections = parse_switch(config_lines)
        # Validações de Switch
        results_details = {
            "VLANs configuradas": check_vlan_config(sections["vlans"]),
            "Portas trunk/tag": check_port_security(sections["ports"]),
            "MAC security": check_mac_security(sections["mac_security"]),
            "BPDU Guard": check_bpdu_guard(sections["bpdu_guard"]),
            "Autenticação 802.1X/RADIUS": check_auth(sections["auth"]),
            "SNMP configurado": check_snmp(sections["snmp"]),
            "Syslog configurado": check_syslog(sections["syslog"]),
        }
    elif tipo == "wifi":
        sections = parse_wifi(config_lines)
        # Validações de Wi-Fi
        results_details = {
            "SSIDs configurados": check_ssids(sections["ssids"]),
            "Segurança WPA2/WPA3": check_wifi_security(sections["security"]),
            "Radios configurados": check_radios(sections["radios"]),
            "Rede guest": check_guest(sections["guest"]),
            "VLAN Wi-Fi": check_wifi_vlan(sections["vlan"]),
            "SNMP configurado": check_snmp(sections["snmp"]),
            "Syslog configurado": check_syslog(sections["syslog"]),
        }
    else:
        print("Tipo não suportado.")
        return

    results_summary = {k: compliance_check(v) for k, v in results_details.items()}
    generate_html_report(tipo, sections, results_summary, results_details)
    export_to_excel(results_summary, results_details, sections, tipo)
    print("--- Fim das validações ---")

if __name__ == "__main__":
    main()