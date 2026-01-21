"""SimplesVet Scrapper - Busca lançamentos financeiros por período."""

from datetime import datetime
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup


def parse_value(text: str) -> float:
    """Converte valor brasileiro para float."""
    if not text:
        return 0.0
    return float(text.strip().replace(".", "").replace(",", "."))


def to_iso(date_str: str, year: int = None) -> str:
    """Converte data BR para ISO (YYYY-MM-DD).

    Args:
        date_str: Data em formato DD/MM ou DD/MM/YYYY
        year: Ano a usar se não informado na data

    Returns:
        Data em formato YYYY-MM-DD ou None se inválida
    """
    if not date_str:
        return None

    parts = date_str.strip().split("/")

    if len(parts) == 2:  # DD/MM
        day, month = int(parts[0]), int(parts[1])
        if year is None:
            year = datetime.now().year
        return f"{year}-{month:02d}-{day:02d}"

    elif len(parts) == 3:  # DD/MM/YYYY
        day, month, year = int(parts[0]), int(parts[1]), int(parts[2])
        return f"{year}-{month:02d}-{day:02d}"

    return None


def transform_html(html: str) -> list[dict]:
    """Converte HTML de lançamentos para lista de dicts."""
    soup = BeautifulSoup(html, "html.parser")
    lancamentos = []

    for row in soup.select("tr.linhaRegistro"):
        receita = row.select_one(".tdReceita")
        despesa = row.select_one(".tdDespesa")

        # Extrai vencimento primeiro para pegar o ano
        vencimento_br = row.get("data-vencimento")
        vencimento = to_iso(vencimento_br)

        # Extrai ano do vencimento para usar na data
        ano_vencimento = None
        if vencimento:
            ano_vencimento = int(vencimento.split("-")[0])

        # Converte data usando ano do vencimento
        data_br = row.select_one(".tdData").get_text(strip=True)
        data = to_iso(data_br, ano_vencimento)

        lancamentos.append(
            {
                "id_r": row.get("id"),
                "data": data,
                "descricao": row.select_one(".tdDescricao").get_text(" ", strip=True),
                "fornecedor": row.select_one(".tdFornecedor").get_text(strip=True),
                "parcela": row.select_one(".tdParcela").get_text(strip=True) or None,
                "valor": (
                    parse_value(receita.get_text())
                    if receita
                    else -parse_value(despesa.get_text())
                ),
                "tipo": "receita" if receita else "despesa",
                "status": row.get("data-status"),
                "origem": row.get("data-origem"),
                "vencimento": vencimento,
                "forma_pagamento": row.get("data-tipofromapagamento"),
            }
        )

    return lancamentos


def format_date_range(start: str, end: str) -> str:
    """Formata período para DD/MM/YYYY-DD/MM/YYYY."""

    def to_br(d):
        if "/" in d:
            return d
        return datetime.strptime(d, "%Y-%m-%d").strftime("%d/%m/%Y")

    return f"{to_br(start)}-{to_br(end)}"


def get_releases(
    email: str, password: str, data_inicio: str, data_fim: str
) -> list[dict]:
    """
    Busca lançamentos financeiros do SimplesVet.

    Args:
        email: Email de login
        password: Senha
        data_inicio: Data inicial (YYYY-MM-DD ou DD/MM/YYYY)
        data_fim: Data final (YYYY-MM-DD ou DD/MM/YYYY)

    Returns:
        Lista de lançamentos
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True, args=["--disable-blink-features=AutomationControlled"]
        )
        page = browser.new_page(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1920, "height": 1080},
            locale="pt-BR",
        )

        # Login
        page.goto("https://app.simples.vet/login/login.php")
        page.get_by_role("textbox", name="Email").fill(email)
        page.get_by_role("textbox", name="Senha").fill(password)
        page.get_by_role("button", name="Entrar no SimplesVet").click()
        page.wait_for_load_state("networkidle")

        # Buscar lançamentos
        form_data = {
            "p__lan_dat_ordem": format_date_range(data_inicio, data_fim),
            "p__cta_int_codigo": "T",
            "p__cta_int_codigo_text": "Todas as contas",
            "p__cat_int_codigo": "",
            "p__cat_int_codigo_text": "Todas as categorias",
            "p__selecionado": "",
            "p__tipo_exportar": "",
            "p__usu_int_codigo_relatoriolog": "",
            "p__for_int_codigo": "",
            "p__for_int_codigo_text": "",
            "p__lan_cha_status": "",
            "p__lan_cha_status_text": "",
            "p__lan_cha_natureza": "",
            "p__lan_cha_natureza_text": "",
            "p__lan_cha_competencia": "CX",
            "p__lan_cha_competencia_text": "",
            "p__fpg_int_codigo": "",
            "p__fpg_int_codigo_text": "",
            "p__frb_int_codigo": "",
            "p__frb_int_codigo_text": "",
            "p__cta_cha_tipo": "",
            "p__cta_cha_tipo_text": "",
            "p__lan_txt_descricao": "",
            "p__cai_int_id": "",
            "p__lan_dec_valor": "",
            "p__lan_var_documento": "",
            "AMBIENTE": "4bac1806d6cbcbf548df329af0065a2b566d7383",
        }

        response = page.request.post(
            "https://app.simples.vet/financeiro/lancamento/lancamento_load.php",
            form=form_data,
        )

        # Ler conteúdo ANTES de fechar o browser
        html_content = response.text()
        browser.close()

        return transform_html(html_content)
